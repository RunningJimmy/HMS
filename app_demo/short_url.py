import requests,json

long_url = "http://tjbg.nbmzyy.com:5005/api/report/down/pdf/155110185"
# querystring = {"url":long_url}
#
# url = "http://suo.im/api.php"
#
# response = requests.request("GET", url, params=querystring)
#
# print(response.text)

url = "http://10.7.200.101:5005/api/forward"
keys = {'tjbh': '155110185','action':'url'}
querystring = {"url":long_url}
response = requests.post(url, params = keys, data = json.dumps(querystring))

print(response.text)
