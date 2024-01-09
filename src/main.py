from fastapi import FastAPI,HTTPException


app = FastAPI()

data_store = {}


@app.get("/get-endpoint/{item_id}")
def read_item(item_id: int, query_param: str = None):
    if item_id in data_store:
        return {"item_id": item_id, "item_data": data_store[item_id], "query_param": query_param}
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/post-endpoint")
def create_item(item_id: int, item_data: str):
    if item_id in data_store:
        raise HTTPException(status_code=400, detail="Item already exists")
    data_store[item_id] = item_data
    return {"item_id": item_id, "item_data": item_data}


@app.patch("/patch-endpoint/{item_id}")
def update_item(item_id: int, item_data: str):
    if item_id not in data_store:
        raise HTTPException(status_code=404, detail="Item not found")
    data_store[item_id] = item_data
    return {"item_id": item_id, "item_data": item_data}


@app.put("/put-endpoint/{item_id}")
def replace_item(item_id: int, item_data: str):
    if item_id not in data_store:
        raise HTTPException(status_code=404, detail="Item not found")
    data_store[item_id] = item_data
    return {"item_id": item_id, "item_data": item_data}


@app.delete("/delete-endpoint/{item_id}")
def delete_item(item_id: int):
    if item_id not in data_store:
        raise HTTPException(status_code=404, detail="Item not found")
    del data_store[item_id]
    return {"message": "Item deleted successfully"}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}

@app.post("/items/")
def create_item(item: dict):
    return {"item": item}

@app.post("/items/test/test1")
def create_item(item: dict):
    return {"item": item}




