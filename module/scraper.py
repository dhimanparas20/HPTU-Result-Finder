import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from os import system

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

def scrape_all_data():
    url = f"https://himachal-pradesh.indiaresults.com/himtu/default.aspx"

    try:   
        response = requests.get(url,headers=HEADERS)    
        if response.status_code != 200:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            fetched_data = []
            fetched_dev = soup.find_all('tr')
            for data in fetched_dev:
                    all_span = data.find_all("span")
                    try:
                        date = all_span[0].text
                        result_of = all_span[1].text
                        url = all_span[1].find('a')['href']

                        if "Removed" not in result_of:
                            data_dict = {"result_of":result_of,"date":date,"url":url}
                            fetched_data.append(data_dict)
                    except:
                        pass
            return fetched_data           
        except Exception as e:
            print(f"Exception occurred: {e}")    
    except Exception as e:
            print(f"Exception occurred: {e}")         

def filter_data(data,filters):
    # Filtering based on keywords in the 'result_of' field
    filtered_data = [
        item for item in data
        if all(keyword in item['result_of'].upper() for keyword in filters)
    ]
    resturn_set = []
    for item in filtered_data:
        resturn_set.append(item)
    return resturn_set 

def extract_id_from_url(url):
    # Parse the URL and extract query parameters
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    # Extract the 'id' parameter value
    id_value = query_params.get('id', [None])[0]
    
    return id_value   

def fetch_result_by_rollNo(rollNo,id):
    url = "https://results.indiaresults.com/hp/himtu/result3/result.aspx"
    # Define the POST request body data
    data = {
        "RollNo": rollNo,
        "txtName": "",
        "id": id
    }

    # Send the POST request
    response = requests.post(url, data=data)
    op = response.text

    return op

    # # Save the response content to a file named op.html
    # with open("op.html", "w", encoding="utf-8") as file:
    #     file.write(op)

    # print("Response saved to op.html")

def fetch_result_by_name(name,id):
    url = "https://results.indiaresults.com/hp/himtu/result3/name-results.aspx"

    data = {
        "__VIEWSTATE": "/wEPDwUKMTA4OTgzNDMwNGRk9Qx7Q7AxJ8UcVEmRv9BFDo+NeYd29fczQSOs2Gcyxms=",
        "__VIEWSTATEGENERATOR": "7E0BBA3D",
        "RollNo": "",
        "txtName": name,
        "id": id
    }

    # Send the POST request
    response = requests.post(url, data=data)
    op = response.text
    return op

    # # Save the response content to a file named op.html
    # with open("op.html", "w", encoding="utf-8") as file:
    #     file.write(op)

    # print("Response saved to op.html")    


    