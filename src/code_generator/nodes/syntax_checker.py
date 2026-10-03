import ast
from code_generator.core.state import codeState
from code_generator import logger




def check_syntax_node(state: codeState) -> tuple[bool, str]:
    try:
        ast.parse(state["code"])
        logger.info(f"no error found (itr : {state['itr']})")
        return {"feedback_type" : "review_code"}
    except SyntaxError as e:
        logger.info(f"error found -> refactoring error (itr : {state['itr']})")
        return {"feedback_type" : "error", "feedback" : f"SyntaxError on line {e.lineno}: {e.msg}"}


def error_route(state : codeState):
    return state["feedback_type"]