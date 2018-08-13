import requests
for x in range(1,469):
    url = "https://assets.documentcloud.org/documents/1505102/pages/slahi-unclassified-manuscript-scan-p"+str(x)+"-normal.gif"
    response = requests.get(url)
    if response.status_code == 200:
        with open("/home/justin/Desktop/Diary/"+str(x)+".gif", 'wb') as f:
            f.write(response.content)