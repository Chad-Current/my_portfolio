# import numpy as np
import pandas as pd
pd.set_option('max_columns',100)
from pprint import pprint as pp
# import warnings
# warnings.filterwarnings(action='ignore',message='',category='')

"""
This Program is meant to tokenize the customer written reviews and the find the correlation between key descrtiptive
words thus finding any correlation or lack there of 
"""

class SeattleAirBNB:

    def __init__(self,read=False,clean=False):
        """
        Collection of the csv files are located in main directory file
        """
        self.listings = pd.read_csv('listings.csv')
        self.listings = self._clean_listings()
        self.reviews = pd.read_csv('reviews.csv')

        try:
            self.df = pd.merge(left=self.listings, right=self.reviews, left_on='id', right_on='listing_id')

        except(TypeError) as e:
            print(e)

        if read:
            self._read_data(self.df)

        if clean:
            df_numerical, df_categorical = self._clean_data(self.df)

    def _read_data(self, object, info=False, describe=False, head=True):
        """
        Take a quick peek at the import data from all the CSVs'
        :return: None
        """
        if info:
            pp(object.info())
        if describe:
            (object.describe())
        if head:
            pp(object.head())

    def _clean_data(self,object):

        """
        Trying to clean up the dataframe of any duplicates or missing values, also looking for missed columns that should
        be numerical i.e. host_response_rate = % where it should be a decimal percentage
        """

        try:
            object.drop_duplicates(inplace=True)
            df_num = object.select_dtypes(exclude=['object'])
            df_cat = object.select_dtypes(include=['object'])
            df_num.fillna(0,inplace=True)
            df_cat.fillna('Missing',inplace=True)

            return df_num, df_cat

        except(ValueError,TypeError,KeyError) as e:
            print('failed to clean data',e)

    def _strip_percent(self,x):
        if isinstance(x,float):
            x = 0
            return x
        elif isinstance(x,str):
            x = x.strip('%')
            x = float(x)/100
            return x
        else:
            return x

    def _clean_listings(self):
        """
        Making sure all columns from the listings.csv are cleaned and converted to proper numerical form
        """
        self.listings.price = self.listings.price.apply(lambda x: x.replace("$",""))
        self.listings.price = self.listings.price.apply(lambda x: x.replace("'",""))
        self.listings.price = self.listings.price.apply(lambda x: x.replace(",",""))
        self.listings.host_acceptance_rate = self.listings.host_acceptance_rate.apply(self._strip_percent)
        self.listings.host_response_rate = self.listings.host_response_rate.apply(self._strip_percent)
#         mask = ((self.listings.host_response_rate>0.0) & (self.listings.host_response_rate<1.0))
        return self.listings

if __name__=='__main__':
    S = SeattleAirBNB(read=False,clean=True)