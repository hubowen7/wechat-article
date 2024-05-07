import requests

def print_api_response(num=1, fake_id='MzIzOTAzNzcwMg%3D%3D', token='1132247621'):
    """请求微信公众号API并打印完整的响应内容。"""
    headers = {
        "cookie": "appmsglist_action_3296508395=card; ua_id=lTGgGdyLybxOEU7YAAAAAMJOVJrBBZLXBApnARbsQFI=; _clck=1k8cupo|1|flj|0; wxuin=15005178482107; uuid=018b1cbb7cf1176ec22d471c71ea96ff; rand_info=CAESIHL0xgA81PdNaKTTdVYOA7HekCl6TYSbEYxj4FcdDWSq; slave_bizuin=3296508395; data_bizuin=3296508395; bizuin=3296508395; data_ticket=U+vcWHVEg0+pcO0Bmoz26ny44jJXfIReAqSdTjoB5oI6sRlPRPfPoxonsIfQ9FCp; slave_sid=OWs4M05iald4ZE1GMEZJaXNrR19YMTlOcnR3SDEySmJnWlZ3R0pGZGlBak9tNUF1WUl1cXlyUWcwSW1ac1U3RjVnWEk3YU9SNURJb2lNTlE5bHZHTXZnc2ZIb2tXd3BpRFlPcjROOHp4NHhPMl9CVGhrVTh6T1RWOWF6eVMwZkVwS09NQnRZa2QwWjYxMjRm; slave_user=gh_a5060f4cf8ae; xid=d6c06582ccb272f04b4cb58e0ca2f4cf; mm_lang=zh_CN; cert=rGzj7GlVHTknNEW4BcJxk84Nrw56rphG; _clsk=1crxk77|1715005217077|3|1|mp.weixin.qq.com/weheat-agent/payload/record",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'

    for page_number in range(num):
        params = {
            'action': 'list_ex',
            'begin': page_number * 5,  # 分页偏移量
            'count': '5',
            'fakeid': fake_id,
            'type': '9',
            'query': '',
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
        }
        response = requests.get(url, headers=headers, params=params)
        print(f"第 {page_number} 页响应内容:")
        if response.status_code == 200:
            print(response.json())  # 打印完整的JSON响应内容
        else:
            print(f"HTTP错误 {response.status_code}")

# 调用函数来打印响应
print_api_response(1)
