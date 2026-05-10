import requests
import os
from PIL import Image, ImageDraw, ImageFont
import random
import datetime
import subprocess

# Pexels API Key
PEXELS_API_KEY = "4siZxCxKkFWzh2Fr2nxAHL5s54J37ZGzf4akGIBjiylrGP03T6DB2DjT"
SEARCH_TERMS = ["fire safety", "fire extinguisher"]

# 动态获取宿主机 IP
try:
    host_ip = "192.168.100.9"
    proxies = {
        "http": f"http://{host_ip}:7897",
        "https": f"http://{host_ip}:7897"
    }
    print(f"检测到宿主机 IP: {host_ip}，代理配置已就绪。")
except Exception as e:
    print(f"无法获取宿主机 IP，使用本地代理: {e}")
    proxies = {
        "http": "http://127.0.0.1:7897",
        "https": "http://127.0.0.1:7897"
    }

def download_image(url, save_path):
    """下载图片"""
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, headers=headers, stream=True, proxies=proxies, verify=False)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return True
    return False

def add_watermark(image_path, text, output_path):
    """在图片底部添加水印"""
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # 获取图片尺寸
    width, height = img.size

    # 创建半透明黑色遮罩条（底部 80px）
    overlay = Image.new('RGBA', (width, 80), (0, 0, 0, 180))
    img.paste(overlay, (0, height - 80), overlay)

    # 尝试加载中文字体
    try:
        # 尝试常见的中文字体路径
        font_paths = [
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
            '/System/Library/Fonts/PingFang.ttc',
            'C:\\Windows\\Fonts\\msyh.ttc'
        ]
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 24)
                break
        if font is None:
            raise Exception("No font found")
    except:
        # 如果找不到中文字体，使用默认字体
        font = ImageFont.load_default()

    # 绘制文字
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    text_y = height - 60

    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)

    # 保存图片
    img.save(output_path, quality=95)
    print(f"图片已保存到: {output_path}")

def get_pexels_image():
    """从 Pexels 获取随机图片"""
    # 随机选择搜索词
    search_term = random.choice(SEARCH_TERMS)

    # 调用 Pexels API
    url = f"https://api.pexels.com/v1/search?query={search_term}&per_page=15&orientation=landscape"
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, headers=headers, proxies=proxies, verify=False)

    if response.status_code == 200:
        data = response.json()
        photos = data.get('photos', [])

        if photos:
            # 随机选择一张图片
            random_photo = random.choice(photos)
            download_url = random_photo['src']['large2x']

            # 生成文件名
            today = datetime.datetime.now().strftime("%Y%m%d")
            image_filename = f"cover-{today}.jpg"

            # 创建 images 目录
            os.makedirs('images', exist_ok=True)
            image_path = os.path.join('images', image_filename)

            print(f"正在下载图片: {search_term}")
            if download_image(download_url, image_path):
                print(f"图片下载成功: {image_path}")

                # 添加水印
                output_path = image_path
                add_watermark(image_path, "武汉天洪消防设备 - 119hb.com.cn", output_path)

                return output_path
            else:
                print("图片下载失败")
        else:
            print("未找到搜索结果")
    else:
        print(f"API 调用失败: {response.status_code}")

    return None

if __name__ == "__main__":
    result = get_pexels_image()
    if result:
        print(f"\n✅ 成功！图片路径: {result}")
    else:
        print("\n❌ 失败")
