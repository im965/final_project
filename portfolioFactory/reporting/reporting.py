"""
reporting is a module that contains a collection of functions to make plots for demo.py

Author: Peter Li and Israel Malkin

"""

from ..utils import utils as utils
from ..utils import customExceptions as customExceptions
import portfolioFactory.metrics.riskMetrics as riskMetrics


import matplotlib.pyplot as plt
import seaborn as sns

import portfolioFactory.metrics.retMetrics as retMetrics
import sys

current_palette = sns.color_palette("Blues")

def plotRollingReturn(inputData, windowArray):
    '''Plots a panel of 4 rolling returns and histogram
    
    Note: size fixed to allow for nicer looking graphs
    
    Input:
        - inputData (timeseries): timeseries of monthly returns
        - horizon (list): list of 4 integers for rolling analysis 
    
    '''
        
    # check in windowArray is a list of 4 integers
    listCheck = isinstance(windowArray, list)
    lengthCheck = len(windowArray) == 4
    typeCheck = all([isinstance(x, int) for x in windowArray ])
        
    if all([listCheck, lengthCheck, typeCheck]):
        sns.set_context("paper")
        
        data = utils.processData(inputData)
        
        fig1 = plt.figure(figsize=(16, 8))
        fig1.patch.set_facecolor('white') 
    
        # Create axis for subplots
        ax1 = plt.subplot2grid((4,3), (0,0), colspan = 2)
        ax2 = plt.subplot2grid((4,3), (1,0), colspan = 2)
        ax3 = plt.subplot2grid((4,3), (2,0), colspan = 2)
        ax4 = plt.subplot2grid((4,3), (3,0), colspan = 2)    
            
        ax5 = plt.subplot2grid((4,3), (0,2), colspan = 1)
        ax6 = plt.subplot2grid((4,3), (1,2), colspan = 1)
        ax7 = plt.subplot2grid((4,3), (2,2), colspan = 1)
        ax8 = plt.subplot2grid((4,3), (3,2), colspan = 1)
        
        tsAx = [ax1, ax2, ax3, ax4]
        histAx = [ax5, ax6, ax7, ax8]
        
        # Plot rolling returns and histograms
        for ixWindow in range(4):        
            
            ixColor = current_palette[2+ixWindow]
            retMetrics.rollingReturn(data,windowArray[ixWindow]).plot(ax = tsAx[ixWindow], color = ixColor)
            retMetrics.rollingReturn(data,windowArray[ixWindow]).hist(ax = histAx[ixWindow], bins = 30, color = ixColor)
            tsAx[ixWindow].set_ylabel(str(windowArray[ixWindow]) + ' Months', fontsize = 15)
        
        # remove lables for ts plots
        ax1.set_xlabel('')
        ax2.set_xlabel('')
        ax3.set_xlabel('')
        
        ax1.get_xaxis().set_ticks([])
        ax2.get_xaxis().set_ticks([])
        ax3.get_xaxis().set_ticks([])
        
        # set title
        ax1.set_title('Rolling Returns', fontsize = 15)
        ax5.set_title('Distribution of Rolling Returns', fontsize = 15)        
            
    else: 
        raise customExceptions.invalidInput('Invalid Horizon: Expect list of 4 window values')
        

def plotWithStats(series,startyear,endyear):
    ''' Function to plot cumulative returns including risk metrics as text
        The plot and risk metrics are calculated between startyear-endyear
        
        Arguments:
        -series (series) : a series containing returns
        -staryear(integer): year to begin the plot and analysis
        -endyear (integer): year to end the plot and analysis
    
        Result:
        Shows a matplotlib figure containing cumulative returns and the risk metrics
        
    '''
    
    #limit to years of interest
    try:
        measure = series.truncate(before='01/01/'+str(startyear),after='12/31/'+str(endyear))
        
    except (TypeError, ValueError):
        raise customExceptions.invalidInput('Invalid year specified')
        
    if len(measure)==0:
        raise customExceptions.invalidInput("The series passed does not contain data in the specified interval")
    
    #calculate cumulative returns
    cumulative =  (measure+1).cumprod()
    
    # calculate risk metrics
    metric1 = round(riskMetrics.VaR(measure,12,95),2)
    metric2 = round(riskMetrics.maxDrawdown(measure),2)
    
    
    #plot     
    firstObs = measure.dropna().index[0].year

    text_date = '01/01/'+str(firstObs + 1)
    text_y = 0.65*(cumulative.max())
    
    fig = plt.figure(figsize=(16, 8))
    fig.patch.set_facecolor('white')     
    
    cumulative.plot()
    plt.xlabel('Date', fontsize = 15)
    plt.ylabel('Total Value', fontsize = 15)
    plt.title('Cumulative Returns', fontsize = 15)        
    metric1 = 'Max Drawdown: ' + '{:.1%}'.format(riskMetrics.maxDrawdown(measure))
    metric2 = '95% 1-Year VaR:' + '{:.1%}'.format(riskMetrics.VaR(measure, 12, 95))
    metric3 = 'Annualized Volatility: ' + '{:.1%}'.format(riskMetrics.annualizedVolatility(measure))
    metric4 = 'Cumulative Return: ' + '{:.1%}'.format(retMetrics.cumulativeReturn(measure))
    metric5 = 'Average 6-month Return: ' + '{:.1%}'.format(retMetrics.averageHorizonReturn(measure, 6))
    metric6 = 'Average 12-month Return: ' + '{:.1%}'.format(retMetrics.averageHorizonReturn(measure, 12))
    metric7 = 'Average 36-month Return: ' + '{:.1%}'.format(retMetrics.averageHorizonReturn(measure, 36))

    riskText = (metric3 + '\n' + metric1 + '\n' + metric2)
    returnsText = (metric4 + '\n' + metric5 + '\n' + metric6 + '\n' + metric7)             
    
    plt.text(text_date, text_y, riskText + '\n\n\n' + returnsText,fontsize=15)

    plt.show(block = False)
    
    return

def getUserPlottingParameters():
    ''' Method to get user input for demo plotting
    
    This method will prompt the user fof the following input:

        - Start Year (int): start year for cum. ret. plot
        - End Year (int): end year for cum. ret. plot 
        - Rolling Analysis Window (list for 4 ints): windows sizes for rolling analysis
    
    '''
    
    inputCheck = False  
    maxWindow = 72 # Maximum roling window size i.e. 5 years
    minYear = 1991
    maxYear = 2014
    
    while inputCheck == False:
    
        print 'For plotting, please supply the following input: '
    
        try:
            startYear = input('Start Year (min 1991): ')
            
            # Check start year is an int
            if not isinstance(startYear, int):
                
                raise Exception  
                
            # Check end year is an interger
            endYear = input('End Year (max 2014): ')
            
            if not isinstance(endYear, int) or endYear < startYear:
                
                raise Exception  
            
            # Check start year is in range                
            if not minYear <= startYear <= maxYear:
                
                raise Exception
                
            # check end year is in range
            if not (startYear < endYear <= maxYear):
                
                raise Exception
            
            windowInput= input('Rolling Analysis Window (list of 4 int for window size e.g. [3,6,12,24], max window = 72): ')
            
            # check input is list
            if not isinstance(windowInput, list):
                
                raise Exception
            # check list entries are int
            if not all([isinstance(x, int) for x in windowInput]):
                
                raise Exception
            # check window within bound
            if max(windowInput) > maxWindow:
                
                raise Exception 
            
            # pass
            inputCheck = True
            
        except KeyboardInterrupt:
            
            print 'Keybout Interrupt'
            sys.exit()
                
        except:
            
            print 'Invalid Input - try again'
            inputCheck = False
                
    return startYear, endYear, windowInput
            
def main():
    pass

if __name__ == "__main__":
    main()    
    