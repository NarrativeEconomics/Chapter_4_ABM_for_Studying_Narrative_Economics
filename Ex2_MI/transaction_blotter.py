import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import random



prices_fname = "bse_MI_min150_i05_0001_tape.csv"
prices_df = pd.read_csv(prices_fname, parse_dates=True)
prices_df.columns = ['index','Sec', 'Transactions']


prices_df['Sec'] = prices_df['Sec'].astype(int)

print(prices_df.head())

prices_df.plot.scatter(x='Sec', y='Transactions')
plt.xlabel('Sec')
plt.ylabel('Price')

plt.show()


smth_prices_df = prices_df.groupby('Sec').mean()
print(smth_prices_df)
smth_prices_df.dropna()
smth_prices_df.plot()
plt.xlabel('Sec')
plt.ylabel('Price')

plt.show()


