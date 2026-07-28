from fastapi import FastAPI, HTTPException, Request, Depends

import sqlite3


app = FastAPI()

conn = sqlite3.connect("test.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute('''

  create table if not exists items(
  
  item_id integer auto increment primary key,
  name text not null,
  item_description text
  
  )

''')





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

