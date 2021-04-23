from pysnowball import api_ref
from pysnowball import utls
from pandas import DataFrame, Timestamp
from urllib.parse import urljoin


def finance_report(
        start: Timestamp, end: Timestamp, market: str, symbol: str, report_type: str, quarter="all"
) -> DataFrame:
    """

    :param start: start time
    :param end: end time
    :param market: {'HK', 'CN'}
    :param symbol: stock symbol
    :param report_type: {'indicator', 'balance', 'income', 'business'}
    :param quarter: {'all', 'Q1', 'Q2', ‘Q3', 'Q4'}
    :return: data frame contains items of financial report
    """
    count = (end.to_period(freq='Q') - start.to_period(freq='Q')).n
    end_timestamp = int(end.timestamp()*1000)
    urlpath = f"{market}/{report_type}.json?symbol={symbol}&&type={quarter}" \
              f"&is_detail=true&count={count}&timestamp={end_timestamp}"
    url = urljoin(api_ref.finance_base, urlpath)
    data = utls.fetch(url)
    data_list = data.pop('list')
    for d in data_list:
        for k in d:
            if isinstance(d[k], list):
                d[k] = d[k][0]
    df = DataFrame(data_list).drop(columns=['ctime']).rename(columns={'report_date': 'date'}).set_index('date')
    df.date = df.date.astype('M8[ms]')
    df.report_name = df.report_name.str.replace('年报', 'Q4').str.replace('三季报', 'Q3')\
        .str.replace('中报', 'Q2').str.replace('一季报', 'Q1')
    return df
