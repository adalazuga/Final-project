import pandas as pd
import pytest
import funkcje

dane_co2 = funkcje.clear_data(pd.read_csv("../dane_co2.csv").rename(columns={'Country': 'Country Name'}))
@pytest.mark.parametrize("data", [dane_co2])
def test_take_one_data(data):
    with pytest.raises(TypeError):
        funkcje.find_dates(data)

@pytest.mark.parametrize("data", [dane_co2])
def test_take_non_pivot_table_data(data):
    with pytest.raises(AttributeError):
        funkcje.get_data(data)

@pytest.mark.parametrize("data, dates", [(dane_co2, 1980)])
def test_take_int_not_tuple(data, dates):
    with pytest.raises(TypeError):
        funkcje.get_data(data, dates)
