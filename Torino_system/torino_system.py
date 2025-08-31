import sys
import logging
import pandas as pd 
import numpy as np
from logging_.logger import setup_logging
from exception.custom_astroid_exc import custom_exception

class torino:
    def __init__(self,df:pd.DataFrame):
        self.df = df 
    
    def give_mass(self,density:int)->pd.DataFrame:
        '''density in kg/m^3'''
        self.df['mass'] = self.df['estimated_diameter_max'].apply(lambda x : density * ((4.0/3.0)*(np.pi)*(np.power((x*1000)/2,3))))
        return self.df  
    
    def give_energy(self)->pd.DataFrame:
        '''Energy in Megaton \n
        mass feature is removed after this'''
        try:
            self.df['energy'] = (0.5)*(self.df['mass'])*(self.df['relative_velocity_kmps']*1000) 
            self.df['energy']=self.df['energy']/(4.2 * (10**15))
            self.df.drop(['mass'],axis=True,inplace=True)
            return self.df 
        except Exception as e : 
            raise custom_exception(e,sys)
    
    def relative_probability(self)->pd.DataFrame:
        '''give relative probability with respect to miss distance'''
        try:
            scale = self.df['miss_distance_in_astronomical'].median()  
            self.df['probability'] = np.exp(- self.df['miss_distance_in_astronomical'] / scale)
            return self.df 
        except Exception as e : 
            raise custom_exception(e,sys)
    
    
    def torino_rating(self,p, E):
        try:
            logp = np.log10(p) if p > 0 else -np.inf
            logE = np.log10(E) if E > 0 else -np.inf
            
            # Rating 0
            if ( (logE + 1)/3 + (logp + 2)/2 < 0 ) or (logE < 0):
                return 0
            
            # Rating 1
            if ((logE + 1)/3 + (logp + 2)/2 >= 0 and logE >= 0 and
                (logE - 2)/3 + (logp + 2)/2 < 0 and logp < -2):
                return 1
            
            # Rating 2
            if ((logE - 2)/3 + (logp + 2)/2 >= 0 and
                (logE - 5)/3 + (logp + 2)/2 < 0 and logp < -2):
                return 2
            
            # Rating 3
            if (logp >= -2 and logE >= 0 and p < 0.99 and logE < 2):
                return 3
            
            # Rating 4
            if (logp >= -2 and logE >= 2 and
                (logE - 5)/3 + (logp + 2)/2 < 0 and p < 0.99):
                return 4
            
            # Rating 5
            if ((logE - 5)/3 + (logp + 2)/2 >= 0 and p < 0.99 and logE < 5):
                return 5
            
            # Rating 6
            if ((logE - 5)/3 + (logp + 2)/2 >= 0 and logp < -2):
                return 6
            
            # Rating 7
            if (logp >= -2 and logE >= 2 and logE >= 5 and p < 0.99):
                return 7
            
            # Rating 8
            if (p >= 0.99 and logE >= 0 and logE < 2):
                return 8
            
            # Rating 9
            if (p >= 0.99 and logE >= 2 and logE < 5):
                return 9
            
            # Rating 10
            if (p >= 0.99 and logE >= 5):
                return 10
            
            return 0  # fallback safety
        
        except Exception as e : 
            raise custom_exception(e ,sys )
    
    def give_torino_rating(self,density:int):
        '''density in kg/m^3\n
        probability in this system is a proxy of impact probability made with miss distance feature'''
        setup_logging("intiating torino rating system ",logging.INFO)
        try:
            df = self.give_mass(density)
            df = self.give_energy()
            df = self.relative_probability()
            df['danger_rating'] = df.apply(lambda row: self.torino_rating(row['probability'], row['energy']), axis=1)
            df.drop(['energy','probability'],axis = 1 , inplace=True)
            setup_logging("torino rating done , returning the dataframe ",logging.INFO)
            return df 
        except Exception as e : 
            raise custom_exception(e ,sys )
    

    def __str__(self):
        return 'working'

