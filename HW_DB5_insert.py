import json
from HW_DB5_models import *
from HW_DB5_connect import *
# import os

def load_data(path_to_file):
    with open(path_to_file, 'r', encoding='UTF-8') as f:
        for line in json.load(f):
            model = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale,
            }[line.get('model')]
            session.add(model(id=line.get('pk'), **line.get('fields')))
    session.commit()


if __name__ == '__main__':
    engine, session = connect_to_base(
        base_driver='postgresql',
        login='postgres',
        pwd='postgres',
        # pwd=os.getenv('netology_db_2_password')
        ip='localhost',
        port=5432,
        base_name='netology_db_2',
    )

    delete_tables(engine)
    create_tables(engine)
    load_data('fixtures/tests_data.json')
    session.close()
