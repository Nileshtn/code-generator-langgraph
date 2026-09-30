from code_generator.core.state import codeState
from langgraph.graph import StateGraph, END, START
from code_generator.nodes import (check_syntax_node, 
                                error_route,
                                review_route,
                                code_reviewer_node,
                                code_generator_node,
                                write_file)

from code_generator import logger

def generator_graph_app():
    logger.info("graph created!")
    logger.info(f"state : {codeState}")
    workflow = StateGraph(codeState)

    workflow.add_node('generator', code_generator_node)
    workflow.add_node('syntax_checker', check_syntax_node)
    workflow.add_node("code_reviewer", code_reviewer_node)
    workflow.add_node("write_file", write_file)

    workflow.add_edge(START, 'generator')
    workflow.add_conditional_edges('generator',
                                   error_route,
                                   {'error' : 'generator',
                                    'review_code' : 'code_reviewer'})
    workflow.add_conditional_edges("code_reviewer",
                                   review_route,
                                   {"refactor" : "generator",
                                    "write": "write_file"})
    workflow.add_edge("write_file", END)
    
    return workflow.compile()


app = generator_graph_app()
