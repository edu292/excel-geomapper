import pandas as pd
import sqlite3
from enum import Enum, auto

def detect_header_row(excel_file, max_rows_to_check=10):
    raw_df = pd.read_excel(excel_file, header=None)

    for i in range(max_rows_to_check):
        row = raw_df.iloc[i]
        if row.isnull().all():
            continue

        if row.apply(lambda x: isinstance(x, str)).any():
            return i

    return 0


def save_markers(df: pd.DataFrame):
    with sqlite3.connect('geoloc.db') as conn:
        df.to_sql('geoloc', conn, if_exists='append', index=False)


class AppState(Enum):
    UPLOADING = auto()
    GEOCODING = auto()
    PREVIEW = auto()
    CREATING_MAP = auto()