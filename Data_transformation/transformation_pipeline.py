import pandas as pd 
import requests
from datetime import datetime ,timedelta
import os
import sys
from dotenv import load_dotenv
from logging_.logger import setup_logging
from exception.custom_astroid_exc import custom_exception

class Transformation_pipeline:
    def __init__(self,response,yesterday,today):
        self.response = response
        self.yesterday = yesterday
        self.today = today

    def get_intial_data(self)->pd.DataFrame:
            try:
                para1 = self.response.json()['near_earth_objects'][self.yesterday]
                para2 = self.response.json()['near_earth_objects'][self.today]
                df1 = pd.DataFrame(para1)
                df2 = pd.DataFrame(para2)
                return pd.concat([df1,df2],axis=0).reset_index()
            except Exception as e : 
                 raise custom_exception(e,sys)

    def get_diameter(self,df:pd.DataFrame)->pd.DataFrame:
        try:
            df['estimated_diameter_max'] = df['estimated_diameter'].apply(lambda x : x['kilometers']['estimated_diameter_max'])
            df.drop(['estimated_diameter'],axis=1, inplace=True)
            return df
        except Exception as e : 
             raise custom_exception(e,sys) 
    
    def get_close_approach_data(self,df:pd.DataFrame)->pd.DataFrame:
        try:
            df['relative_velocity_kmps']=df['close_approach_data'].apply(lambda x : float(x[0]['relative_velocity']['kilometers_per_second']))
            df['miss_distance_in_astronomical']=df['close_approach_data'].apply(lambda x : float(x[0]['miss_distance']['astronomical']))
            df.drop(['close_approach_data'],axis=1,inplace=True)
            return df
        except Exception as e : 
            raise custom_exception(e,sys)

    def get_details(self,df:pd.DataFrame)->pd.DataFrame:
            try:
                df['details'] = df['links'].apply(lambda x : x['self'])
                df.drop(['links'],axis=1,inplace=True)
                return df
            except Exception as e : 
                raise custom_exception(e,sys) 
    
    def get_orbital_data(self,df:pd.DataFrame)->pd.DataFrame:
        try:
            url2 = df['details'][0]
            res = requests.get(url2)
            final_dict = res.json()['orbital_data']
            del final_dict['orbit_class']
            oorb = list(final_dict.keys())
            temp = pd.DataFrame(columns=oorb)
            for i in range(df.shape[0]):
                url = df['details'][i]
                response = requests.get(url)
                req_left = int(response.headers.get('X-RateLimit-Remaining'))
                if req_left > 5 :
                    final_dict = response.json()['orbital_data']
                    del final_dict['orbit_class']
                    temp2 = pd.DataFrame(final_dict,index=[i])
                    temp = pd.concat([temp,temp2],axis=0)
                    print(f"left: {req_left} , iteration: {i}")
                else : 
                    break

            df = pd.concat([df,temp],axis=1)
            df.drop(['details'],axis=1,inplace=True)
            return df
        except Exception as e : 
            raise custom_exception(e,sys)
    
    def get_data_divide(self,df:pd.DataFrame):
        try:
        
            pred_df =df.loc[:,['absolute_magnitude_h', 'jupiter_tisserand_invariant',
            'eccentricity', 'inclination', 'ascending_node_longitude',
            'perihelion_distance', 'perihelion_argument', 'mean_anomaly',
            'estimated_diameter_max', 'relative_velocity_kmps',
            'miss_distance_in_astronomical']]
            
            pred_df = pred_df.astype('float64')

            info_df = df.drop(['neo_reference_id','nasa_jpl_url'],axis=1)

            return pred_df , info_df
        
        except Exception as e : 
            raise custom_exception(e,sys)



    def run_pipeline(self):
        setup_logging("intiating tranformation pipeline")
        df = self.get_intial_data()
        df = self.get_diameter(df)
        df = self.get_close_approach_data(df)
        df = self.get_details(df)
        df = self.get_orbital_data(df)
        pred_df , info_df = self.get_data_divide(df)
        return pred_df , info_df



