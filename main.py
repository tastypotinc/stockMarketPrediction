#Program runs under Python 3
#Packages requirements: TA-Lib, scikit-learn, pandas, matplotlib, numpy

from data import getStock_A, getStock_C
from featureGeneration import addFeatures
from machineLearning import Classify
from preprocess import Prep
from CV import CV
from performance import Portfolio, MarketIntradayPortfolio
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from pylab import *
from datetime import datetime

HS300 = getStock_C('000300')
SP500 = getStock_A('^GSPC')
HS300 = addFeatures(HS300)
SP500 = addFeatures(SP500)
HS300.drop('ADOSC', axis=1)
X_train, y_train, X_test, y_test = Prep(HS300)
Classify(X_train, y_train, X_test, y_test, 'RF')
CV(X_train, y_train, 9, 'RF')
clf = LDA()
y_pred = clf.fit(X_train, y_train).predict(X_test)
symbol = 'CSI300'
start_test = datetime(2014,1,1)
end_period = datetime(2015,9,29)
bars = HS300[['Open','AdjClose']]

bars = bars[start_test:end_period]

signals = pd.DataFrame(index=bars.index)
signals['signal'] = 0.0
signals['signal'] = y_pred
#Short the stock
signals.signal[signals.signal == 0] = -1

# positions change
signals['positions'] = signals['signal'].diff()

pf = MarketIntradayPortfolio(symbol, bars, signals)

returns = pf.backtest_portfolio()

# Plot results
f, ax = plt.subplots(2, sharex=True)
f.patch.set_facecolor('white')
ylabel = symbol + ' Close Price in RMB'
bars['AdjClose'].plot(ax=ax[0], color='r', lw=3.)    
ax[0].set_ylabel(ylabel, fontsize=18)
ax[0].set_xlabel('', fontsize=18)
ax[0].set_ylim([0,6000])
ax[0].legend(('Close Price of CSI300',), loc='upper left', prop={"size":18})
ax[0].set_title('CSI300 Close Price VS Portofolio Performance (1 January 2014 - 29 September 2015)', fontsize=20, fontweight="bold")
returns['total'].plot(ax=ax[1], color='b', lw=3.)  
ax[1].set_ylabel('Portfolio value in RMB', fontsize=18)
ax[1].set_xlabel('Date', fontsize=18)
ax[1].legend(('Portofolio Performance. Capital Invested: 100k RMB. Shares Traded per day: 500+500',), loc='upper left', prop={"size":18})            
plt.tick_params(axis='both', which='major', labelsize=14)
loc = ax[1].xaxis.get_major_locator()
loc.maxticks[DAILY] = 24
plt.show()
