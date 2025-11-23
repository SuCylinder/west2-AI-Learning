import requests
import pandas as pd
from pathlib import Path

'''用于获取项目列表'''

REQUEST_BODY = {
    "difficulty": [],
    "lang": "zh",
    "orgName": [],
    "pageNum": "1",
    "pageSize": "999",
    "programName": "",
    "programmingLanguageTag": [],
    "supportLanguage": [],
    "techTag": []
}

api_url = "https://summer-ospp.ac.cn/api/getProList"

response = requests.post(api_url,json=REQUEST_BODY)

csv_path = Path(__file__).parent / "project.csv"

data = response.json()

df = pd.DataFrame(data["rows"])

df.to_csv(csv_path,index=False,encoding="utf-8")

print(response.text)