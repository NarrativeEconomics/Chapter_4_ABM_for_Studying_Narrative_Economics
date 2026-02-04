import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import random



prices_fname = "bse_OPRDE_NPN_d150_i05_0013_transactions.csv"
prices_df = pd.read_csv(prices_fname, parse_dates=True)
prices_df.columns = ['index','Day', 'Transactions']
prices_df['Day'] = prices_df['Day'].apply(lambda x: float(x) / (60 *60 *24)).map(int)








smth_prices_df = prices_df.groupby('Day').mean()
print(smth_prices_df)
smth_prices_df.dropna()
smth_prices_df.plot()
plt.xlabel('Day')
plt.ylabel('Price')

plt.show()


prices_df.plot.scatter(x='Day', y=smth_prices_df['Transactions'])
plt.xlabel('Day')
plt.ylabel('Price')

plt.show()