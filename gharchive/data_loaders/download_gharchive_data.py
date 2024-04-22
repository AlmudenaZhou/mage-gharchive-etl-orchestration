from urllib.request import Request, urlopen


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


import zlib
import json
import pandas as pd


def download_gharchive_data(year, month, day, hour):
    url = f'http://data.gharchive.org/{year}-{month:02d}-{day:02d}-{hour}.json.gz'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    compressed_data = response.read()
    print(f'Downloaded {url}')
    return compressed_data


def compressed_data_to_list_of_dicts(compressed_data):
    decompressed_data = zlib.decompress(compressed_data, 16 + zlib.MAX_WBITS)

    decoded_lines = decompressed_data.decode('utf-8').split('\n')
    decoded_lines = filter(lambda x: x != '', decoded_lines) 

    json_decoded_lines = [json.loads(line) for line in decoded_lines]
    return json_decoded_lines


def convert_to_df(json_decoded_lines):
    df = pd.DataFrame(json_decoded_lines)

    df.created_at = pd.to_datetime(df.created_at)
    return df


@data_loader
def load_data(*args, **kwargs):

    execution_date = kwargs.get('execution_date')
    year = execution_date.year
    month = execution_date.month
    day = execution_date.day
    hour = execution_date.hour - 1

    if hour == -1:
        day -= 1
        hour = 23

    print(year, month, day, hour)

    compressed_data = download_gharchive_data(year, month, day, hour)
    print('Downloaded data')
    json_decoded_lines = compressed_data_to_list_of_dicts(compressed_data)
    print('Converted data to list of dicts')
    df = convert_to_df(json_decoded_lines)
    print('Converted data to pandas DataFrame')
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
