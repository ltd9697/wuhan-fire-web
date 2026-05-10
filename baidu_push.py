import requests
import xml.etree.ElementTree as ET

def push_to_baidu():
    sitemap_path = 'sitemap.xml'
    api_url = 'http://data.zz.baidu.com/urls?site=https://www.119hb.com.cn&token=zAPJ9tnQwLWooTKw'
    
    try:
        # 解析 sitemap.xml
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        
        # 提取所有 <loc> 中的链接
        # 注意: 需要处理命名空间
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [url.find('ns:loc', namespace).text for url in root.findall('ns:url', namespace)]
        
        if not urls:
            print("没有找到链接。")
            return

        # 推送给百度
        headers = {'Content-Type': 'text/plain'}
        data = '\n'.join(urls)
        
        response = requests.post(api_url, headers=headers, data=data)
        
        print(f"推送结果: {response.status_code}")
        print(f"响应内容: {response.text}")
        
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    push_to_baidu()
