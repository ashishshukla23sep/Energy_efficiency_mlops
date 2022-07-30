import logging
from datetime import datetime
import os
import pandas as pd
from Energy_efficiency.constant import get_current_time_stamp
from Energy_efficiency.database.mangodb import MangoDbconnection
from Energy_efficiency.exception import EnergyException
import sys


LOG_DIR="logs"

def get_log_file_name():
    return f"log_{get_current_time_stamp()}.log"

LOG_FILE_NAME=get_log_file_name()

os.makedirs(LOG_DIR,exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE_NAME)



logging.basicConfig(filename=LOG_FILE_PATH,
filemode="w",
format='[%(asctime)s]^;%(levelname)s^;%(lineno)d^; %(filename)s^;%(funcName)s()^;%(message)s',
level=logging.INFO
)

def get_log_dataframe(file_path):
    data=[]
    with open(file_path) as log_file:
        for line in log_file.readlines():
            data.append(line.split("^;"))

    log_df = pd.DataFrame(data)
    columns=["Time stamp","Log Level","line number","file name","function name","message"]
    log_df.columns=columns
    
    log_df["log_message"] = log_df['Time stamp'].astype(str) +":$"+ log_df["message"]

    return log_df[["log_message"]]

def upload_log_to_db():
    try:
        data = []
        file_name = os.listdir(LOG_DIR)[-1]
        file_path = os.path.join(LOG_DIR,file_name)
        with open(file_path) as log_file:
            for line in log_file.readlines():
                data.append(line.split("^;"))

        log_df = pd.DataFrame(data)
        columns=["Time stamp","Log Level","line number","file name","function name","message"]
        log_df.columns=columns
        DB_NAME = 'ENERGY_EFFICICENCY'
        collection_name = 'logs'
        MangoDbconnection().insert_dataframe_into_collection(db_name=DB_NAME,collection_name= collection_name,data_frame=log_df)
    except Exception as e:
        raise EnergyException(e,sys) from e
    
    



