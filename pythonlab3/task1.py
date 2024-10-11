
k = int(input("Кол-во стран: "))

countries = {}

for i in range(k):
    data = input(f"{i+1} страна: ").split()
    country = data[0]
    cities = data[1:]
    countries[country] = cities

def find_country(city):
    for country, cities in countries.items():
        if city in cities:
            return country
    return None

# Ввод и проверка трех городов
for i in range(3):
    city = input(f"{i+1} город: ")
    country = find_country(city)
    if country:
        print(f"Город {city} расположен в стране {country}.")
    else:
        print(f"По городу {city} данных нет.")