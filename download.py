import requests
import json
import os
import datetime
import pytz
import csv
import time
import argparse

def write_string_to_file(string_data, filename, save_folder):
    filename = filename + '.sol'
    # 获取当前UTC时间
    current_utc_time = datetime.datetime.utcnow()

    # 将UTC时间转换为北京时间
    beijing_timezone = pytz.timezone('Asia/Shanghai')
    current_beijing_time = current_utc_time.replace(tzinfo=pytz.utc).astimezone(beijing_timezone)

    # 格式化为字符串
    current_date = current_beijing_time.strftime('%Y-%m-%d')

    # Create the folder path with the current date as the folder name
    folder_path = os.path.join(save_folder, current_date)

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create the file path inside the folder with the provided filename
    file_path = os.path.join(folder_path, filename)

    # Write the string data to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(string_data)

def get_contract_source_code(chain_id, api_key, contract_address, save_folder):
    # 构建API的URL (V2) / Build API URL (V2)
    url = f"https://api.etherscan.io/v2/api?chainid={chain_id}&module=contract&action=getsourcecode&address={contract_address}&apikey={api_key}"
    
    try:
        # 发起HTTP GET请求 / Send HTTP GET request
        response = requests.get(url)
        data = response.json()

        # 检查API是否返回成功 / Check if API returns success
        if data["status"] == "1" and data["message"] == "OK":
            # 获取合约源代码 / Get contract source code
            source_code = data["result"][0]["SourceCode"]
            if len(source_code) == 0:
                # 仅返回状态，不打印日志 / Only return status, don't print log
                return False
            
            # 处理多文件合约 / Process multi-file contracts
            if source_code.startswith("{{") and source_code.endswith("}}"):
                print(f'处理到多文件合约：{contract_address}')
                data = json.loads(source_code[1:-1])
                sources_code = data['sources']
                sources = ''
                for item in list(sources_code.keys()):
                    sources += sources_code[item]['content'] + "\n\n"
                source_code = sources
            # 处理特殊格式的多文件合约 / Process special format multi-file contracts
            elif source_code.startswith("{\"") and source_code.endswith("}}"):
                print(f'处理到特殊格式多文件合约：{contract_address}')
                data = json.loads(source_code)
                sources_code = data
                sources = ''
                for item in sources_code:
                    sources += sources_code[item]['content'] + "\n\n"
                source_code = sources
                
            write_string_to_file(source_code, contract_address, save_folder)
            print(f"合约源代码已成功保存：{contract_address}")
            return True
        else:
            print(f"API返回错误 - 状态: {data['status']}, 消息: {data['message']}, 结果: {data.get('result', '无结果')}")
            # 仅返回状态，不打印日志 / Only return status, don't print log
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"请求出错：{e}")
        return False

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 链ID映射表
CHAIN_IDS = {
    "ethereum": "1",
    "optimism": "10",
    "bsc": "56",
    "polygon": "137",
    "arbitrum": "42161",
    "base": "8453",
    "zksync": "324",
    "fantom": "250",
    "avalanche": "43114",
    "cronos": "25"
}

def process_csv(csv_file, network_name, api_key, save_folder):
    # 获取对应的链ID / Get corresponding chain ID
    chain_id = CHAIN_IDS.get(network_name.lower(), "1")  # 默认为以太坊主网 / Default to Ethereum mainnet
    
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        contract_addresses = [row['ContractAddress'] for row in csv_reader]
    
    def process_batch(batch):
        results = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(get_contract_source_code, chain_id, api_key, address, save_folder) for address in batch]
            for future in as_completed(futures):
                results.append(future.result())
        return results

    for i in range(0, len(contract_addresses), 5):
        batch = contract_addresses[i:i+5]
        results = process_batch(batch)
        for address, success in zip(batch, results):
            if not success:
                print(f"无法获取合约 {address} 的源代码")
        time.sleep(1)  # 每处理5个请求后等待1秒，以符合API限速要求 / Wait 1 second after processing 5 requests to comply with API rate limits

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='下载合约源代码')
    parser.add_argument('network', help='区块链网络名称 (如ethereum, bsc, polygon等) / Blockchain network name (e.g., ethereum, bsc, polygon)')
    parser.add_argument('api_key', help='API密钥')
    parser.add_argument('save_folder', help='保存文件的路径')
    parser.add_argument('csv_file', help='CSV文件路径')
    
    args = parser.parse_args()
    
    process_csv(args.csv_file, args.network, args.api_key, args.save_folder)

    # print("命令行示例:")
    # print("python download.py ethereum YOUR_API_KEY ./ethereum_contracts ./contracts.csv")
    # print("python download.py bsc YOUR_API_KEY ./bsc_contracts ./contracts.csv")
