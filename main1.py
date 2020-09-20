from fastapi.logger import logging
from fastapi import FastAPI, Path, Query, Body, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel
from starlette.responses import RedirectResponse
from uuid import UUID, uuid4
from typing import List

from data.dmodel import Group, Group_attr, Member, Group_In, Group_Out
from utils.utils import *
from settings.settings import getEnv, s_output

import copy



app=FastAPI()

#logger = logging.getLogger(__name_)
#logger.setLevel(logging.DEBUG)
logger = logging.getLogger("gunicron.error")

#https://github.com/tiangolo/fastapi/issues/199

@app.get("/")
def read_root():
    url = app.url_path_for("read_app")
    response = RedirectResponse(url=url)
    #return f"Welcome to whsu api" 
    return response
    
@app.get("/app/")
async def read_app():
    return f"Welcome to whsu app api" 

@app.get("/health/")
async def read_app():
    return f"whsu api is up and running..." 

@app.get("/group/", response_model=Group, summary="getting the group from group id or the first group", response_description="group returned")
def read_group(gid: UUID = Query(None)):
      dataList= loadJson(s_output)
      logger.info(dataList)
      for grp in dataList:
          if (gid == None or str(grp['group_id']) == str(gid)):
               return grp
      raise HTTPException(status_code=404, detail="group with the id is not found")

@app.get("/groups/", response_model=List[Group], summary="getting the whole groups", response_description="group returned")
def read_groups():
      dataList= loadJson(s_output)
      if not dataList or len(dataList) == 0:
        raise HTTPException(status_code=404, detail="empty group")

      return dataList 

@app.get("/groups/attributes", response_model=List[Group_Out], summary="getting the whole groups only with attributes without members", response_description="group returned")
def read_groupattrs():
      dataList= loadJson(s_output)
      if not dataList or len(dataList) == 0:
        raise HTTPException(status_code=404, detail="empty group")
      return dataList 

@app.get("/group/attr/", response_model=Group_Out, summary="getting the group attribute for the first group's attributes", response_description="group attributes without member returned")
def read_groupattr(gid: UUID = Query(None)):
      dataList= loadJson(s_output)
      if not dataList or len(dataList)== 0:
          raise HTTPException(status_code=404, detail="no group exists yet")
      for grp in dataList:
          if gid == None or str(grp['group_id'])== str(gid):
             return grp
      raise HTTPException(status_code=404, detail="group with the id is not found")

@app.post("/group/", status_code=201, response_model=Group_Out, response_model_exclude_unset=True)
def create_group(grp:Group_In=Body(..., embed=True)):
       result={}
       result['group_id']=uuid4()
       result['group_attribute']=grp.group_attribute

       data=findEntryInJson(s_output, result['group_id'])
       if not data:
            dumpJson(jsonable_encoder(result), s_output)
       else:
            raise HTTPException(status_code=400, detail="Item already exists") 
       return result     

@app.put("/group/member/rate/", response_model=Group, response_description="update member rating and return updated group or None")
def update_member_rating(group_id:str=Query(..., max_length=50), member:Member=Body(..., embed=True)):

      data1=findEntryInJson(s_output, group_id)
      logger.info("data1 in member")
      logger.info(data1)
      if not data1 or len(data1) == 0:
         raise HTTPException(status_code=404, detail="group does not exist") 

      updateMembers(s_output, group_id, member)

      return data1
    
@app.put("/group/{group_id}/attr/", response_model=Group_Out, response_description="update group attribute and return the original group list without members")
def update_group_attribute(group_id:str = Query(..., max_length=50), attrs:Group_attr=Body(..., embed=True)):

      data1=findEntryInJson(s_output, group_id)
      #if not data1 or len(data1) == 0:
         #empty response , no update is needed
      #   return Response(status_code=status.HTTP_200_OK) 

      if not data1 or len(data1) == 0:
         raise HTTPException(status_code=404, detail="group does not exist") 

      updateAttributes(jsonfile, gid, attrs)

if __name__=="__main__":
      import uvicorn
      uvicorn.run("main:app", host="localhost", port=3002, reload=True, debug=True)
#to do : router,(app.router : multiple files : bigger apps ) cache,  async equvialent of with open file router serialization with UUID db
