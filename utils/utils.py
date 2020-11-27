#https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/

import json, os
from fastapi.logger import logging
from fastapi.encoders import jsonable_encoder
import shutil

logger = logging.getLogger("gunicron.error")

def loadJson(jsonfile, mode='r', encoding='utf8'):
     if not os.path.exists(jsonfile) or  os.stat(jsonfile).st_size == 0:
        return []
     dataList=[]
     with open(jsonfile, 'r') as infile:
         for line in infile:
            #line=line.strip()[:-1]
            print(line)
            if (',' != line.strip()):
              dataDict=json.loads(line.strip())
              logger.info(dataDict)
              if dataDict:
                dataList.append(dataDict)
     return dataList 

def findGroupInJsonByGid(jsonfile, gid):
     with open(jsonfile, 'r') as infile:
       for line in infile:
          dataDict=json.loads(line.strip())
          if not dataDict:
             return None
          if str(dataDict['group_id'])==str(gid):
              logger.info("found : ")
              logger.info(dataDict)
              return dataDict
       return None 

def updateMembers(jsonfile, gid, member1):
     #precondition : gid is known existing 
     result=[]
     updatedgroup={}
     with open(jsonfile, 'r') as infile:
       for line in infile:
          dataDict=json.loads(line.strip())

          if str(dataDict['group_id'])==str(gid):
              logger.info("found : ")
              logger.info(dataDict)
              updatedmembers=[]
              memberlist=dataDict.get('members', [])

              for newmember in memberlist:
                print(newmember)
                print(dict(member1))
                print(newmember['member_id'])
                m1_dict=dict(member1)
                if newmember['member_id']==m1_dict['member_id']:
                  newmember['rating']=m1_dict['rating']
                  updatedgroup=dataDict
                  break

              if not updatedgroup:
                 dataDict['members'].append(member1)
                 updatedgroup=dataDict
              
          result.append(dataDict)

     writeNewOutput(result,jsonfile) 
     #with open(jsonfile, 'w') as outfile:
     #   for group1 in result:
     #     dumpJson(jsonable_encoder(group1), outfile)

     return updatedgroup        

def dumpJson(data, jsonfile, mode='a+', newline='\n'):
    with open(jsonfile, mode) as outfile:
        json.dump(data, outfile)
        outfile.write(newline)

def updateAttributes(jsonfile, gid, attrs):
     #precondition : gid is known existing 
     result=[]
     updatedgroup={}
     with open(jsonfile, 'r') as infile:
       for line in infile:
          dataDict=json.loads(line.strip())

       if str(dataDict['group_id'])==str(gid):
          logger.info("found : ")
          logger.info(dataDict)
          dataDict['group_attribute']=attrs
          updatedgroup=dataDict
          result.append(dataDict)
     print("UPDATE a")
     print(result)

     writeNewOutput(result,jsonfile) 
     return updatedgroup 
             

def writeNewOutput(dataList, jsonfile, newline='\n'):
     with open(jsonfile, 'w') as outfile:
        for group1 in dataList:
          json.dump(jsonable_encoder(group1), outfile)

def dumpJson(data, jsonfile, mode='a+', newline='\n'):
    with open(jsonfile, mode) as outfile:
        json.dump(data, outfile)
        outfile.write(newline)

def updateJsonFile(data1, jsonfile, mode='w+', newline='\n'):
    dataList=loadJson(jsonfile)
    logger.info("data list : ")
    logger.info(dataList)
    logger.info("data1 : ")
    logger.info(data1)
    with open(jsonfile, mode) as outfile:
      for i, data_org in enumerate(dataList):
        #if i==0:
        #   outfile.truncate()
        logger.info("data org : ")
        logger.info(data_org)
        if str(data_org['group_id'])==str(data1['group_id']):
           dataList[i]=data1
        json.dump(jsonable_encoder(dataList[i]), outfile)
        outfile.write(newline)
