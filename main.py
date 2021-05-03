import requests
import os
import json

# inputs

date = "03-05-2021"     # will show you all the available centres 7 days from this date
age = 50        # enter age of the person to be vaccinated
state_name = "uttar pradesh"        # enter your state name
district_name = "gorakhpur"        # enter your district name

'''
For Andaman and Nicobar Islands enter state name state_name = "Andaman and Nicobar Islands" 
For Dadra and Nagar Haveli enter state name state_name = "Dadra and Nagar Haveli" 
For Daman and Diu enter state name state_name = "Daman and Diu" 
For Jammu and Kashmir enter state name state_name = "Jammu and Kashmir" 
'''

states = json.loads(os.popen("curl --silent https://cdn-api.co-vin.in/api/v2/admin/location/states").read())['states']
state_id = str(next(item for item in states if item["state_name"] == state_name.title())['state_id'])

districts = json.loads(os.popen("curl --silent https://cdn-api.co-vin.in/api/v2/admin/location/districts/"+state_id).read())['districts']
district_id = next(item for item in districts if item["district_name"] == district_name.capitalize())['district_id']


final_response = requests.get(
    "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict",
    params={
        'district_id': district_id,
        'date': date
    },
)
total_available_centres = 0
for centre in final_response.json()["centers"]:
    for details in centre["sessions"]:
        result = dict()
        if details['available_capacity'] > 0 and details["min_age_limit"] <= age:
            total_available_centres += 1
            result["name"] = centre["name"]
            result["block_name"] = centre["block_name"]
            result["pincode"] = centre["pincode"]
            result["min_age_limit"] = details["min_age_limit"]
            result["date"] = details["date"]
            result["available_capacity"] = details["available_capacity"]
            print(result, "\n")

if total_available_centres > 0:
    print("\nTotal available centres: ", total_available_centres)
    print("\nRegister your slot at https://www.cowin.gov.in/home")
else:
    print("\nNo vaccines available in this district, for the given age!")
