import sys
import pandas as pd 
from logging_.logger import setup_logging
from exception.custom_astroid_exc import custom_exception
from pydantic import ValidationError
from .pydantic_model import DataFrameRowModel

class Validation_pipeline():
    def __init__(self,df:pd.DataFrame):
        self.df = df

    def is_column_correct(self):
        try:
            columns = self.df.shape[1]
            if columns == 11 : 
                return True
            else : 
                return False
        except Exception as e : 
            raise custom_exception(e,sys) 
    def has_null(self):
        try:
            null = int(self.df.isna().sum().sum())
            if null == 0:
                return False
            else : 
                return True
        except Exception as e : 
            raise custom_exception(e,sys)

    
    def run_validation_pipeline(self):
        setup_logging("intiating validation pipeline")
        try:
            if self.is_column_correct() == True and self.has_null() == False :
                    setup_logging("validation successfull")
                    return True            
            return False
        except Exception as e : 
            raise custom_exception(e,sys)


