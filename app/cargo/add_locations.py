import pandas as pd
from .models import Location


def load_locations():
    df = pd.read_csv('uszips.csv')
    for i, j in df.iterrows():
        print(i, j)
