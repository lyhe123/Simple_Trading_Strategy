/*================================================================================                               
*     Source: ../RCM/StrategyStudio/examples/strategies/SimpleMomentumStrategy/SimpleMomentumStrategy.cpp                                                        
*     Last Update: 2013/6/1 13:55:14                                                                            
*     Contents:                                     
*     Distribution:          
*                                                                                                                
*                                                                                                                
*     Copyright (c) RCM-X, 2011 - 2013.                                                  
*     All rights reserved.                                                                                       
*                                                                                                                
*     This software is part of Licensed material, which is the property of RCM-X ("Company"), 
*     and constitutes Confidential Information of the Company.                                                  
*     Unauthorized use, modification, duplication or distribution is strictly prohibited by Federal law.         
*     No title to or ownership of this software is hereby transferred.                                          
*                                                                                                                
*     The software is provided "as is", and in no event shall the Company or any of its affiliates or successors be liable for any 
*     damages, including any lost profits or other incidental or consequential damages relating to the use of this software.       
*     The Company makes no representations or warranties, express or implied, with regards to this software.                        
/*================================================================================*/   

#ifdef _WIN32
    #include "stdafx.h"
#endif

#include "GroupOneStrategy.h"

#include "FillInfo.h"
#include "AllEventMsg.h"
#include "ExecutionTypes.h"
#include <Utilities/Cast.h>
#include <Utilities/utils.h>

#include <math.h>
#include <iostream>
#include <cassert>
#include <queue>
#include <sstream>

using namespace RCM::StrategyStudio;
using namespace RCM::StrategyStudio::MarketModels;
using namespace RCM::StrategyStudio::Utilities;

using namespace std;

GroupOneStrategy::GroupOneStrategy(StrategyID strategyID, const std::string& strategyName, const std::string& groupName):
    Strategy(strategyID, strategyName, groupName),
    m_instrument_order_id_map(),
	m_instrumentX(NULL),
	m_instrumentY(NULL),
    m_aggressiveness(0.2),
    m_position_size(100),
    m_debug_on(true),
	ma_first(0),
	ma_second(0),
	last_trade(0),
	trade_count(0),
	hold_position(0),
	current_50_trades(50,0.0),
	lagged_50_trades(50, 0.0),
	max_trade_num(10000000000000), //make sure that all the orders are cleared by the end of the trading day
	trade_num(0),
	seen_spy(0),
	seen_vxx(0)
{
    
}

GroupOneStrategy::~GroupOneStrategy()
{
}

void GroupOneStrategy::OnResetStrategyState()
{
   	m_instrument_order_id_map.clear();
	trade_num = 0;
	hold_position = 0;
	seen_spy = 0;
	seen_vxx = 0;
	m_instrumentY = NULL;
	m_instrumentX = NULL;
	std::cout << "RESET" << std::endl;
}

void GroupOneStrategy::DefineStrategyParams()
{
    CreateStrategyParamArgs arg1("aggressiveness", STRATEGY_PARAM_TYPE_RUNTIME, VALUE_TYPE_DOUBLE, m_aggressiveness);
    params().CreateParam(arg1);

    CreateStrategyParamArgs arg2("position_size", STRATEGY_PARAM_TYPE_RUNTIME, VALUE_TYPE_INT, m_position_size);
    params().CreateParam(arg2);
    
    CreateStrategyParamArgs arg3("debug", STRATEGY_PARAM_TYPE_RUNTIME, VALUE_TYPE_BOOL, m_debug_on);
    params().CreateParam(arg3);
}

void GroupOneStrategy::DefineStrategyCommands()
{
    StrategyCommand command1(1, "Reprice Existing Orders");
    commands().AddCommand(command1);

    StrategyCommand command2(2, "Cancel All Orders");
    commands().AddCommand(command2);
}

void GroupOneStrategy::RegisterForStrategyEvents(StrategyEventRegister* eventRegister, DateType currDate)
{    
    for (SymbolSetConstIter it = symbols_begin(); it != symbols_end(); ++it) {
        eventRegister->RegisterForBars(*it, BAR_TYPE_TIME, 10);
    }
}

void GroupOneStrategy::OnTrade(const TradeDataEventMsg& msg)
{
	//std::cout << "OnTrade(): (" << msg.adapter_time() << "): " << msg.instrument().symbol() << ": " << msg.trade().size() << " @ $" << msg.trade().price() << std::endl;
	
	std::stringstream ss;
	ss << msg.adapter_time();			
	std::string tmstp = ss.str();
	std::string time = tmstp.substr(tmstp.find(' ') + 1, 6);
	std::string hour = time.substr(0, time.find(':'));
	std::string minutes = time.substr(time.find(':') + 1);
	int minutes_int = std::stoi(minutes);
	int hour_int = std::stoi(hour);
	if (hour_int >= 19 && minutes_int >= 59) { // at the last minute close our position
		if (hold_position == 1) {
			this->SendOrder(m_instrumentY, -100); //close position when close to end of trading day to eliminate potiential risk during market closure
			std::cout <<"End of the day, close position" << endl;
		}
	}
	else if (hour_int == 13 && minutes_int <= 31) {
		//Do nothing, this is added to avoid a bug occured on 13:00
	}
	else {
		if ((m_instrumentX == NULL) or (m_instrumentY == NULL)) {
			if (msg.instrument().symbol() == "SPY") {
				m_instrumentX = &msg.instrument(); //assign symbol SPY to m_instrumentX
				seen_spy = 1;
			}
			if (msg.instrument().symbol() == "VXX") {
				m_instrumentY = &msg.instrument();  //assign symbol VXX to m_instrumentY
				seen_vxx = 1;
			}
		}
		
		if (msg.instrument().symbol() == "SPY" && (seen_spy * seen_vxx == 1)) {
			current_50_trades.pop_front(); //remove the oldest trade price
			current_50_trades.push_back(msg.trade().price()); //add the latest trade price 

			ma_first = 0; //varaible to store the moving sum of the current 50 trade prices
			ma_second = 0; //variable to store the moving sum of lagged 50 trade prices

			for (int i = 0; i < 50; i++) {
				ma_first = ma_first + current_50_trades[i]; //compute the sum of the cuurent 50 trade prices
				ma_second = ma_second + lagged_50_trades[i]; //compute the sum of the lagged 50 trade prices 
			}

			ma_first = ma_first / 50; //compute the moving avarage 
			ma_second = ma_second / 50;

			if (trade_count >= 51 && trade_num <= max_trade_num) { //only execute our strategy when there are at least 51 trades 
				if ((ma_second - ma_first) >= 0.0004 && hold_position == 0) {
					this->SendOrder(m_instrumentY, 100); //buy VXX when the difference is above or equal the threshold 
				}

				if ((ma_second - ma_first) <= -0.0004 && hold_position == 1) {
					this->SendOrder(m_instrumentY, -100); //sell VXX when the difference is less than the threshold 
				}
			}
			
			
			
			trade_count++;   //update the trade count after we send an order 
			lagged_50_trades = current_50_trades; //now the current_50_trades becomes the lagged_50_trades as a new order is sent
		}
	}
}

void GroupOneStrategy::OnBar(const BarEventMsg& msg)
{

}

void GroupOneStrategy::OnOrderUpdate(const OrderUpdateEventMsg& msg)
{    
	std::cout << "OnOrderUpdate():" << msg.update_time() << msg.name() << std::endl;
	if(msg.completes_order()) {
		m_instrument_order_id_map[msg.order().instrument()] = 0;
		std::cout << "OnOrderUpdate(): oder is complete; " << std::endl;
		if (msg.order().order_side() == ORDER_SIDE_BUY) {
			hold_position = 1;   //set the flag variable to be 1 when we are in buy side 
		}
		else {
			hold_position = 0; // set the flag varaible to be 0 when we are in sell side 
		}
	} 
}

void GroupOneStrategy::AdjustPortfolio(const Instrument* instrument, int desired_position)
{

}

void GroupOneStrategy::SendSimpleOrder(const Instrument* instrument, int trade_size)
{

}

void GroupOneStrategy::SendOrder(const Instrument* instrument, int trade_size)
{
	
    if(instrument->top_quote().ask()<.01 || instrument->top_quote().bid()<.01 || !instrument->top_quote().ask_side().IsValid() || !instrument->top_quote().ask_side().IsValid()) {
        std::stringstream ss;
        ss << "Sending buy order for " << instrument->symbol() << " at price " << instrument->top_quote().ask() << " and quantity " << trade_size <<" with missing quote data";   
        logger().LogToClient(LOGLEVEL_DEBUG, ss.str());
        std::cout << "SendOrder(): " << ss.str() << std::endl;
        
     }

    double price = trade_size > 0 ? instrument->top_quote().bid() + m_aggressiveness : instrument->top_quote().ask() - m_aggressiveness;

    OrderParams params(*instrument, 
        abs(trade_size),
        price, 
        MARKET_CENTER_ID_IEX,
        (trade_size>0) ? ORDER_SIDE_BUY : ORDER_SIDE_SELL,
        ORDER_TIF_DAY,
        ORDER_TYPE_MARKET);

    if (trade_actions()->SendNewOrder(params) == TRADE_ACTION_RESULT_SUCCESSFUL) {
        m_instrument_order_id_map[instrument] = params.order_id;
		std::cout << "SendOrder(): Sending new order successful!" << std::endl;
		trade_num++;
    }
	else
	{
		std::cout << "SendOrder(): Error sending new order!!!" << std::endl;
	}
}

void GroupOneStrategy::RepriceAll()
{
    for (IOrderTracker::WorkingOrdersConstIter ordit = orders().working_orders_begin(); ordit != orders().working_orders_end(); ++ordit) {
        Reprice(*ordit);
    }
}

void GroupOneStrategy::Reprice(Order* order)
{
    OrderParams params = order->params();
    params.price = (order->order_side() == ORDER_SIDE_BUY) ? order->instrument()->top_quote().bid() + m_aggressiveness : order->instrument()->top_quote().ask() - m_aggressiveness;
    trade_actions()->SendCancelReplaceOrder(order->order_id(), params);
}

void GroupOneStrategy::OnStrategyCommand(const StrategyCommandEventMsg& msg)
{
    switch (msg.command_id()) {
        case 1:
            RepriceAll();
            break;
        case 2:
            trade_actions()->SendCancelAll();
            break;
        default:
            logger().LogToClient(LOGLEVEL_DEBUG, "Unknown strategy command received");
            break;
    }
}

void GroupOneStrategy::OnParamChanged(StrategyParam& param)
{    
 
}
