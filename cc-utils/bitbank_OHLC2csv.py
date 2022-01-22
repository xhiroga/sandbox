from datetime import date
import json
import requests
import pandas as pd


def save2csv(pair):
    start_year = 2011
    url = "https://public.bitbank.cc/{0}/candlestick/1day/{1}"

    df = pd.DataFrame()
    for year in range(start_year, date.today().year):
        r = requests.get(url.format(pair, year))
        df_tmp = pd.DataFrame(json.loads(r.text)["data"]["candlestick"][0]["ohlcv"])

        df_tmp[5] = pd.to_datetime(df_tmp[5].values, unit="ms")
        df = df.append(df_tmp)

    fname = "csv/bitbank_{0}.csv".format(pair)
    header = ["Open", "High", "Low", "Close", "Volume", "Date"]
    df.to_csv(fname, sep=",", header=header, index=False)


if __name__ == "__main__":
    print("Input Pair Currency codes. ex) btc_jpy")
    pair = input()
    save2csv(pair)
