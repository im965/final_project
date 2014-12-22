
# portfolioFactory: A simple Python package to build cross-sectional equity portfolios

## Team Members

Peter Li (PHL232)

Israel Malkin (IM965)

## What is it

A Python package ( that streamlines the process for building cross-sectional trading strategies/factors. 
In our examples, we show how you can easily use **portfolioFactory** to implement [**momentum**][momentum] (i.e. buy the winners) strategies with different 
horizons and selection criteria. In addition, we demonstrate the flexibility of the package by building generic cross-sectional strategy based on realized volatility.

## Quick Start

After installing all the required packages [See Dependencies], the demo can be run via the terminal in Python's interactive mode. This allows the user to explore the 
returned object and plots.

```
>>>./final_project/phl232$ python

Python 2.7.6 (default, Mar 22 2014, 22:59:56) 
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.

>>> import demo
>>> strategy = demo.main() 
```

The demo will first ask for the location of the universe and strategy config file [See Demonstration for full explanation]. Please select the following files:

- Returns File: ./final_project/phl232/ExampleFile/assetReturnsData_SELECTME
- Config File: ./final_project/phl232/ExampleFile/config_Ex1.txt

Once the portfolio has been formed, the program will prompt for dates for plotting. 

```
For plotting, please supply the following input: 
Start Year (min 1991): 1995
End Year (max 2014): 2012
Rolling Analysis Window (list of 4 integer window lengths e.g. [3,6,12,24], max window = 72): [3,6,12,24]
```

The program will return the strategy object along with two figures showing risk/return metrics and plots for the strategy The strategy object can be used in the standard ways. For example:

```
>>> help(strategy)
>>> strategy.strategyReturns
```

## Demonstration

As discussed, we show 3 examples that make use of our package. Examples can be run via the terminal using the demo module from the main directory after going through this user guide.

The data for the examples can be found in /ExampleData. The examples will return a series of plots showing the risk/return characteristics of the specified strategy. 
Additionally, the example will return a strategy object. For convenience, we have already created the necessary datasets and config files to run the examples demonstrated below. 

The demo module takes care of manually entering commands into the terminal, when prompted please select the appropriate datasets and config files.
The examples below are written so that after going through them you will be able to generate a custom strategy with the help of the demo module, but 
also to exhibit how someone could use the functionality and flexibility of the package to generate various strategies *without the demo module*.

### Initializing a universe

universe is the primary data container for portoflioFactory. This object defines the entire universe (set of potential investments) upon which the different investment strategies can be generated. To start the procedure, one would initialize a universe object by passing the location of a pickled pandas dataframe (of **monthly** stock returns) to the *universe* constructor.
```
example_uni = universe('Name','./ExampleData/universeData')
```
Where universeData is the path to a pickled pandas dataframe containing stock returns. 

In the demo module you will not have to explicitly pass any commands, you will simply be asked to select (click) on the universe file the we have pre-loaded into the /ExampleData directory. 

All strategies generated through the demo will be defined on the same universe so you will have to select this file for all the examples below.
The universe dataset we provide consists of monthly returns data for around 3000 companies. This data can be obtained from a number of online sources e.g. Yahoo, Google and Quandl. 

After creating a universe object, you are now ready to define a strategy over all the stocks in this universe.

### Example I: Momentum strategy of top 300 stocks with annual rebalancing

Suppose an investor has the idea that stocks that have performed well will continue to perform well. To test this strategy, the investor uses the the following procedure:
- At the end of each year, look back over the previous *12 months* and buy the top *300* stocks as ranked by *12 month* return
- Hold these *300* stocks for *12 months*
- Repeat the sorting procedure and form a new portfolio every *12 months* (aka rebalace every 12 months)


To implement this strategy using **portfolioFactory**, pass the *strategy* constructor a universe object and the location of a config file:
```
strategy_ex1 = strategy(example_uni,'./ExampleData/config_Ex1.txt')
```

The config file config_Ex1.txt would look like:
```
name = first example strategy
signalPath = ./ExampleFiles/rolling_returns_12m
rebalanceWindow = 12
rule = 300 
```
The strategy config file must include the four parameters as above:
- *Name* can be anything you wish to name the strategy.
- *signalPath* specifies the path for a pickled pandas dataframe which will be used as a signal. These are called *signals* because buying/selling is based on this data, so for this first example we are using 12-month rolling returns as the *signal*.
- *rebalanceWindow* specifies how often the sorting procedure should take place.
- *rule* specifies how many investments should be picked based on the signal. 

Putting it all together, we are picking the top 300 (*rule*) stocks based on 12-month rolling returns (*signal*) and reoptimizing every 12 months (*rebalanceWindow*).

Again, the config file *config_Ex1.txt* and the *rolling_returns_12m* signal dataset specified in that config file have been pre-loaded for use in the demo, you will simply have to click
the desired config file to select it.
 
Note that such *signal* datasets (rolling returns, rolling volatility, etc.) are easily generated using the pandas rolling_apply method.
For this example, we created the *rolling_returns_12m signal* easily with:
```
rolling_returns_12m = (pd.rolling_apply(1+universeData,window=12,func=np.prod,min_periods=12) - 1) 
pd.to_pickle('./ExampleFiles/rolling_returns_12m')
```

In the demo, after selecting the universe and config file the strategy will be generated by selecting the top 300 stocks based on 12-month rolling returns and be rebalanced every 12 months.
This procedure might take a little while (around 30 seconds), you will then be asked to enter a starting and ending year over which the plots will be generated and risk metrics will be calculated.
The risk metrics will be displayed on the figures.

### Example II: Momentum strategy of top 300 stocks with semi-annual rebalancing

After looking at the return metrics generated by the first strategy, the investor decided that he would like to rebalance more often (from every 12 months to every 6 months).
To test this strategy, the investor uses the the following procedure:
- At the end of each year, look back over the previous *12 months* and buy the top *300* stocks as ranked by *12 month* return
- Hold these *300* stocks for *6 months*
- Repeat the sorting procedure and form a new portfolio every *6 months* (aka rebalace every 6 months)


To implement this strategy, pass the *strategy* constructor a slightly modified config file:
```
strategy_ex2 = strategy(example_uni,'./ExampleData/config_Ex2.txt')
```

The config file config_Ex2.txt would look like:
```
name = second example strategy
signalPath = ./ExampleFiles/rolling_returns_12m
rebalanceWindow = 6
rule = 300 
```
Note that the only difference between the config file in example one and this example is that the *rebalanceWindow* parameter was changed from 12 to 6.
The *signal* data and *rule* parameters remain the same as they did in the first example, but an entirely different investment strategy is created.


### Example III: Volatility strategy of bottom 200 stocks with annual rebalancing


After looking at the risk/return metrics and plots for the first two strategies, the investor notices that his returns would be too volatile.
He has the idea that stocks which had low volatility will continue to do so. To test this strategy, the investor uses the the following procedure:
- look back over the previous *12 months* and buy the bottom *200* stocks as ranked by *12 month* volatility
- Hold these *200* stocks for *6 months*
- Repeat the sorting procedure and form a new portfolio every *6 months* (aka rebalace every 6 months)


To implement this volatility strategy, construct a new *strategy* object:
```
strategy_ex3 = strategy(example_uni,'./ExampleData/config_Ex3.txt')
```

The config file config_ex3.txt would look like:
```
name = third example strategy
signalPath = ./ExampleFiles/rolling_volatility_12m
rebalanceWindow = 6
rule = -200 
```
Where *rolling_volatility_12m* is a pickled pandas dataframe containing 12-month rolling standard deviation of returns, as opposed to rolling returns used in the examples above.
Note that for picking the bottom 200 stocks, the *rebalanceWindow* parameter was set to -200 in the config file.



*Although the examples went through the syntax of how someone would use the package, the demo module will simply prompt you to select the
desired universe and config file (which are all located in the /ExampleData directory). We hope that the demo will give you an idea of how someone would use this package to generate and analyze investment strategies defined over
large universes with ease. Feel free to play with the different parameters in the config file and create your own investment strategy!* 


[momentum]: http://faculty.chicagobooth.edu/tobias.moskowitz/research/JF_12021_TMcomments.pdf

## Dependencies

Our project was tested to work using Python 2.7 on both Windows 8 and Ubuntu 15.04 systems. In addition to **portfolioFactory** the following packages are required for basic functionality:

- [NumPy](http://www.numpy.org): 1.7.0+
- [matplotlib](http://matplotlib.sourceforge.net/): for plotting
- [Pandas](http://pandas.pydata.org/): 0.15.1 is required for file loading to work. The update can be done using pip. This update is require if demo is run on the class virtual machine.

	```
	pip install Pandas --upgrade
	```
- [TkInter](http://tkinter.unpythonic.net/wiki/How_to_install_Tkinter): Used for GUI. This package should be built in. 
- [Seaborn](http://stanford.edu/~mwaskom/software/seaborn/): Required for plotting. Using pip, Seaborn can be installed using the following command:

	```
	pip install seaborn
	```
## License
MIT

