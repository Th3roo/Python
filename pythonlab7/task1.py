import pandas as pd

CSV_PATH = 'pythonlab7/FIFA.csv'

df = pd.read_csv(CSV_PATH)

# 1
matches_per_year = df.groupby('Year').size()
print("Количество матчей на каждом чемпионате мира:")
print(matches_per_year)

# 2
wc_2014 = df[df['Year'] == 2014][['Datetime', 'City']]
print("\nМатчи чемпионата мира 2014:")
print(wc_2014)

# 3
df['goals'] = df['Home.Team.Goals'] + df['Away.Team.Goals']
match_info = df[['Datetime', 'Home.Team.Name', 'Away.Team.Name', 'goals']]
print("\nИнформация о матчах:")
print(match_info)

# 4
goals_stats = df.groupby('Year').agg({
    'goals': ['sum', 'min', 'max']
})
print("\nСтатистика голов по чемпионатам:")
print(goals_stats)

# 5
matches_per_stadium = df.groupby(['City', 'Stadium']).size().reset_index(name='Matches')
print("\nКоличество матчей на каждом стадионе:")
print(matches_per_stadium)

# 6
avg_goals_per_match = df.groupby('Year')['goals'].mean()
print("\nСреднее количество голов за матч на каждом ЧМ:")
print(avg_goals_per_match)

# 7
high_scoring_years = goals_stats[goals_stats[('goals', 'sum')] > 150]
print("\nГоды с более чем 150 забитыми голами:")
print(high_scoring_years[('goals', 'sum')])