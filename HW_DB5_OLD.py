import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import json
from datetime import datetime
# import os


# Задание 1
base_driver = 'postgresql'
login = 'postgres'
pwd = 'postgres'
# pwd = os.getenv('netology_db_2_password')
ip = 'localhost'
port = 5432
base_name = 'netology_db_2'

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="books")


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    book = relationship(Book, backref="stocks")
    shop = relationship(Shop, backref="shops")


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship(Stock, backref="sales")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


DSN = f"{base_driver}://{login}:{pwd}@{ip}:{port}/{base_name}"
engine = sq.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


# Задание 3
with open('fixtures/tests_data.json', 'r', encoding='UTF-8') as f:
    for line in json.load(f):
        #Делал сам
        # fields = line['fields']
        # if line['model'] == 'publisher':
        #     session.add(Publisher(id=line['pk'], name=fields['name']))
        # elif line['model'] == 'book':
        #     session.add(Book(id=line['pk'], title=fields['title'], id_publisher=fields['id_publisher']))
        # elif line['model'] == 'shop':
        #     session.add(Shop(id=line['pk'], name=fields['name']))
        # elif line['model'] == 'stock':
        #     session.add(Stock(id=line['pk'], id_shop=fields['id_shop'], id_book=fields['id_book'], count=fields['count']))
        # elif line['model'] == 'sale':
        #     session.add(Sale(id=line['pk'], price=fields['price'], date_sale=fields['date_sale'], count=fields['count'], id_stock=fields['id_stock']))
        # else:
        #     print('Неверная запись в строке')

        #Скорректировал готовый шаблон
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[line.get('model')]
        session.add(model(id=line.get('pk'), **line.get('fields')))

session.commit()


# Задание 2
val = input('Введите ID Издателя или его имя: ')
try:
    fltr = Publisher.id == int(val)
except ValueError:
    fltr = Publisher.name.ilike(f'%{val}%')

for row in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale, Sale.count).join(Publisher).join(Stock).join(Shop).join(Sale).filter(fltr).all():
    book_title, shop_name, sale_price, sale_date, sale_count = row
    print(f'{book_title:<40} | {shop_name:^10} | {sale_price * sale_count:^8g} | {datetime.date(sale_date)}')

session.close()
