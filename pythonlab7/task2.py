import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = 'pythonlab7/vg_sale1.csv'

df = pd.read_csv(CSV_PATH)

df_unique = df.drop_duplicates(subset=['Name', 'Year'])

# 1. Популярность жанров до и после 2000 года
fig, axs = plt.subplots(2, 2, figsize=(20, 20))
fig.suptitle('Популярность жанров до и после 2000 года', fontsize=16)

# По количеству выпущенных игр
before_2000 = df_unique[df_unique['Year'] < 2000]['Genre'].value_counts()
after_2000 = df_unique[df_unique['Year'] >= 2000]['Genre'].value_counts()

before_2000.plot(kind='bar', ax=axs[0, 0])
axs[0, 0].set_title('Количество игр до 2000 года')
axs[0, 0].set_xlabel('Жанр')
axs[0, 0].set_ylabel('Количество игр')
axs[0, 0].tick_params(axis='x', rotation=45)

after_2000.plot(kind='bar', ax=axs[0, 1])
axs[0, 1].set_title('Количество игр после 2000 года')
axs[0, 1].set_xlabel('Жанр')
axs[0, 1].set_ylabel('Количество игр')
axs[0, 1].tick_params(axis='x', rotation=45)

# По объему продаж
before_2000_sales = df_unique[df_unique['Year'] < 2000].groupby('Genre')['Global_Sales'].sum()
after_2000_sales = df_unique[df_unique['Year'] >= 2000].groupby('Genre')['Global_Sales'].sum()

before_2000_sales.plot(kind='bar', ax=axs[1, 0])
axs[1, 0].set_title('Объем продаж до 2000 года')
axs[1, 0].set_xlabel('Жанр')
axs[1, 0].set_ylabel('Объем продаж (млн)')
axs[1, 0].tick_params(axis='x', rotation=45)

after_2000_sales.plot(kind='bar', ax=axs[1, 1])
axs[1, 1].set_title('Объем продаж после 2000 года')
axs[1, 1].set_xlabel('Жанр')
axs[1, 1].set_ylabel('Объем продаж (млн)')
axs[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# 2 Общее число видеоигр по годам
games_per_year = df_unique['Year'].value_counts().sort_index()

plt.figure(figsize=(12, 6))
games_per_year.plot()
plt.title('Количество выпущенных видеоигр по годам')
plt.xlabel('Год')
plt.ylabel('Количество игр')
plt.show()

# 3 Топ3 издателя и их игры по платформам
top_publishers = df_unique['Publisher'].value_counts().nlargest(3).index

publisher_platform = df_unique[df_unique['Publisher'].isin(top_publishers)].groupby(['Publisher', 'Platform']).size().unstack()

#plt.figure(figsize=(12, 6))
publisher_platform.plot(kind='bar', stacked=True)
plt.title('Количество игр по платформам для топ-3 издателей')
plt.xlabel('Издатель')
plt.ylabel('Количество игр')
plt.legend(title='Платформа', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 4. Доли продаж по регионам
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
fig.suptitle('Доли продаж по регионам', fontsize=16)

def plot_sales_pie(data, ax, title):
    sales = data[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
    ax.pie(sales, labels=['Северная Америка', 'Европа', 'Япония', 'Другие'], autopct='%1.1f%%')
    ax.set_title(title)

before_2000 = df_unique[df_unique['Year'] < 2000]
plot_sales_pie(before_2000, ax1, 'До 2000 года')

after_2000 = df_unique[df_unique['Year'] >= 2000]
plot_sales_pie(after_2000, ax2, 'С 2000 года')

plt.tight_layout()
plt.show()
