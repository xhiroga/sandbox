import json
import requests
import pandas as pd
# import pdb


def save2csv(pair):

    url = "https://poloniex.com/public?command=returnChartData&currencyPair={0}&start=0&end=9999999999&period=86400"
    r = requests.get(url.format(pair))

    df = pd.DataFrame(json.loads(r.text))
    df = df[["date","high","low","open","close","volume","quoteVolume","weightedAverage"]]

    df["date"] = pd.to_datetime(df["date"].values, unit="s")

    fname = "csv/poloniex_{0}.csv".format(pair)
    df.to_csv(fname, sep=",", index=False)


if __name__ == "__main__":
    # pdb.set_trace()
    print("Input Pair Currency codes. ex) BTC_XMR")
    pair = input()
    save2csv(pair)
