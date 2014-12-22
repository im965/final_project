
# portfolioFactory: a simple Python package to build cross-sectional equity portfolios

## What is it

**portfolioFactory** is a Python package that streamlines the process for constructing asset pricing factors.
Built on top of **Pandas**, this package builds portfolios based on user supplied signals and trading rules.
See strategy class and demo for more details.

## Dependencies
- [NumPy](http://www.numpy.org): 1.7.0 or higher
- [SciPy](http://www.scipy.org): miscellaneous statistical functions
- [matplotlib](http://matplotlib.sourceforge.net/): for plotting
- [Pandas](http://pandas.pydata.org/): 0.15.1
- [TkInter](http://tkinter.unpythonic.net/wiki/How_to_install_Tkinter): Used for GUI. This package should be built in. 
- [Seaborn](http://stanford.edu/~mwaskom/software/seaborn/): Required for plotting.

## License
MIT

## Background

This package arose out of a need for a simple framework for creating factors used in asset pricing. In the field of empirical finance,
many pricing factors can be created using similar methodology. However, there does not exist (to our best knowledge) a standard software framework for building these objects. As a result, work is duplicated across teams in academia and industry as researchers create similar platforms on an ad hoc basis. **portfolioFactory** was created to standardize this process. 
