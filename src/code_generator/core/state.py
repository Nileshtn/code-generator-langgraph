from typing import TypedDict, Optional

class codeState(TypedDict):
    query:str
    max_itr:int 
    itr:int
    code:Optional[str]
    feedback_type:Optional[str] 
    feedback:Optional[str]
    code_score:Optional[int]