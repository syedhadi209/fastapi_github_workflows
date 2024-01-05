from fastapi.openapi.utils import get_openapi
import json
from src.main import app

def save_openapi_to_file():
    # Check if openapi.json exists
    try:
        with open("openapi.json", "r", encoding="utf-8") as existing_file:
            existing_content = json.load(existing_file)
    except FileNotFoundError:
        existing_content = None

    # Create a new openapi-new.json file
    new_file_path = "openapi-new.json"
    with open(new_file_path, "w", encoding="utf-8") as new_file:
        openapi_content = get_openapi(title="Lazaza", version="1.0.0", routes=app.routes)
        json.dump(openapi_content, new_file, ensure_ascii=False, indent=2)

    # Check if both files have the same content
    if existing_content is not None:
        with open(new_file_path, "r", encoding="utf-8") as new_file:
            new_content = json.load(new_file)
            if existing_content == new_content:
                print("No changes detected. Deleting the temporary file.")
                # Clean up: Delete the temporary file
                import os
                os.remove(new_file_path)
                return False

    # Update openapi.json with the content of openapi-new.json
    with open(new_file_path, "r", encoding="utf-8") as new_file:
        new_content = json.load(new_file)
        with open("openapi.json", "w", encoding="utf-8") as existing_file:
            json.dump(new_content, existing_file, ensure_ascii=False, indent=2)

    # Clean up: Delete the temporary file
    import os
    os.remove(new_file_path)
    
    return True


def get_openapi_status():
    try:
        changes_detected = save_openapi_to_file()
        print(f"Changes detected: {changes_detected}")
        exit_code = 0 if not changes_detected else 1
        exit(exit_code)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Expected error: {e}")
        exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)