import requests
import json

data = {"data" : "24.3"}
data_json = json.dumps(data)

# Accept: application/json


headers = {'Accept': 'application/json'}

resp_name = requests.get("https://api.elsevier.com/content/author/author_id/7004322609")
if resp.status_code != 200:
    # This means something went wrong.
    print('life is hard')
    # raise ApiError('GET /tasks/ {}'.format(resp_name.status_code))

print (resp)
# print (resp_name.status_code)

# response_name = resp_name.json()
# print (response_name['items'][0]['name']['lastName'])




#
# resp_publications = requests.get('https://research.vu.nl/ws/api/59/research-outputs/6e2aeddc-45c1-4074-974a-b9577f40e126?apiKey=1aecc9b3-0b58-4e00-b757-c1a8026cbbfd',  headers=headers)
# if resp_publications.status_code != 200:
#     # This means something went wrong.
#     print('life is hard')
#     raise ApiError('GET /tasks/ {}'.format(resp_publications.status_code))
#
# print (resp_publications)
# print (resp_publications.status_code)
#
# response_publications = resp_publications.json()
# print (response_publications['items'][0]['name']['firstName'])



# for todo_item in resp.json():
#
#     print('{} {}'.format(todo_item['id'], todo_item['summary']))