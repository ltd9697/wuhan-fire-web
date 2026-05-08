import requests
import json

def push_to_bing():
    # Bing IndexNow API Endpoint
    # 需要提供 host, key, keyLocation
    # 为简单起见，这里演示如何向 Bing 推送 URL
    # 在实际环境中，需要替换为您的 API Key
    
    api_url = 'https://api.indexnow.org/indexnow'
    site_url = 'https://www.119hb.com.cn'
    key = 'DD555841B105EE7F28CDD603B49531D9' # 可以在这里使用之前设置的验证码
    
    data = {
        "host": "www.119hb.com.cn",
        "key": key,
        "keyLocation": f"{site_url}/{key}.txt",
        "urlList": [
            f"{site_url}/",
            f"{site_url}/fire-renovation-standards.html"
        ]
    }
    
    try:
        response = requests.post(api_url, json=data, headers={'Content-Type': 'application/json'})
        print(f"Bing 推送状态码: {response.status_code}")
        if response.status_code == 200:
            print("Bing 推送成功")
        else:
            print(f"Bing 推送失败: {response.text}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    push_to_bing()
