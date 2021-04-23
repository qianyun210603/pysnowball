from pysnowball import api_ref
from pysnowball import utls
import numpy as np
import numpy.random as nr
from pandas import DataFrame
import time


def population_by_market(market: str, batch_size: int = 1000) -> DataFrame:
    """

    :param market: {'HK', 'CN'}
    :param batch_size: size of one batch
    :return: dataframe contains all population
    """
    url = api_ref.population_base + "?page=1&size={}&order=asc&order_by=symbol&market={}&type={}".format(
        batch_size, market, market.lower()
    )

    res = utls.fetch(url)

    total_count = res['count']
    data: list = res['list']

    # noinspection PyTypeChecker
    time.sleep(np.clip(nr.normal(1, 0.02), 0.9, 1.1))

    for page in range(2, (total_count-1)//batch_size+2):
        url = api_ref.population_base + "?page={}&size={}&order=asc&order_by=symbol&market={}&type={}".format(
            page, batch_size, market, market.lower()
        )

        res = utls.fetch(url)
        this_count = res.get('count', 0)
        if this_count != total_count:
            raise RuntimeWarning(
                f"Get record number ({this_count}) from page {page}, which is different from first page ({total_count})"
            )

        this_list = res.get('list', [])
        if not this_list:
            raise RuntimeWarning("empty page, seemingly missing data")

        data.extend(this_list)
        # noinspection PyTypeChecker
        time.sleep(np.clip(nr.normal(1, 0.02), 0.9, 1.1))

    return DataFrame(data).set_index('symbol')
