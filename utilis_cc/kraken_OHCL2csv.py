import json
import requests
import pandas as pd


def save2csv(pair):

    url = "https://api.kraken.com/0/public/OHLC?pair={0}&interval=1440"
    r = requests.get(url.format(pair))

    df = pd.DataFrame(json.loads(r.text)["result"][pair])

    df[[0]] = pd.to_datetime(df[[0]][0].values, unit="s")

    fname = "csv/kraken_{0}.csv".format(pair)
    header = ["Date", "Open", "High", "Low", "Close", "VWAP", "Volume", "Count"]
    df.to_csv(fname, sep=",", header=header, index=False)


if __name__ == "__main__":
    print("Input Pair Currency codes. ex) XXBTZEUR")
    pair = input()
    save2csv(pair)
