from sqlalchemy import create_engine,update
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
    description = Column(String)
    price = Column(Integer)  

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price    

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    product_id = Column(Integer,ForeignKey('products.id'))

    def __init__(self,user_id,product_id):
        self.user_id = user_id
        self.product_id = product_id

# class Adress(Base):
#     __tablename__ = 'adress'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer)
#     adress = Column(String)

#     def __init__(self,user_id,adress):
#         self.user_id = user_id
#         self.adress = adress

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
    
def add_position_to_db(name, description, price):

    request = Products(name, description, price)
    session.add(request)
    session.commit()

def show_all_position(to_delete=False):
    text = 'id | НАЗВАНИЕ | ЦЕНА\n'
    request = session.query(Products).order_by(Products.id).all()
    for raw in request:
        text = text + f'{raw.id}| {raw.name} | {raw.price} UAH \n'

    return text

def change_price(id, new_price):
    request = session.query(Products).get(id)
    request.price = new_price

    session.commit()   

def _show_pos_list(colname) -> tuple:
    request = session.query(Products).filter(Products.name.ilike(f'%{colname}%')).all()
    return request

def _add_to_cart(uid,id):
    request = Order(uid,id)
    session.add(request)
    session.commit()

def _list_order(uid) -> tuple:
    data = session.query(Order,Products).join(Products).filter(Order.user_id==uid).all()
    return data

def add_adress(raw_uid,raw_adress):
    request = User.__table__.update().where(User.uid==raw_uid).values(adress=raw_adress)

    session.execute(request)
    session.commit()

def get_adress(uid):
    data = session.query(User).filter(User.uid==uid).first()
    return data.adress

# def del_adress(uid):
#     try:
#         request = session.query(Adress).filter_by(user_id=uid).all()
#         for raw in request:
#             session.delete(raw)
#     except:
#         return
   
#     session.commit()

def delete_cart(uid):
    try:
        request = session.query(Order).filter_by(user_id=uid).all()

    except Exception as e:
        print(e)
    for raw in request:
        session.delete(raw)
    session.commit()

