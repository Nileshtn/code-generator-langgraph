from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from code_generator.config import prompt, model_config
from code_generator.core.state import codeState
from code_generator import logger
import re


def extract_raw_code(llm_output: str) -> str:
    """Extracts raw code from markdown fences if present, otherwise returns stripped text."""
    pattern = r"```(?:python)?\s*([\s\S]*?)\s*```"
    match = re.search(pattern, llm_output, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return llm_output.strip()


generator_llm = ChatOllama(model=model_config['model'], temperature=model_config['temp'])
prompt = ChatPromptTemplate([('system', prompt['generator_system_prompt']), 
                             ('human', prompt['generator_user_prompt'])], 
                             template_format="jinja2").partial(existing_code=None, feedback_type=None, feedback=None)


chain = prompt | generator_llm | StrOutputParser() | extract_raw_code


def code_generator_node(state : codeState):
    '''
    funtion generate code based on the problem statement and the existing code
    fixes error if any and return the code
    refactor the code if needed and return the code

    feedback_type:
        - "error"
        - "refactor"
        - ""
    '''

    if state["feedback_type"] == "":
        logger.info("generating code for the first time...")
        response = chain.invoke({'problem_statement' : state["query"]})
        return {"code" : response}

    logger.info(f"refactoring code , type : {state['feedback_type']}")

    response = chain.invoke({"problem_statement" : state["query"],
                            "existing_code" : state["code"],
                            "feedback_type" : state["feedback_type"],
                            "feedback" : state["feedback"]
                                                })


    return {"code" : response, "feedback_type" : "", "feedback" : ""}


        