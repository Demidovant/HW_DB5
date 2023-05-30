from HW_DB5_models import *
from HW_DB5_connect import *
# import os

def get_shops(val):
    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale, Sale.count). \
        select_from(Shop). \
        join(Stock). \
        join(Book). \
        join(Publisher). \
        join(Sale)

    if val.isdigit():
        items = q.filter(Publisher.id == int(val)).all()
    else:
        items = q.filter(Publisher.name.ilike(f'%{val}%')).all()

    for book_title, shop_name, sale_price, sale_date, sale_count in items:
        print(f"{book_title:<40} | {shop_name:^10} | {sale_price * sale_count:^8g} | {sale_date.strftime('%d-%m-%Y')}")


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

    val = input('Введите ID Издателя или его имя: ')
    get_shops(val)
    session.close()
