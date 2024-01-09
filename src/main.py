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

@app.post("/items/")
def create_item(item: dict):
    return {"item": item}

@app.post("/items/test/test1")
def create_item(item: dict):
    return {"item": item}


# def save_openapi_to_file():
#     openapi_content = get_openapi(title="Lazaza", version="1.0.0",routes=app.routes)
#     with open("openapi.json", "w", encoding="utf-8") as file:
#         json.dump(openapi_content, file, ensure_ascii=False, indent=2)

def save_openapi_to_file():
    existing_content = None
    try:
        with open("openapi.json", "r", encoding="utf-8") as existing_file:
            existing_content = json.load(existing_file)
    except FileNotFoundError:
        pass  # File not found, no existing content

    new_file_path = "openapi-new.json"
    with open(new_file_path, "w", encoding="utf-8") as new_file:
        openapi_content = get_openapi(title="Lazaza", version="1.0.0", routes=app.routes)
        json.dump(openapi_content, new_file, ensure_ascii=False, indent=2)

    if existing_content is not None and existing_content == openapi_content:
        print("No changes detected. Deleting the temporary file.")
        import os
        os.remove(new_file_path)
        return False

    with open(new_file_path, "r", encoding="utf-8") as new_file:
        new_content = json.load(new_file)
        with open("openapi.json", "w", encoding="utf-8") as existing_file:
            json.dump(new_content, existing_file, ensure_ascii=False, indent=2)

    import os
    os.remove(new_file_path)
    
    return True

def get_openapi_status():
    changes_detected = save_openapi_to_file()
    print(f"Changes detected: {changes_detected}")
    exit_code = 0 if not changes_detected else 1
    exit(exit_code)


get_openapi_status()



