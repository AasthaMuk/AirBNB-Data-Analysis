import pymongo
import pandas as pd
import streamlit as st
import time


class Extract:
    def connect_to_db(self):
        connection_string = "mongodb+srv://aastha:aastha123@airbnbcluster.b7zsalo.mongodb.net/"
        client = pymongo.MongoClient(connection_string)
        db = client.sample_airbnb
        col = db.listingsAndReviews
        return col
       
    
    @st.cache_data
    def convert_df(_self,df):
        return df.to_csv()


    def create_dataframe(self):
        rel_data = []
        with st.spinner('Connected to Mongo Cluster. Creating Dataframe  .....'):
            time.sleep(2)
            col = self.connect_to_db()
            for i in col.find():
                data = dict(Id = i['_id'],
                            Listing_url = i['listing_url'],
                            Name = i.get('name'),
                            Description = i['description'],
                            House_rules = i.get('house_rules'),
                            Property_type = i['property_type'],
                            Room_type = i['room_type'],
                            Bed_type = i['bed_type'],
                            Min_nights = int(i['minimum_nights']),
                            Max_nights = int(i['maximum_nights']),
                            Cancellation_policy = i['cancellation_policy'],
                            Accomodates = i['accommodates'],
                            Total_bedrooms = i.get('bedrooms'),
                            Total_beds = i.get('beds'),
                            Availability_365 = i['availability']['availability_365'],
                            Price = i['price'],
                            Security_deposit = i.get('security_deposit'),
                            Cleaning_fee = i.get('cleaning_fee'),
                            Extra_people = i['extra_people'],
                            Guests_included= i['guests_included'],
                            No_of_reviews = i['number_of_reviews'],
                            Review_scores = i['review_scores'].get('review_scores_rating'),
                            Amenities = ', '.join(i['amenities']),
                            Host_id = i['host']['host_id'],
                            Host_name = i['host']['host_name'],
                            Street = i['address']['street'],
                            Country = i['address']['country'],
                            Country_code = i['address']['country_code'],
                            Location_type = i['address']['location']['type'],
                            Longitude = i['address']['location']['coordinates'][0],
                            Latitude = i['address']['location']['coordinates'][1],
                            Is_location_exact = i['address']['location']['is_location_exact']
                )
                rel_data.append(data)
               
        df = pd.DataFrame(rel_data)
        df.to_csv("raw_data.csv",index=False)
        

        with st.spinner("Changing Datatype of some features..."):
            time.sleep(3)
            # checking Data types
            print(df.info())

            # The below features are in Decimal128 type hence changing it to relevant data types
            df.Price = df.Price.astype(str).astype(float)
            df.Security_deposit = df.Security_deposit[~df.Security_deposit.isna()].astype(str).astype(float)
            df.Cleaning_fee = df.Cleaning_fee[~df.Cleaning_fee.isna()].astype(str).astype(float)
            df.Extra_people = df.Extra_people.astype(str).astype(float)
            df.Guests_included = df.Guests_included.astype(str).astype(float)
            df.Review_scores = df.Review_scores.astype('Int64')


        with st.spinner("Checking for Null Values and filling them up ..."):
            time.sleep(3)
            # Checking for null values
            print(df.isna().sum())

            # Filling Total bedrooms with mode
            df.Total_bedrooms.fillna(df.Total_bedrooms.mode()[0],inplace=True)

            # Filling Total beds with median because data has outliers
            df.Total_beds.fillna(df.Total_beds.median(),inplace=True)
            df.Security_deposit.fillna(df.Security_deposit.median(),inplace=True)
            df.Cleaning_fee.fillna(df.Cleaning_fee.median(),inplace=True)
            df.Review_scores.fillna(df.Review_scores.median(),inplace=True)

            # Filling Empty values in Description and House rules columns
            df.Description.replace(to_replace='',value='No Description Provided',inplace=True)
            df.House_rules.replace(to_replace='',value='No House rules Provided',inplace=True)
            df.Amenities.replace(to_replace='',value='Not Available',inplace=True)


        with st.spinner("Checking for Duplicate Records and Cleaning them up..."):
            time.sleep(3)
            # Checking Duplicate records
            print(df[df.duplicated()])

            # Name Column has empty values and some duplicates hence dropping them
            df.drop(labels=list(df[df.Name.duplicated(keep=False)].index),inplace=True)

            df.reset_index(drop=True,inplace=True)

        st.success('Data is cleaned and ready for download ',icon='✅')
        return df
        
