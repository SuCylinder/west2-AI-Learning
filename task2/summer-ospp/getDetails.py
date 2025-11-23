import requests
from lxml import etree
import pandas as pd
from pathlib import Path
from time import sleep

'''用于获取项目细节'''

# 获取项目简介
def getIntroduce(response):
    html =  etree.HTML(response.json()["programDesc"])
    intr = html.xpath('//p/text() | //span/text()')
    introduce = ""
    for t in intr:
        t = t.strip()
        introduce+=t
    return introduce

# 获取产出要求
def getOutputRequirement(response):
    req = ""
    r = response.json()["outputRequirement"]
    for i in r:
        if not i:
            continue
        if "title" in i:
            req+=(i["title"]).strip()
    return req

# 通过接口请求项目详情的网页
def getProjectDetail(programCode):
    request_json = {
        "programId":programCode,
        "type":"org"
    }
    response = requests.post("https://summer-ospp.ac.cn/api/getProDetail",json=request_json)
    return response


if __name__ == "__main__":
    # 读取项目列表
    source_csv_path = Path(__file__).parent /"project.csv"
    df = pd.read_csv(source_csv_path,encoding="utf-8")
    datas = df.to_dict(orient="records")


    ans = []
    cnt = 1

    # 获取项目细节
    for project in datas:
        pro = {"programName":project["programName"],"difficulty":project["difficulty"],"techTag":project["techTag"]}
        print(f"获取 {project["programName"]} 的细节 {cnt} / {len(datas)}")
        cnt+=1
        currpro = getProjectDetail(project["programCode"])
        pro["Introduce"] = getIntroduce(currpro)
        pro["OutputRequirements"] = getOutputRequirement(currpro)
        ans.append(pro)

    # 保存内容
    ans_csv_path = Path(__file__).parent /"details.csv"
    df = pd.DataFrame(ans)
    df.to_csv(ans_csv_path,index=False,encoding="utf-8")