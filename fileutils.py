import os

__all__ = [
    "create_file", "save_to_file", "fetch_file", "display_file_content",
    "clear_file", "display_file_as_string", "delete_file", "file_exists", "test_content", "load_json", "save_json", "update_json", "clear_json"
]

test_content = 'The quick brown fox jumps over the lazy dog'

def update_json(file: str, record: dict) -> str:
  pass

def load_json(file: str):
  import json
  try:
    with open(f'{file}', 'r') as f:
      return json.load(f)
  except Exception as e:
    return f'Error: {e}!'

def save_json(file: str, record:list) -> str:
  import json
  try:
    if os.path.exists(file):
      with open(f'{file}', 'r') as f:
        data = json.load(f)
    else:
      data = []

    data.append(record)
    try:
      with open(file, 'w') as f:
        json.dump(data, f, indent=2)
        return 'Saved!'
    except Exception as e:
      return f'Error: {e}!'

  except Exception as e:
    return f'Error {e}!'  

def clear_json(file:str) -> str:
  try:
    with open(file, 'w') as f:
      f.write('[]')
      return 'Cleared'
  except Exception as e:
    return f'Error: {e}!'

def create_file(file: str, content: str) -> str:
  try:
    with open(f'{file}', 'w') as f:
      f.write(content)
      return 'Success!'
  except Exception as e:
    return f'Error: {e}!'

def save_to_file(file: str, content: str) -> str:
  try:
    with open(f'{file}', 'a') as f:
      f.write(f'{content}\n')
      return 'Saved!'
  except Exception as e:
    return f'Error: {e}!'
  
def fetch_file(file: str) -> list:
  try:
    with open(f'{file}', 'r') as f:
      return [line.strip() for line in f if line.strip()]
  except Exception as e:
    return f'Error: {e}!'

def display_file_content(lines: list, numerate: bool) -> str:
  string_to_return = ''
  if not numerate:
    for item in lines:
      string_to_return += f'{item}\n' 
  else:
    for i, line in enumerate(lines):
      string_to_return += f'{i+1}. {line}\n'
  return string_to_return

def clear_file(file: str) -> str:
  try:
    with open(f'{file}', 'w') as f:
      f.write('')
      return f'Cleared! {file}'
  except Exception as e:
    return f'Error: {e}!'

def display_file_as_string(file: str) -> str:
  try:
    with open(f'{file}', 'r') as f:
      return f.read()
  except Exception as e:
    return f'Error: {e}!'
  
def delete_file(file: str) -> str:
  try:
    os.remove(file)
    return 'Success!'
  except FileNotFoundError:
    return 'Not Found!'
  except Exception as e:
    return f'Error: {e}!'
  
def file_exists(file: str) -> bool:
  return os.path.isfile(file)

