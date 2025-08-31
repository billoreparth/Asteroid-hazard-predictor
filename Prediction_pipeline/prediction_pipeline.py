import pandas as pd 
import sys
import os
import requests
from dotenv import load_dotenv 
from logging_.logger import setup_logging
from exception.custom_astroid_exc import custom_exception
from utils.main_utils import rfc_prediction
from Data_validation_pipeline.validation_pipeline import Validation_pipeline
from Data_transformation.transformation_pipeline import Transformation_pipeline
from datetime import datetime , timedelta
 
class Prediction_pipeline : 
    def __init__(self,response,yesterday:str,today:str):
        self.response = response
        self.yesterday = yesterday
        self.today = today

    def data_validation(self,df:pd.DataFrame)->bool:
        try:
            valid_pipe = Validation_pipeline(df)
            is_validated = valid_pipe.run_validation_pipeline()
            return is_validated
        except Exception as e : 
            raise custom_exception(e,sys)
    
    def data_transformation(self)->pd.DataFrame:
        try:
            trans_pipe = Transformation_pipeline(self.response,self.yesterday,self.today)
            pred_df , info_df = trans_pipe.run_pipeline()
            return pred_df,info_df
        except Exception as e : 
            raise custom_exception(e,sys)
    
        
    def run_pipeline(self):
        try:
            setup_logging("intiating prediction pipeline")
            pred_info , info_df = self.data_transformation()
            is_data_validated = self.data_validation(pred_info)
            if is_data_validated : 
                output = rfc_prediction(pred_info)
                pred_info['is_potential_hazard'] = output
                print(output)
            return pred_info , info_df 
        except Exception as e : 
            raise custom_exception(e,sys)

