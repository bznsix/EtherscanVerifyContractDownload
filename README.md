# EtherscanVerifyContractDownload / 以太坊验证合约下载工具

一个用于从Etherscan以及兼容链下载已验证合约的Python脚本。  
A Python script to download verified contracts from Etherscan and compatible chains.

## 数据来源 / Data Source
您可以从以下链接下载合约CSV数据：  
You can download contract CSV data from:
[download / 下载](https://etherscan.io/myapikey_stats?apikey={YOUR_API_KEY})

注意：下载过程需要人机验证，目前尚未找到绕过方法。  
Note: The download process requires CAPTCHA verification, no bypass method available yet.

## 使用方法 / Usage
使用以下命令格式下载合约：  
Use the following command format to download contracts:

```bash
python download.py etherscan YOUR_API_KEY ./ethereum_contracts ./ethereum_contracts.csv
```

## 支持的链 / Supported Chains
支持所有基于以太坊模板的链，例如：  
Supports all Ethereum-based chains, such as:

- Ethereum (etherscan)
- BSC (bscscan)
- Polygon (polygonscan)
- Arbitrum (arbiscan)
- Optimism (optimistic.etherscan)
- 等其他兼容链 / And other compatible chains

## 功能特点 / Features
- 自动处理多文件合约  
  Automatically handles multi-file contracts
- 批量下载支持  
  Batch download support
- 按日期归档存储  
  Date-based archiving
- 多线程下载提高效率  
  Multi-threaded downloading for efficiency
