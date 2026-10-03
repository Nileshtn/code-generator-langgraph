from langchain_core.prompts import ChatPromptTemplate
from code_generator.core.llm import core_llm
from code_generator.config import prompt
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

structured_output = core_llm.with_structured_output(CodeReviewResult)

prompt = ChatPromptTemplate([('system', prompt['quality_system_prompt']), 
                             ('human', prompt['quality_user_prompt'])],
                             template_format="jinja2")


chain = prompt | structured_output


def code_reviewer_node(state : codeState):
    logger.info(f"started code review (itr no : {state['itr']})")
    response = None
    
    if state["feedback_type"] == "review_code" and state['itr'] < state['max_itr']:
        logger.info(f"reviewing code (itr : {state['itr']})")
        response:CodeReviewResult = chain.invoke({"code" : state["code"]})
    
    new_itr_num = state["itr"] + 1

    if not response:
        logger.info(f"""no response generated, max itr state : {state['itr']>=state['max_itr']},
                    feed back from syntax checker {state["feedback_type"]}
                    """)
        return {"feedback_type" : "",
                "feedback" : ""}

    if response.score < 8:
        logger.info(f"current code score {response.score}, refactoring again")
        return {"feedback_type" : "refactor",
                "feedback" : response.critic,
                "itr" : new_itr_num}

    else:
        logger.info(f"current code score {response.score}, got a good code!")
        return {"feedback_type" : "",
                "feedback" : ""}



def review_route(state : codeState):
    if state["feedback_type"] == "":
        return "write"
    return "refactor"