import os
import aiohttp
import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
import threading

async def 调用本地AI提取英文名(文本):
    """使用本地AI服务提取英文名"""
    url = "http://localhost:5000/chat"
    提示词 = "你是一个专业的文本处理助手。请从以下公司名中提取英文名称（通常在括号内）。只需返回英文名称，一定不要含有中文，就只返回他英文名字，不需要其他解释。如果没有英文名称，请返回空字符串。"
    
    try:
        payload = {
            "问题": f"请提取这个公司名中的英文名称：{文本}\n{提示词}"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    结果 = await response.json()
                    print(f"API返回的原始结果: {结果}")
                    if 结果 and 'data' in 结果 and 'message' in 结果['data']:
                        return 结果['data']['message'].strip()
                    else:
                        print(f"返回结果格式不正确: {结果}")
                else:
                    print(f"API返回状态码: {response.status}")
    except Exception as e:
        print(f"处理文本时出错: {文本}, 错误: {str(e)}")
    return ""

async def process_hotel(hotel, lock, output_file, semaphore):
    """处理单个酒店名称并安全写入结果"""
    async with semaphore:  # 使用信号量控制并发
        try:
            hotel = hotel.strip()
            eng_name = await 调用本地AI提取英文名(hotel)
            print(f'原始名称: {hotel}, 提取的英文名: [{eng_name}]')
            
            print(f"是否有英文名: {bool(eng_name)}")
            print(f"是否包含字母: {any(c.isalpha() for c in eng_name)}")
            
            if eng_name and any(c.isalpha() for c in eng_name):
                with lock:  # 使用锁确保写入操作的原子性
                    with open(output_file, 'a', encoding='utf-8') as f:
                        f.write(f"{eng_name}\n")
                        print(f"成功写入文件: {eng_name}")
        except Exception as e:
            print(f"处理酒店名称时出错: {hotel}, 错误: {str(e)}")

async def main():
    当前目录 = os.path.dirname(os.path.abspath(__file__))
    输出文件 = os.path.join(当前目录, '酒店英文名.txt')
    
    # 清空输出文件
    with open(输出文件, 'w', encoding='utf-8') as f:
        pass
    
    # 读取文件
    with open(os.path.join(当前目录,'公司名.txt'), 'r', encoding='utf-8') as f:
        hotels = f.readlines()
    
    # 创建线程锁
    file_lock = threading.Lock()
    
    # 创建信号量限制并发数量为3
    semaphore = asyncio.Semaphore(100)
    
    # 创建任务列表
    tasks = [process_hotel(hotel, file_lock, 输出文件, semaphore) for hotel in hotels]
    
    # 使用 gather 替代 TaskGroup
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main()) 