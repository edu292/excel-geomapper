import pandas as pd
import requests
from dotenv import load_dotenv
import os
from time import sleep
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

load_dotenv()
TOKEN = os.getenv('TOKEN')

base_path = 'https://us1.locationiq.com/v1/search'
retry_strategy = Retry(total=3, status_forcelist=[429, 500], backoff_factor=0.7)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.session()
session.mount('https://', adapter)


def get_geoloc(address):
    params = address
    params['key'] = TOKEN
    params['format'] = 'json'

    response = session.get(base_path, params=params, timeout=10)
    data = response.json()
    if isinstance(data, list) and data:
        return data[0]['lat'], data[0]['lon']

    return None, None


def get_geocoded_df(df, column_names, fixed):
    geocoded_df = pd.DataFrame(columns=['date', 'address', 'info', 'lat', 'long'])
    for _, row in df.iterrows():
        address = fixed.copy()
        if pd.isna(row[column_names['address']]):
            continue
        address['street'] = row[column_names['address']]
        if 'city' in column_names:
            address['city'] = row[column_names['city']]
        if 'state' in column_names:
            address['state'] = row[column_names['state']]
        if 'country' in column_names:
            address['country'] = row[column_names['country']]
        lat, long = get_geoloc(address)
        sleep(0.7)
        new_row = {
            "date": row[column_names['date']],
            "address": address['street'],
            "info": row[column_names['info']],
            "lat": float(lat) if lat is not None else None,
            "long": float(long) if lat is not None else None
        }
        geocoded_df.loc[len(geocoded_df)] = new_row
    return geocoded_df