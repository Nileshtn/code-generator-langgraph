from code_generator.core.state import codeState
from code_generator import logger

def print_response(state : codeState):
    print(state['code'])

def write_file(state : codeState):
    logger.info(f"writing code to the file!")
    with open("generated_code.py", "w") as f:
        f.write(state["code"])

