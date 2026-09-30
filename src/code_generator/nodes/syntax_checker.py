import ast
from code_generator.core.state import codeState
from code_generator import logger


exclude_state = [""]

def check_syntax_node(state: codeState) -> tuple[bool, str]:
    try:
        ast.parse(state["code"])
        logger.info(f"no error found (itr : {state['itr']})")
        return {"feedback_type" : ""}
    except SyntaxError as e:
        logger.info(f"error found -> refactoring error (itr : {state['itr']})")
        return {"feedback_type" : "error", "feedback" : f"SyntaxError on line {e.lineno}: {e.msg}"}


def error_route(state : codeState):
    if state["feedback_type"] in exclude_state:
        return "review_code"
    return "error"