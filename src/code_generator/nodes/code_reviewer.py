from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from code_generator.config import prompt, model_config
from code_generator.core.state import codeState
from pydantic import BaseModel, Field
from code_generator import logger


class CodeReviewResult(BaseModel):
    critic: str = Field(
        description="Detailed technical breakdown including Big-O complexity, bottlenecks, verdict, and recommended optimizations formatted in markdown."
    )
    score: int = Field(
        ge=1,
        le=10,
        description="Complexity & Optimality rating integer from 1 (broken/degenerate) to 10 (fully optimal).",
    )

reviewer_llm = ChatOllama(model=model_config['model'], temperature=model_config['temp'])
structured_output = reviewer_llm.with_structured_output(CodeReviewResult)

prompt = ChatPromptTemplate([('system', prompt['quality_system_prompt']), 
                             ('human', prompt['quality_user_prompt'])],
                             template_format="jinja2")


chain = prompt | structured_output



# to be changed
def code_reviewer_node(state : codeState):
    logger.info(f"started code review (itr no : {state['itr']})")
    if state['itr'] >= state['max_itr']:
        logger.warning(f"max itr reached on review!")
        return {"feedback_type" : "",
                "feedback" : ""}

    
    if state["feedback_type"] == "":
        logger.info(f"reviewing code (itr : {state['itr']})")
        response:CodeReviewResult = chain.invoke({"code" : state["code"]})

    new_itr_num = state["itr"] + 1

    if response.score < 8:
        logger.info(f"current code score {response.score}, refactoring again")
        return {"feedback_type" : "refactor",
                "feedback" : response.critic,
                "itr" : new_itr_num}

    else:
        logger.info(f"current code score {response.score}, got a good code!")
        return {"feedback_type" : "",
                "feedback" : "",
                "itr" : new_itr_num}



def review_route(state : codeState):
    if state["feedback_type"] == "":
        return "write"
    return "refactor"