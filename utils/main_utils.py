import os
import pickle
import pandas as pd 
from dotenv import load_dotenv

def configure():
    load_dotenv()

def rfc_prediction(df:pd.DataFrame):
    with open('D:/Work/Projects/Astroid_danger_rating_system/Model/rfc_model.pkl','rb') as file : 
        rfc_model = pickle.load(file)

    prediction = rfc_model.predict(df)

    return prediction
    
