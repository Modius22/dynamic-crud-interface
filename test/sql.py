from sqlalchemy import MetaData, create_engine, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

# https://medium.com/@anushkamehra16/connecting-to-sql-database-using-sqlalchemy-in-python-2be2cf883f85

engine = create_engine("mysql+pymysql://wordpress:wordpress@localhost/wordpress")

Session = sessionmaker(bind=engine)
session = Session()


meta = MetaData()

Base = automap_base()
Base.prepare(engine, reflect=True)

name = "wp_options"

wp_options = Base.classes[name]

result = session.query(wp_options).all()

for r in result:
    print(r.option_name)

# new_test = wp_options(name='asasdfsdf',key=00000)
# session.add(new_test)
# session.commit()

# meta.tables.keys()


insp = inspect(engine)
insp.get_table_names()
