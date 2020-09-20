import os
from os.path import join, dirname
from dotenv import load_dotenv

#https://stackoverflow.com/questions/41546883/can-somebody-explain-the-use-of-python-dotenv-module
#https://12factor.net/
env_path = join(dirname(__file__), '.env')
load_dotenv(env_path)

#examples : 
#jsonfile=os.environ.get("jsondata");
def getEnv(env_key):
 return os.environ.get(env_key)

s_output=join(getEnv("data_path"), getEnv("json_data"))
