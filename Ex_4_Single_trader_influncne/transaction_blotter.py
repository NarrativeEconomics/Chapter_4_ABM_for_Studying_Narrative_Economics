import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import random



prices_fname = "bse_STAC_min150_i30_0001_tape.csv"
prices_df = pd.read_csv(prices_fname, parse_dates=True)
prices_df.columns = ['index','Sec', 'Transactions']
print(prices_df.head())

prices_df['Sec'] = prices_df['Sec'].astype(int)



prices_df.plot.scatter(x='Sec', y='Transactions')
plt.xlabel('Sec')
plt.ylabel('Price')

plt.show()


prices_df = prices_df.set_index('Sec')
n_hours = 2

smth_prices_df = prices_df.groupby('Sec').mean()
print(smth_prices_df)
smth_prices_df.dropna()
smth_prices_df.plot()
plt.xlabel('Sec')
plt.ylabel('Price')

plt.show()


