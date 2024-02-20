from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse  
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
app = FastAPI()
origins = [
    "https://tool.sddoc.in",
    "http://localhost:3000",
    "http://68.183.81.248",
    "http://68.183.81.248/",
    "http://62.72.0.214/",
    "http://62.72.0.214",
    "http://localhost:3000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# host = 'roundhouse.proxy.rlwy.net'
# database = 'u958929721_tools'
# user = 'root'
# password = 'gcC4cgchGCghg3-611256A5eED-ed-g5'
# port = 14636
host = '193.203.166.103'
database = 'u958929721_admin'
user = 'u958929721_admin'
password = 'Pr0h1b1t3d'
port = 3306

async def get_connection():
    return create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )


async def get_table_data_as_json(engine, table_name):
    df = pd.read_sql_table(table_name, engine)
    json_data = df.to_json(orient='records')

    return json_data

# engine = get_connection()
# json_data = get_table_data_as_json(engine, 'deft_platforms')
# print(json_data)



async def get_feature(engine, table_name, platform_id):
    query = text(f"SELECT * FROM {table_name} WHERE platform_id = :platform_id")
    df = pd.read_sql_query(query, engine, params={"platform_id": platform_id})
    json_data = df.to_json(orient='records')
    return json_data

# engine = get_connection()
# json_data = get_feature(engine, 'deft_features', 1)
# print(json_data)


@app.get("/get_data")
async def get_data_endpoint():
    data = await get_table_data_as_json(await get_connection(), 'deft_platforms')
    return json.loads(data)


@app.get("/get_feature")
async def get_feature_endpoint(platform_id: int = Query(...)):
    data = await get_feature(await get_connection(), 'deft_features', platform_id)
    return  json.loads(data)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
