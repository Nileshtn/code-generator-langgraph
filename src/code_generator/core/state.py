from typing import TypedDict, Optional

class codeState(TypedDict):
    query:str
    max_itr:int
    itr:int
    itr_history:Optional[list[str]]
    code:Optional[str]
    feedback_type:Optional[str]
    feedback:Optional[str]
    execution_result:Optional[str]