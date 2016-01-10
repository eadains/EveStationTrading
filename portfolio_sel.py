from portfolio.portfolio import calc_scores
from sqlalchemy import create_engine
import pandas as pd
from functools import partial
from multiprocessing.pool import Pool
from config.config import SQL_USER, SQL_PASS


def main():
    SQL_DATABASE = 'EveMarketData'
    engine = create_engine('mysql+mysqlconnector://%s:%s@localhost/%s' % (SQL_USER, SQL_PASS, SQL_DATABASE))
    item_id_list = [int(index) for (index, row) in pd.read_sql_table('items', engine, index_col='item_id').iterrows()]
    data_write = partial(calc_scores(), SQL_USER, SQL_PASS, SQL_DATABASE)
    p = Pool(4)
    p.map(data_write, item_id_list)

if __name__ == '__main__':
    main()