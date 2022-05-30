import pandas as pd
from models.models import db


def get_dataframe_from_csv(file_path: str):
    quotes = pd.read_csv(file_path, parse_dates=False, delimiter=',', decimal='.')
    # quotes['Report_Date_as_MM_DD_YYYY'] = pd.to_datetime(quotes['Date'], dayfirst=True)
    # quotes = quotes.sort_values(by='Report_Date_as_MM_DD_YYYY')
    # quotes = pd.merge_asof(quotes, cot, on='Report_Date_as_MM_DD_YYYY')
    # quotes_with_commercials = pd.DataFrame()
    # quotes_with_commercials['Ticker'] = quotes['Symbol']
    # quotes_with_commercials['Date'] = quotes['Report_Date_as_MM_DD_YYYY']
    # quotes_with_commercials['Open'] = quotes['Open']
    # quotes_with_commercials['High'] = quotes['High']
    # quotes_with_commercials['Low'] = quotes['Low']
    # quotes_with_commercials['Close'] = quotes['Close']
    # print(quotes)

    return quotes