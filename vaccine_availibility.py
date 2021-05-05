import requests
import json
import pandas as pd
import datetime
from fuzzywuzzy import fuzz
from fuzzywuzzy import process



class Covictory:
    """
    This call handles all the calls to api setu to get districts, state and vaccine availibility
    """

    def __init__(self, state):
        """

        constructor function to initialize variables
        """
        self.state = state
        self.state_id = ""

        self.districts_df = pd.DataFrame()
        

    

    def load_districts(self):
        """

        This function gets districts from state id
        """

        response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(self.state_id))

        if response.ok:

            df = pd.DataFrame(json.loads(response.text)["districts"])
            self.districts_df = df
    

    def initialize(self):
        """

        This function gets state ids from states
        """
        state_name = self.state

        state_name = state_name.lower()

        response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states")    

        if response.ok:

            df = pd.DataFrame(json.loads(response.text)["states"])            

            state = process.extractOne(state_name, df["state_name"].tolist()) # fuzzy match to get best state match            

            self.state_id = df.loc[df.state_name == state[0],["state_id"]].values[0][0]                 
        self.load_districts()

    

    def get_districtid_by_name(self, dname):

        """This function returns district id by name"""

        dname = process.extractOne(dname, self.districts_df["district_name"].tolist())

        district_id = self.districts_df.loc[self.districts_df.district_name == dname[0],["district_id"]].values[0][0] 

        return district_id


    def generate_dates(self):
        """
        This function generates next 20 days which will be used to find vaccine availibility in next 20 days
        """

        numdays = 20

        base = datetime.datetime.today()

        date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]

        date_str = [x.strftime("%d-%m-%Y") for x in date_list]

        return date_str


    def get_vaccine_availibility(self, district_name):
        dates = self.generate_dates()
        district_id = self.get_districtid_by_name(district_name)
        dfs = list()
        for v_date in dates:
            response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(district_id,v_date))

            if response.ok:

                df = pd.DataFrame(json.loads(response.text)["centers"])

                df["date"] = v_date
                dfs.append(df)

        if len(dfs)>0:
            final_df = pd.concat(dfs)

        return final_df



if __name__ == "__main__":

    cls_obj = Covictory("maharashtra")

    cls_obj.initialize()

    vac_df = cls_obj.get_vaccine_availibility("thane")

    vac_df = vac_df[["center_id", "name", "block_name", "district_name", "state_name", "pincode", "from", "to", "fee_type","date"]]    

    print(vac_df.head(10))

    print(vac_df.shape)


                



        



    



