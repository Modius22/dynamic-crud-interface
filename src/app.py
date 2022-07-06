import json

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.config import logger

import helpers.db as db

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello_world():  # put application's code here
    return "Hello World!"


@app.get("/get_db_names")
def get_db_data():
    try:
        test = db.DB()
        data = test.get_table_names()
        return json.dumps(data)
    except Exception as e:
        logger.info("Error in api call get_db_names: {}".format(e))


@app.get("/{table}/get_table_structure")
async def get_table_structure(table: str):
    try:
        test = db.DB()
        logger.info(table)
        data = test.get_table_columns(table)
        return data
    except Exception as e:
        logger.info("Error in api call get_table_structure: {}".format(e))


# @app.get("/{table}/{key}")
# async def get_column(table: str, key: str):
#    logger.info('Table: {} - Key: {}'.format(table,key))
#    return 'jojo'


@app.get("/table_data/{table}")
async def get_table_data(table: str):
    logger.info("get table data of table: {}".format(table))

    test = db.DB()

    data = test.get_table_data_all(table)
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2000)
