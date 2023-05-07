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

class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    product_id = Column(Integer,ForeignKey('products.id'))

    def __init__(self,user_id,product_id):
        self.user_id = user_id
        self.product_id = product_id

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

def _show_list_category() -> tuple:
    request = session.query(Products.category).distinct(Products.category)
    return request

def _show_pos_list(category) -> tuple:
    request = session.query(Products).filter(Products.category==category).all()
    return request

def _add_to_cart(uid,id):
    request = Orders(uid,id)
    session.add(request)
    session.commit()

def _list_order(uid) -> tuple:
    data = session.query(Orders,Products).join(Products).filter(Orders.user_id==uid).group_by(Orders.product_id).all()
    return data

def add_adress(raw_uid,raw_adress):
    request = User.__table__.update().where(User.uid==raw_uid).values(adress=raw_adress)

    session.execute(request)
    session.commit()

def get_user(uid):
    data = session.query(User).filter(User.uid==uid).first()
    return data

def get_count_in_order(uid,item_id):
    request = session.query(func.count(Orders.product_id)).filter(and_(Orders.product_id==item_id, Orders.user_id==uid))
    return request[0][0]

def delete_cart(uid):
    try:
        request = session.query(Orders).filter_by(user_id=uid).all()

    except Exception as e:
        print(e)
    for raw in request:
        session.delete(raw)
    session.commit()

def delete_product_from_order(product_id,user_id):

    request = session.query(Orders).filter(and_(Orders.product_id==product_id,Orders.user_id==user_id)).first()
    session.delete(request)
    session.commit()

def delete_products_for_test():
    try:
        request = session.query(Products).all()
        for obj in request:
            session.delete(obj)
        session.commit()
    except Exception as e:
        print(e)