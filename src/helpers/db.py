import logging

import yaml
from sqlalchemy import MetaData, create_engine, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker


class DB:
    """
    A class for interacting with a SQL database.

    Attributes:
        engine (sqlalchemy.engine.base.Engine): The database engine.
        session (sqlalchemy.orm.session.Session): The database session.
        meta (sqlalchemy.schema.MetaData): The database metadata.
        inspector (sqlalchemy.engine.reflection.Inspector): The database inspector.
        logger (logging.Logger): The logger for the class.
    """

    def __init__(self, path="./"):
        """
        Initializes a new instance of the DB class.

        Args:
            path (str): The path to the configuration file for the database.
        """
        # Load database configuration from file
        with open(path + "config.yaml") as ymlfile:
            cfg = yaml.safe_load(ymlfile)

        # Create database engine
        db = cfg["database"]
        self.engine = create_engine(
            db["driver"]
            + "://"
            + db["user"]
            + ":"
            + db["password"]
            + "@"
            + db["url"]
            + ":"
            + db["port"]
            + "/"
            + db["name"]
        )

        # Create database session
        sess = sessionmaker(bind=self.engine)
        self.session = sess()

        # Create database metadata and inspector
        self.meta = MetaData()
        self.inspector = inspect(self.engine)

        # Create logger for the class
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")

        file_handler = logging.FileHandler("db.log")
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def get_engine(self):
        """
        Returns the database engine.

        Returns:
            sqlalchemy.engine.base.Engine: The database engine.
        """
        return self.engine

    def get_session(self):
        """
        Returns the database session.

        Returns:
            sqlalchemy.orm.session.Session: The database session.
        """
        return self.session

    def get_table_names(self):
        """
        Returns a list of all table names in the database.

        Returns:
            list: A list of all table names in the database.
        """
        try:
            return self.inspector.get_table_names()
        except Exception as e:
            self.logger.error(f"Error in get_table_names: {e}")

    def get_table_columns(self, table):
        """
        Returns a dictionary of all columns in the specified table.

        Args:
            table (str): The name of the table to retrieve column information for.

        Returns:
            dict: A dictionary of all columns in the specified table.
        """
        try:
            dicts = {}
            for x in self.inspector.get_columns(table_name=table):
                dicts[x["name"]] = str(x["type"])
            return dicts
        except Exception as e:
            self.logger.error(f"Error in get_table_columns: {e}")

    def get_table_data_all(self, table):
        """
        Returns all data in the specified table.

        Args:
            table (str): The name of the table to retrieve data for.

        Returns:
            list: All data in the specified table.
        """
        try:
            base = automap_base()
            base.prepare(self.engine, reflect=True)
            result = self.session.query(base.classes[table]).all()

            return result
        except Exception as e:
            self.logger.error(f"Error in get_table_data_all: {e}")

    def set_table_field(self, table, field, value):
        """
        Sets the value of a field in the database.

        Args:
            table (str): The name of the table to update.
            field (str): The name of the field to update.
            value (any): The new value for the field.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            # Get the table object
            base = automap_base()
            base.prepare(self.engine, reflect=True)
            table_obj = base.classes[table]

            # Update the field value
            row = self.session.query(table_obj).first()
            setattr(row, field, value)
            self.session.commit()

            self.logger.info(f"Field {field} in table {table} updated successfully")
            return True

        except Exception as e:
            self.logger.error(f"Error in set_table_field: {e}")
            return False

    def update_table_structure(self, table: str, new_schema: dict):
        """
        Updates the schema of the specified table.

        Args:
            table (str): The name of the table to update.
            new_schema (dict): The new schema for the table.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            columns = self.get_table_columns(table)

            # Check if all columns in new schema exist in current schema
            for column in new_schema:
                if column not in columns:
                    self.logger.error(f"Column {column} does not exist in table {table}")
                    return False

            # Check if all columns in current schema exist in new schema
            for column in columns:
                if column not in new_schema:
                    self.logger.error(f"Column {column} is missing in new schema for table {table}")
                    return False

            # Update table schema
            for column, data_type in new_schema.items():
                self.engine.execute(f"ALTER TABLE {table} ALTER COLUMN {column} TYPE {data_type}")

            self.logger.info(f"Table {table} schema updated successfully")
            return True

        except Exception as e:
            self.logger.error(f"Error in update_table_structure: {e}")
            return False
