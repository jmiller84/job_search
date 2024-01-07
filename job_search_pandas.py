import requests
import json
import os
import os.path
import csv

# Function makes call to API and returns the results in a dict
def search_jobs(keywords, locationName, distance_in_miles):

    api_key = "440e3704-d856-440c-b07f-00ec507efd09"
    username = api_key
    password = ""

    url = f"https://www.reed.co.uk/api/1.0/search?keywords={keywords}&locationName={locationName}&distanceFromLocation={distance_in_miles}"

    response = requests.get(url,
                        auth=requests.auth.HTTPBasicAuth(
                            username, password))

    json_data = json.loads(response.text)
    return json_data['results']


results = search_jobs("python", "London", 10)
column_names = list(results[0].keys())

# Function to write search results to csv
def create_csv(filename):
    csv_file_path = f'csv_files/{filename}.csv'

    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=column_names)
        
        writer.writeheader()
        writer.writerows(results)

    print(f'CSV file created at {csv_file_path}')

create_csv("python_jobs")