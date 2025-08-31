import sys
import pickle
from logging_.logger import setup_logging
from exception.custom_astroid_exc import custom_exception
from utils.training_utils import split_data  , give_training_report , train_model 
from Data_validation_pipeline.validation_pipeline import Validation_pipeline


class training_pipeline():
    
    def __init__(self,df):
        self.df = df
    
    def data_validation(self)->bool:
        valid_pipe = Validation_pipeline(self.df)
        is_validated = valid_pipe.run_validation_pipeline()
        return is_validated
    
    def training_report(self):

        try:
            setup_logging("intiating training pipeline")
            x_train,x_test,y_train,y_test = split_data(self.df,'is_potentially_hazardous',0.25)
            setup_logging("submiting report")
            give_training_report(x_train,x_test,y_train,y_test,algo='classifier')
          
        except Exception as e : 
            raise custom_exception(e,sys)

    def run_pipeline(self):
        try:
            setup_logging("intiaitng training pipeline")
            if self.data_validation():
                print("entered")
                model , params , score = train_model(self.df)
                with open('rfc_model.pkl','wb') as file : 
                    pickle.dump(model,file)

        except Exception as e : 
            raise custom_exception(e,sys)
