from portfolio.portfolio import init_function, calc_scores
from sqlalchemy import create_engine
import pandas as pd
from functools import partial
from multiprocessing import Pool, Queue
from config.config import SQL_USER, SQL_PASS, SQL_DATABASE


def main():
    SQL_DATABASE = 'EveMarketData'
    wallet = 2500000000
    broker_fee = .008
    sales_tax = .0075
    dataframe = pd.DataFrame()
    engine = create_engine('mysql+mysqlconnector://%s:%s@localhost/%s' % (SQL_USER, SQL_PASS, SQL_DATABASE))
    item_id_list = [int(index) for (index, row) in pd.read_sql_table('items', engine, index_col='item_id').iterrows()]
    data_write = partial(calc_scores, wallet, broker_fee, sales_tax)
    p = Pool(initializer=init_function, initargs=(SQL_USER, SQL_PASS, SQL_DATABASE))
    result = p.map(data_write, item_id_list)
    dataframe = dataframe.append(result).sort_values('profit_factor', ascending=False)
    print dataframe.head(n=20)

if __name__ == '__main__':
    main()
