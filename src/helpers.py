import os 

def check_path(path: str) -> bool:
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found")
    return True