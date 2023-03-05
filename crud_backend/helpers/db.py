import json

import yaml
from sqlalchemy import MetaData, create_engine, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker


class DB:
    def __init__(self):
        with open("./config.yaml", "r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)

        db = cfg["database"]
        self.engine = create_engine(
            db["driver"] + "://" + db["user"] + ":" + db["password"] + "@" + db["url"] + "/" + db["name"]
        )
        sess = sessionmaker(bind=self.engine)
        self.session = sess()

        self.meta = MetaData()
        self.inspector = inspect(self.engine)

    def get_engine(self):
        return self.engines

    def get_session(self):
        return self.session

    def get_table_names(self):
        return self.inspector.get_table_names()

    def get_table_columns(self, table):
        y = self.inspector.get_columns(table_name=table)
        dicts = {}
        for x in y:
            print("key: {} - value:{}".format(x["name"], x["type"]))
            dicts[x["name"]] = str(x["type"])
        return json.dumps(dicts)

    def get_table_data_all(self, table):
        Base = automap_base()
        Base.prepare(self.engine, reflect=True)
        result = self.session.query(Base.classes[table]).all()

        return result

    def set_tabel_field(self, key, value):
        # Base = automap_base()
        # @ToDo: how can this be implemented: https://docs.sqlalchemy.org/en/14/core/dml.html
        pass


# test = DB()

# x = test.get_table_names()
# y = test.get_table_columns("test")
#
# data = test.get_table_data_all("test")
