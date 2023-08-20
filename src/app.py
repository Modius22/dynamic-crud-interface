import helpers.db as db
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def hello_world():
    """
    Returns a simple "Hello World!" message.

    Returns:
        str: A simple "Hello World!" message.
    """
    return "Hello World!"


def get_db_data():
    """
    Returns a list of all table names in the database.

    Returns:
        list: A list of all table names in the database.
    """
    try:
        test = db.DB()
        data = test.get_table_names()
        return data
    except Exception as e:
        app.logger.error(f"Error in api call get_db_names: {e}")


def get_table_structure(table: str):
    """
    Returns a dictionary of all columns in the specified table.

    Args:
        table (str): The name of the table to retrieve column information for.

    Returns:
        dict: A dictionary of all columns in the specified table.
    """
    try:
        test = db.DB()
        app.logger.info(table)
        data = test.get_table_columns(table)
        return data
    except Exception as e:
        app.logger.error(f"Error in api call get_table_structure: {e}")


def get_table_data(table: str):
    """
    Returns all data in the specified table.

    Args:
        table (str): The name of the table to retrieve data for.

    Returns:
        list: All data in the specified table.
    """
    app.logger.info(f"get table data of table: {table}")

    test = db.DB()

    data = test.get_table_data_all(table)
    return data


@app.get("/")
async def root():
    """
    Returns a simple "Hello World!" message.

    Returns:
        str: A simple "Hello World!" message.
    """
    return hello_world()


@app.get("/get_db_names")
async def read_db_names():
    """
    Returns a list of all table names in the database.

    Returns:
        list: A list of all table names in the database.
    """
    return get_db_data()


@app.get("/{table}/get_table_structure")
async def read_table_structure(table: str):
    """
    Returns a dictionary of all columns in the specified table.

    Args:
        table (str): The name of the table to retrieve column information for.

    Returns:
        dict: A dictionary of all columns in the specified table.
    """
    return get_table_structure(table)


@app.get("/table_data/{table}")
async def read_table_data(table: str):
    """
    Returns all data in the specified table.

    Args:
        table (str): The name of the table to retrieve data for.

    Returns:
        list: All data in the specified table.
    """
    return get_table_data(table)


@app.route("/set_table_field", methods=["POST"])
async def set_table_field(request: Request):
    """
    Sets the value of a field in the database.

    Request Body:
        table (str): The name of the table to update.
        field (str): The name of the field to update.
        value (any): The new value for the field.

    Returns:
        str: A message indicating whether the update was successful or not.
    """
    try:
        data = request.get_json()
        table = data["table"]
        field = data["field"]
        value = data["value"]

        test = db.DB()
        success = test.set_table_field(table, field, value)

        if success:
            return "Field updated successfully"
        else:
            return "Error updating field"

    except Exception as e:
        app.logger.error(f"Error in set_table_field API call: {e}")
        return "Error updating field"


@app.route("/update_table_structure", methods=["POST"])
async def update_table_structure(request: Request):
    """
    Updates the schema of the specified table.

    Request Body:
        table (str): The name of the table to update.
        new_schema (dict): The new schema for the table.

    Returns:
        str: A message indicating whether the update was successful or not.
    """
    try:
        data = request.get_json()
        table = data["table"]
        new_schema = data["new_schema"]

        test = db.DB()
        success = test.update_table_structure(table, new_schema)

        if success:
            return "Table schema updated successfully"
        else:
            return "Error updating table schema"

    except Exception as e:
        app.logger.error(f"Error in update_table_structure API call: {e}")
        return "Error updating table schema"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2000)
