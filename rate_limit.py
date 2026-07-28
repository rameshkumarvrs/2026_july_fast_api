from fastapi import FastAPI, HTTPException, Request, Depends

from pydantic import BaseModel

import sqlite3


app = FastAPI()

conn = sqlite3.connect("test.db", check_same_thread=False)

cursor = conn.cursor()

# cursor.execute("DROP TABLE IF EXISTS items")

# cursor.execute('''

#   create table if not exists items(
  
#   item_id INTEGER PRIMARY KEY AUTOINCREMENT,
#   name TEXT NOT NULL,
#   item_description TEXT
  
#   )

# ''')

# conn.commit()

class Item(BaseModel):
    name: str
    item_description: str



@app.post("/items/create/")
def create_item(i: Item):
    try:
        cursor.execute("Insert into items(name, item_description) values(?,?)", (i.name, i.item_description))

        conn.commit()
        return {"message": "Items stored successfully", "item": i}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to insert.. {e}")


@app.get("/items/")
def get_all_items():
    try:
        cursor.execute("select * from items")
        rows = cursor.fetchall()
        conn.commit()
        return [{"id": r[0], "name": r[1], "description": r[2]} for r in rows] 

    except Exception as e:
            return HTTPException(status_code=500, detail=f"Unable to fetch the data.. {e}")



# app = FastAPI()


# rate_limit = {}

# max_count = 5

# @app.get("/data")
# def get_data(request : Request):

#     client_ip = request.client.host
#     rate_limit[client_ip] = rate_limit.get(client_ip,0)+1

#     print(rate_limit)

#     if rate_limit[client_ip] > max_count:
#         raise HTTPException(status_code=500, detail="Rate limit exceeds")

#     return {"Message": f"request{rate_limit[client_ip]} is successfull"}


# def get_db():
#     return {"message": "db retrived"}

# @app.get("/datacenter")
# def get_datas(a :dict = Depends(get_db)):
#     return {"message": "Dependency data recived", "db_status": a}

