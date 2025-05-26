# EtherscanVerifyContractDownload / 以太坊验证合约下载工具

一个用于从Etherscan以及兼容链下载已验证合约的Python脚本。  
A Python script to download verified contracts from Etherscan and compatible chains.

## 更新说明 / Update Notes
该项目已升级到支持Etherscan V2 API，现在所有区块链查询均通过统一的API端点和chainId参数完成。  
This project has been upgraded to support Etherscan V2 API, all blockchain queries are now handled through a unified API endpoint with chainId parameter.

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
python download.py <network> YOUR_API_KEY ./save_folder ./contracts.csv
```

示例 / Examples:
```bash
python download.py ethereum YOUR_API_KEY ./ethereum_contracts ./contracts.csv
python download.py bsc YOUR_API_KEY ./bsc_contracts ./contracts.csv
```

## 支持的链 / Supported Chains
支持多种区块链网络，通过网络名称参数指定：  
Supports multiple blockchain networks, specified by network name parameter:

- Ethereum (ethereum, chainId: 1)
- BSC (bsc, chainId: 56)
- Polygon (polygon, chainId: 137)
- Arbitrum (arbitrum, chainId: 42161)
- Optimism (optimism, chainId: 10)
- Base (base, chainId: 8453)
- zkSync Era (zksync, chainId: 324)
- Fantom (fantom, chainId: 250)
- Avalanche (avalanche, chainId: 43114)
- Cronos (cronos, chainId: 25)

## 功能特点 / Features
- 支持Etherscan V2 API，统一访问多链  
  Supports Etherscan V2 API for unified multi-chain access
- 自动处理多文件合约  
  Automatically handles multi-file contracts
- 批量下载支持  
  Batch download support
- 按日期归档存储  
  Date-based archiving
- 多线程下载提高效率  
  Multi-threaded downloading for efficiency

## V1到V2 API迁移说明 / V1 to V2 API Migration Notes
Etherscan已将其API从V1升级到V2，主要变化：

1. 所有请求现在通过单一端点访问: `https://api.etherscan.io/v2/api`
2. 使用chainId参数指定目标区块链: `?chainid=<chain_id>`
3. 不再需要为不同链使用不同的域名，如bscscan.com、polygonscan.com等

Etherscan has upgraded its API from V1 to V2, key changes:

1. All requests now go through a single endpoint: `https://api.etherscan.io/v2/api`
2. Use chainId parameter to specify target blockchain: `?chainid=<chain_id>`
3. No need for different domains for different chains (e.g., bscscan.com, polygonscan.com)
