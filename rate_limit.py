from fastapi import FastAPI, HTTPException, Request, Depends, Header

from pydantic import BaseModel
from typing import Optional

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

@app.get("/items/get_one/{name}")
def get_one(name:str):
     try:
          cursor.execute("select * from items where name = ?", (name,)) 
          row = cursor.fetchone()
          if row is None:
               raise HTTPException(status_code=401, detail="Item not found")
          return {"id": row[0], "name": row[1], "description": row[2]}
     except Exception as e:
             return HTTPException(status_code=500, detail=f"Unable to fetch the single data.. {e}")

@app.put("/items/update/{item_id}")
def update_item(item_id: int, i:Item):
    try:
          cursor.execute("update items set name =?, item_description = ? where item_id = ?", (i.name, i.item_description, item_id))
          conn.commit()
          return {"message": "Items update succesfully"}
     
    except Exception as e:
            return HTTPException(status_code=500, detail=f"Unable to update the data.. {e}")

@app.delete("/items/delete/{name}")
def delete_items(name: str):
    try:
         cursor.execute("Delete from items where name =?", (name,))
         conn.commit()
         return {"messages": "items deleted successfully"} 
    except Exception as e:
            return HTTPException(status_code=500, detail=f"Unable to Delete the data.. {e}")

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


@app.get("/greet")
def greet_name(name: Optional[str]= "Ochaye", age:int=0):
     return {"message": f"Hello {name}", "age": age}


class BookModel(BaseModel):
     title : str
     author : str


@app.post("/create_book")
def create_book(book: BookModel):
    return {
         "title": book.title,
         "author": book.author}


@app.get("/get_headers", status_code=200)
def get_headers(
     accept:str = Header(None),
     user_agent: str = Header(None)
):         
    request_header = {}
    request_header["Accept"] = accept
    request_header["User_Agent"] = user_agent
    return request_header