from fastapi import FastAPI, HTTPException, Request

app = FastAPI()


rate_limit = {}

max_count = 5

@app.get("/data")
def get_data(request : Request):

    client_ip = request.client.host
    rate_limit[client_ip] = rate_limit.get(client_ip,0)+1

    print(rate_limit)

    if rate_limit[client_ip] > max_count:
        raise HTTPException(status_code=500, detail="Rate limit exceeds")

    return {"Message": f"request{rate_limit[client_ip]} is successfull"}
