**Group Info:**

Jialing Zhu jz72@illinois.edu - MSFE

Jiaqi (Ivan) Su jiaqisu2@illinois.edu - MSFE

Guancheng Guo gguo5@illinois.edu - MSFE

Lingyu He lingyuh2@illinois.edu - MSFE


**Project Structure:**

- GroupOneStrategy: This contains the C++ codes for our strategy 
- backtesting-cra-exports: This contains the results of running backtest on our strategy 
- python_src : This contains the Python codes for our correlation analyses 
- backtest_archive: This contains the backtesting results of our intial (non-optimized) strategy

---

**How to run and backtest a Strategy**

- clone the repo in your current folder
```
git clone https://gitlab.engr.illinois.edu/fin566_algo_market_micro_fall_2020/fin566_fall_2020_group_one.git
```
- Build the stratey using the bash script under fin566_fall_2020_group_one/GroupOneStrategy
```
./build_n_update
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This will automatically build and update the strategy in the backtesting engine, then it will automatically start the backtesting engine


- To backtest, first create an instance of the trading strategy. Enter the following command in the backtesting engine UI:
```
create_instance GroupOneStrategy GroupOneStrategy UIUC SIM-1001-101 dlariviere 100000 -symbols SPY|VXX
```

- Start the backtest：
```
start_backtest YYYY-MM-DD YYYY-MM-DD GroupOneStrategy 1
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;where the first date represents the starting date and the second dates represents the end date


- When the backtest is finished, search for the backtesting result which is in the following path, and it is in .cra format. The cra file can be found using the following command：
```
ls /home/vagrant/Desktop/strategy_studio/backtesting/backtesting-results
```

- export the cra file to csv format:
```
export_cra_file backtesting-results/FILE_NAME.cra backtesting/backtesting-cra-exports
```

- The backtesting result in csv format will be saved in backtesting/backtesting-cra-exports
