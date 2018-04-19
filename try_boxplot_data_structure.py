import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('digital_currency.db')
cur = conn.cursor()
statement = '''select spot_price, month
           from Coinbase
           where year=2017
           
               '''
result = cur.execute(statement)
conn.commit()
boxplot = result.fetchall()
conn.close()



df_box_plot = pd.DataFrame(boxplot, columns=['spot_price', 'month'])
print(df_box_plot.head)
df_box_plot.boxplot(column='4',by='6')
# plt.savefig("boxplot.png")
plt.show()