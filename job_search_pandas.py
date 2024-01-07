import requests
import json
import os.path
import csv
import pandas as pd
from datetime import datetime

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


# Function to write search results to csv
def create_csv(filename):

    results = search_jobs("python", "London", 10)
    column_names = list(results[0].keys())
    
    csv_file_path = f'csv_files/{filename}.csv'

    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=column_names)
        
        writer.writeheader()
        writer.writerows(results)

    print(f'CSV file created at {csv_file_path}')

# create_csv("python_jobs")

def update_csv(filename):

    csv_file_path = f'csv_files/{filename}.csv'
    df = pd.read_csv(csv_file_path)
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    last_date = df['date'].max()

    results = search_jobs("python", "London", 10)

    count = 0
    for result in results:
        dt_date = datetime.strptime(result['date'], "%d/%m/%Y")
        if dt_date > last_date:
            with open(csv_file_path, 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(result.values())
            count += 1

    if count > 0:
        print(f"{count} New results added to {csv_file_path}.")
    else:
        print("No new jobs since last update")

update_csv("python_jobs")