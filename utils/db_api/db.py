import datetime

from sqlalchemy import and_, create_engine, distinct, func,update
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer,String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer)
    name = Column(String)
    tel_number = Column(String)
    adress = Column(String)

    def __init__(self,uid, name, tel_number,adress=''):
        self.uid = uid
        self.name = name
        self.tel_number = tel_number
        self.adress = adress

class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    category = Column(String)
    description = Column(String)
    img_name = Column(String)
    price = Column(Integer)  

    def __init__(self, name,category, description, img_name, price):
        self.name = name
        self.category = category
        self.description = description
        self.img_name = img_name
        self.price = price    

class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    product_id = Column(Integer,ForeignKey('products.id'))

    def __init__(self,user_id,product_id):
        self.user_id = user_id
        self.product_id = product_id

class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    adress = Column(String)
    product_name = Column(String)
    price = Column(Integer)
    date = Column(String)
    time = Column(String)
    status = Column(String)

    def __init__(self,username,adress,product_name,price,date,time,status='Оплачен'):
        self.username = username
        self.adress = adress
        self.product_name = product_name
        self.price = price
        self.date = date
        self.time = time
        self.status = status


engine = create_engine('sqlite:///.\db.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

def create_db():
    Base.metadata.create_all(engine)

def register_user(uid, name, tel_number):
    request = User(uid, name, tel_number)
    session.add(request)
    session.commit()

def show_all_users():
    request = session.query(User).all()
    text = ''
    for row in request:
        text += f'{row.name} | {row.tel_number}\n'

    return text

def check_user_registration(row_uid:int):
    try:
        request = session.query(User.uid)
        uid = int(request[0][0])

        if row_uid == uid: 
            return True
        else:
            return False
    except:
        return False
    
def add_position_to_db(kwargs):

    request = Products(**kwargs)
    session.add(request)
    session.commit()

def show_all_position():
    text = ' НАЗВАНИЕ | ЦЕНА\n'
    request = session.query(Products).order_by(Products.category).all()
    for raw in request:
        text = text + f'{raw.name} | {raw.price} UAH \n'

    return text

def get_item(id):
    request = session.query(Products).filter(Products.id==id).first()
    return request

def get_order_sort(date,time):
    request = session.query(Orders).filter(and_(Orders.date==date,Orders.time==time)).group_by(Orders.product_name).all()
    return request

def _show_list_category() -> tuple:
    request = session.query(Products.category).distinct(Products.category)
    return request

def _show_pos_list(category) -> tuple:
    request = session.query(Products).filter(Products.category==category).all()
    return request

def _add_to_cart(uid,id):
    request = Cart(uid,id)
    session.add(request)
    session.commit()

# для генерации окна оплаты
def _list_order(uid) -> tuple:
    data = session.query(Cart,Products).join(Products).filter(Cart.user_id==uid).all()
    return data

# для генерации окна корзины
def _list_order_sort(uid) -> tuple:
    data = session.query(Cart,Products).join(Products).filter(Cart.user_id==uid).group_by(Cart.product_id).all()
    return data

def add_adress(raw_uid,raw_adress):
    request = User.__table__.update().where(User.uid==raw_uid).values(adress=raw_adress)

    session.execute(request)
    session.commit()

def get_user(uid):
    data = session.query(User).filter(User.uid==uid).first()
    return data

def generate_user_cart(uid):
    data = _list_order_sort(uid)
    user = get_user(uid)

    if data:
        text = ''
        sum = 0
        for _, products in data:
                item_count = get_count_in_cart(uid,products.id)
                sum += products.price * item_count
                text = text + f'''{products.name} (<b>x{item_count}</b>) - {products.price} грн | /del{products.id}\n'''
        text += f'\nАдрес: {user.adress}'
        text += f'\n\n Итого: {sum} грн.'
    
    else:
        return
    return text

def generate_order_to_admin(uid):
    data = _list_order_sort(uid)
    user = get_user(uid)

    text = '<b>НОВЫЙ ЗАКАЗ</b>\n\n'

    sum = 0
    for _, products in data:
        item_count = get_count_in_cart(uid,products.id)
        sum += products.price * item_count
        text = text + f'''{products.name} <b>x{item_count}</b>\n'''

    text += f'\n<b>Адрес</b>: {user.adress}'
    text += f'\n<b>ФИО</b>: {user.name}'

    text += f'\n\n Итого: {sum} грн.'
    return text

def generate_dates_list():
    row_data = show_order_dates()
    text = 'Дни, когда были совершены заказы\n\n'
    count = 1
    for data in row_data:
        row_date = data.date.replace('-','_')
        text += f'{count}){data.date} /see_{row_date}\n'
        count += 1

    return text

def generate_orders_list(date,raw_date):
    orders = show_orders_from_date(date)
    text = f'Заказы на {date[:5]}\n\n'
    count = 1
    for order in orders:
        raw_time = order.time.replace(':','_')
        text += f'{count}) {order.adress} [{order.time}] /order_{raw_date}_{raw_time}\n'
        count += 1
    return text

def generate_current_order(date,time):
    text = f'Заказ на {date} [{time}]\n\n'
    raw_data = get_order_sort(date,time)
    sum = 0
    for data in raw_data:
        item_count = get_count_in_order(data.product_name,date,time)
        sum = data.price * item_count
        text += f'{data.product_name} (x{item_count})\n'
    text += f'\nИтого: {sum} грн'
    return text

def get_count_in_cart(uid,item_id):
    request = session.query(func.count(Cart.product_id)).filter(and_(Cart.product_id==item_id, Cart.user_id==uid))
    return request[0][0]

def get_count_in_order(product_name,date,time):
    request = session.query(func.count(Orders.product_name)).filter(and_(Orders.product_name==product_name, 
                                                                            and_(Orders.date==date,
                                                                                and_(Orders.time==time))))
    return request[0][0]

def delete_cart(uid):
    try:
        request = session.query(Cart).filter_by(user_id=uid).all()

    except Exception as e:
        print(e)
    for raw in request:
        session.delete(raw)
    session.commit()

def delete_product_from_cart(product_id,user_id):

    request = session.query(Cart).filter(and_(Cart.product_id==product_id,Cart.user_id==user_id)).first()
    session.delete(request)
    session.commit()

def add_order(uid):
    data = _list_order(uid)
    user = get_user(uid)
    date = datetime.datetime.now().strftime('%d-%m-%Y')
    time = datetime.datetime.now().strftime('%H:%M')

    for _, products in data:

        username = user.name
        adress = user.adress
        product_name = products.name
        price = products.price
    
        request = Orders(username,adress,product_name,price,date,time)
        session.add(request)
    session.commit()

def show_orders_from_date(date):
    request = session.query(Orders).filter(Orders.date==date).group_by(Orders.time).all()
    return request

def show_order_dates():
    return session.query(Orders).group_by(Orders.date).all()

def delete_products_for_test():
    try:
        request = session.query(Products).all()
        for obj in request:
            session.delete(obj)
        session.commit()
    except Exception as e:
        print(e)