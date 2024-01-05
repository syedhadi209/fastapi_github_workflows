from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}


def save_openapi_to_file():
    openapi_content = get_openapi(title="Lazaza", version="1.0.0",routes=app.routes)
    with open("openapi.json", "w", encoding="utf-8") as file:
        json.dump(openapi_content, file, ensure_ascii=False, indent=2)
