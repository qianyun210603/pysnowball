from pandas import Timestamp, DataFrame, concat, to_datetime
from .api_ref import kline_base
from .utls import fetch

BAR_MULTI = {
    "1d": 1,
    "1m": 360,
    "5m": 75,
    "15m": 25,
}


def historical_kline(
    symbol: str,
    start: Timestamp,
    end: Timestamp,
    period: str,
    type: str = "before",
    batch: int = 100
):
    start_epoch = int(start.timestamp() * 1000)
    end_epoch = int(end.timestamp() * 1000)
    estimated_bar_num = ((end - start).days + 1) * BAR_MULTI[period]
    all_dfs = []
    while True:
        query = f"&symbol={symbol}&begin={start_epoch}&period={period}&type={type}&count={min(batch, estimated_bar_num)}"
        url = kline_base + query
        raw = fetch(url)
        df_tmp = DataFrame(raw['item'], columns=raw['column'])
        start_epoch = df_tmp.timestamp.max()
        estimated_bar_num -= len(df_tmp)
        all_dfs.append(df_tmp)
        if start_epoch > end_epoch:
            break

    df = concat(all_dfs)
    df.timestamp = to_datetime(df.timestamp)
    df.set_index("timestamp", inplace=True)

    return df
