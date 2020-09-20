from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Dict, Optional

class Member(BaseModel):
    member_id:str = Field(min_length=2, max_length=20, title="The ID of the member")
    rating: int = Field(..., gt=0, le=11, description="rating from 1 to 10")

class Group_attr(BaseModel):
    attr1: str = Field(None, title="group attribute 1", max_length=100)
    attr2: str  = Field(None, title="group attribute 2", max_length=100)


#service side generate uuid if uuid does not exist yet
class Group_In(BaseModel):
  group_attribute: Group_attr = Field(None, title="group attributes", description="contains 2 attributes")

#group returned without member
class Group_Out(Group_In):
  group_id: UUID 

class Group(Group_Out):
  members: List[Member] = [{}]
