import pyodbc
from sqlalchemy.orm import  sessionmaker
from sqlalchemy import create_engine, Column, Integer,String, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base, declarative_base
#https://medium.com/@anushkamehra16/connecting-to-sql-database-using-sqlalchemy-in-python-2be2cf883f85

engine = create_engine('mysql+pymysql://wordpress:wordpress@localhost/wordpress')

Session = sessionmaker(bind=engine)
session = Session()

from sqlalchemy.ext.automap import automap_base

meta  = MetaData()

Base = automap_base()
Base.prepare(engine,reflect=True)

name = 'wp_options'

wp_options = Base.classes[name]

result = session.query(wp_options).all()

for r in result:
    print(r.option_name)

#new_test = wp_options(name='asasdfsdf',key=00000)
#session.add(new_test)
#session.commit()

#meta.tables.keys()



from sqlalchemy import inspect, create_engine

insp = inspect(engine)
insp.get_table_names()