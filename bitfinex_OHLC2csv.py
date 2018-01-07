import json
import requests
import pandas as pd


def save2csv(pair):
    url = "https://api.bitfinex.com/v2/candles/trade:1D:{0}/hist?limit=1000&sort=-1"

    r = requests.get(url.format(pair))
    df = pd.DataFrame(json.loads(r.text))

    df[0] = pd.to_datetime(df[0].values, unit="ms")

    fname = "csv/bitfinex_{0}.csv".format(pair)
    header = ["Date", "Open", "Close", "High", "Low", "Volume"]
    df.iloc[::-1].to_csv(fname, sep=",", header=header, index=False)


if __name__ == "__main__":
    print("Input Pair Currency codes. ex) tBTCUSD")
    pair = input()
    save2csv(pair)
