import pandas as pd
import re


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


@transformer
def transform(data, *args, **kwargs):
    passenger_count_is_zero = data['passenger_count'].isin([0]).sum()
    print(f'INFO: The number of trips without passengers is {passenger_count_is_zero}')

    # Remove rows where the passenger count is equal to 0 and the trip distance is equal to zero.
    data = data[data['passenger_count'] > 0]

    # Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
    data['lpep_pickup_date'] = pd.to_datetime(data['lpep_pickup_datetime'], unit='ms').dt.date

    # Rename columns in Camel Case to Snake Case
    data.columns = [camel_to_snake(col) for col in data.columns]
    
    return data

@test
def test_vendor_ids(output, *args) -> None:
    assert output['vendor_id'].isin([1, 2]).all()


@test
def test_passenger_count(output, *args) -> None:
    assert output['passenger_count'].isin([0]).sum() == 0