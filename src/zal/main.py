import pandas as pd
import funkcje
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("gdp_file")
parser.add_argument("lm_file")
parser.add_argument("co2_file")
args = parser.parse_args()

dane_gdp = funkcje.clear_data(funkcje.get_data(pd.read_csv(args.gdp_file, skiprows=4)))
dane_pop = funkcje.clear_data(funkcje.get_data(pd.read_csv(args.lm_file, skiprows=4)))
dane_co2 = funkcje.clear_data(pd.read_csv(args.co2_file).rename(columns={'Country': 'Country Name'}))
dates = funkcje.find_dates(dane_gdp, dane_pop, dane_co2)

print("Czy chcesz ustalić własne daty? (t/n)")
odp = input()
if(odp == 't'):
    print("Podaj datę od:")
    data_od = int(input())
    print("Podaj datę do:")
    data_do = int(input())
    if(data_od < dates[0] or data_do > dates[1]):
        print("Podane daty są nieprawidłowe")
    else:
        dates = (data_od, data_do)

print("Zadanie 1:")
print(funkcje.ex1(dane_co2, dates))

print("Zadanie 2:")
print(funkcje.ex2(dane_gdp, dane_pop, dates))

odp3 = funkcje.ex3(dane_co2, dates)
print("Najbardziej zwiększyły: \n", odp3[0] )
print("Najbardziej zmniejszyły: \n", odp3[1])
