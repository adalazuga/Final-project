import pandas as pd
import pycountry

def find_dates(gdp_file, pop_file, co2_file): #szuka lat wspolnych we wszystkich tabelach
    gdp_first = min(gdp_file['Year'])
    gdp_last = max(gdp_file['Year'])
    pop_first = min(pop_file['Year'])
    pop_last = max(pop_file['Year'])
    co2_first = min(co2_file['Year'])
    co2_last = max(co2_file['Year'])
    return max(gdp_first, pop_first, co2_first), min(gdp_last, pop_last, co2_last)

def set_dates(data, dates): #bierze dane w latach date1-date2
    data = data[data['Year'] >= dates[0]]
    data = data[data['Year'] <= dates[1]]
    return data

def clear_data(data): #sprawdza nazwy krajów, jak nie są w spisie to usuwa
    for i in range(len(data['Country Name'])):
        if(pycountry.countries.get(name = data['Country Name'][i])  == None): #jeżeli nazwy nie ma to sprawdzamy dalej
                split_name = data['Country Name'][i].split(',')[0]
                country = pycountry.countries.get(name = split_name)
                if (country == None):
                    split_name = data['Country Name'][i].split(' ')[0]
                    country = pycountry.countries.get(name=split_name)
                    if(country != None):
                        x = data['Country Name'][i]
                        y = str(country.name).upper()
                        data['Country Name'] = data['Country Name'].replace([x], y)
                    else:
                        data = data.drop(i)
    return data.reset_index(drop=True).dropna()

def get_data(data): #bierze dane z tabeli przestawnej i zmienia w normalną tabelę
    countries = []
    year = []
    value = []
    years = data.columns[4:-1]
    for i in years:
        for country in range(len(data['Country Name'])):
            country_name = data['Country Name'][country]
            countries.append(country_name)
            year.append(int(i))
            value.append(data[i][country])
    df = pd.DataFrame({'Country Name': countries, 'Year': year, 'Values' : value})
    return df

def ex1(dane, dates): #zadanie 1
    dane = set_dates(dane, dates)
    return dane.groupby('Year').apply(lambda dane: dane.nlargest(5, 'Per Capita'))[['Country Name', 'Per Capita', 'Total']]

def ex2(dane_gdp, dane_pop, dates): #zadanie 2
    df = dane_pop.merge(dane_gdp, on=['Country Name', 'Year'])
    df = df.rename(columns={'Values_x': 'pop', 'Values_y': 'gdp'})
    df = set_dates(df, dates)
    df['Per Capita'] = df['gdp'] / df['pop']
    return df.groupby('Year').apply(lambda dane: dane.nlargest(5, 'Per Capita'))[['Country Name', 'Per Capita', 'gdp']]

def ex3(dane, dates): #zadanie 3
    dane = set_dates(dane, dates)
    df = pd.pivot_table(dane, values = 'Total', index='Country Name', columns='Year')
    odp = []
    df['Odp'] = df[2014] - df[2004]
    return df['Odp'].nlargest(5), df['Odp'].nsmallest(5)


