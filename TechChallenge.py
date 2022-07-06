'''
    Tech Challenge (Data Scientist)               

    Baptiste Chaigneau
'''

'''
    PACKAGES
'''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
from datetime import datetime



'''
    DATA EXPLORATION
'''

    # SALES  
sales = pd.read_csv('sales_data.txt', sep = ',')
sales['DATE'] = pd.to_datetime(sales['DATE'])
sales['DATE'] = sales['DATE'].dt.strftime('%Y-%m-%d')

sales_daily = pd.pivot_table(
    data = sales, 
    values = 'SALES', 
    index = 'DATE', 
    columns = 'ITEM'
    ).reset_index()

print(sales.describe())
print(sales_daily.index.is_unique)

year = pd.DataFrame(
    pd.date_range(start="2019-01-01",end="2019-12-31").strftime('%Y-%m-%d').tolist(), 
    columns = ['DATE']
    )
unique_days = year.query('DATE not in @sales_daily.DATE')
print(unique_days)

'''
Le magasin doit sûrement fermer le dimanche
'''



fig, ax = plt.subplots(figsize = (12,8))
sns.scatterplot(
    data = sales, 
    x = 'DATE', y ='SALES', 
    hue = 'ITEM', 
    style = 'ITEM', 
    s = 100, 
    palette = 'BrBG'
    )
ax.xaxis.set_major_locator(mticker.MaxNLocator(12))
plt.xticks(rotation = 45)
plt.title('Observation of the Sale distribution with Time', fontsize = 20)
plt.show()







    # METEO
towns = [
    'bordeaux', 
    'lille', 
    'lyon', 
    'marseille'
    ]

meteo_corr = pd.DataFrame(columns = ['A', 'B', 'town'])

for idx, t in enumerate(towns) :
    globals()[t] = pd.read_csv('meteo_{}.txt'.format(t), sep = ',', skiprows = 3)    
    result = pd.merge(
        sales_daily, globals()[t], 
        on = 'DATE'
        )  
    corr = result.corr()
    df = pd.DataFrame()
    df['A'] = corr.A
    df['B'] = corr.B
    df['town'] = t
    meteo_corr = meteo_corr.append(df)

meteo_corr = meteo_corr.reset_index()
meteo_corr = meteo_corr[(meteo_corr['index'] != 'A') & (meteo_corr['index'] != 'B')]


var = [
       'A', 'B'
        ]

for v in var : 
    fig, ax = plt.subplots(figsize = (12,8))
    
    sns.scatterplot(
        data = meteo_corr,
        x = 'town', y = '{}'.format(v), hue = 'index',
        s = 150
        )
    ax.legend(bbox_to_anchor=(1.05, 1))
    plt.title(
        'Bivariate correlation between meteorological\nvariables and sales variable according to the town ({})'.format(v),
        fontsize = 24,
        loc = 'left'
        )
    

'''
    Qualitativement, le résultat semble indiquer que le produit des ventes est
    mieux corrélé (ou anticorrélé) avec la météo dans la ville de Bordeaux
'''
















