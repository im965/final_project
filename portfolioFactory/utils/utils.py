"""
utils contains general purpose functions used throughout portfolioFactory

Author: Peter Li and Israel Malkin
"""

import numpy as np
import pandas as pd
from . import customExceptions


def processData(data):
    """ Function to process timeseries data
    
    processData performs 2 steps:
        - check if data is numeric, monthly with no missing values (NaN in the middle)
        - drop leading and trailng NaN
    
    Args:
        - data (Pandas time series): monthly timeseries
    
    Returns:
        Trimmed time series        
        
    """    
    
    # check if there are any NaN values in the middle
    
    tempData = data.dropna()
    
    # check if monthly    
    if checkSeqentialMonthly(tempData.index):
        
        # check values are numeric
        if all([isinstance(x,(float, int, long)) for x in tempData.values]):

            return tempData
            
        else:
            
            raise customExceptions.badData('non-numeric data found')
    else:
        
        raise customExceptions.badData('missing data found')

def checkSeqentialMonthly(index):
    """ Function to check if dates for data timeseries are sequential
    
    Args:
        - data (Pandas time series): timeseries index
    
    Returns:
        True / False
        
    """    
    
    # Array of Months and Years
    months = index.month
    years = index.year
    
    # Difference in months % 12 -- this value should always be 1
    monthsDiff = np.mod(months[1:]-months[0:-1],12)
    
    # If months are sequential    
    if all(monthsDiff == 1):
        yearsDiff = years[1:] - years[0:-1]
        ix = np.where(yearsDiff == 1)
        
        # If years are sequential
        if all(months[ix] == 12):      
            return True        
        else:        
            return False        


def setParameters(configPath):
    """ Function to read config file
    
    Note:
        configPath is assumed to be a .txt file with (at least) the following fields:
          - name : a name/description for the strategy
          - signalPath: signal data location 
          - rule: the cutoff point for selecting investment (positive/negative int-->pick top/bottom S investments)
          - window: time-span between rebalancing

    
    Args:
        configPath (str): location of config file
      
    Returns:
        A dict with {key = parameter name: value = parameter value} 
        
    """
    
    # Load Parameters Data
        
    if configPath[-3:] != 'txt':    
        
        raise customExceptions.invalidParameterPath('configPath must be a .txt file')
        
    try:
        parameters = pd.read_table(configPath , sep = '=', index_col = 0, header = None)
    except [ValueError, IOError]:
        raise customExceptions.invalidParameterPath(configPath)
        
    parameters.columns = ['values']        
    
    # Strip spaces
    parameters = parameters.astype('string')        
    parameters.index = parameters.index.map(str.strip)        
    parameters = parameters['values'].map(str.strip)
    
    return parameters.to_dict()
    
def calcRollingReturns(df,window):
    ''' Function to calculate window-size rolling returns
    
        Note: assumes returns are in decimal form (ex. 0.02 represents 2%)
    
        Arguments:
        - df (dataframe) : returns matrix (tickers as columns)
        - window (int) : specifies size of rolling window
        
        Returns
        - pandas dataframe with rolling returns
    '''
    #ensure parameters are specified correctly
    if type(df)!=pd.DataFrame:
        raise customExceptions.notDFError
    
    if type(window)!=int:
        raise customExceptions.windowNotInt
    
    if window<1:
        raise customExceptions.windowNegative
    
    return (pd.rolling_apply(1+df,window=window,func=np.prod,min_periods=window) - 1)
      



