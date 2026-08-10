# 国家排污许可申请公开平台 - 企业排污许可证副本批量下载工具

基于 Python + `curl_cffi` + `Pillow` 构建的多省份企业排污许可证副本（PDF）自动化下载工具。

## 项目目录结构

```
PDP-download/
├── main.py                     # 程序唯一主入口脚本
├── app/                        # 核心程序模块
│   ├── config.py               # 全国行政区划代码及配置项
│   └── downloader.py           # 核心防封锁、多省份爬虫及图像转 PDF 逻辑
├── pdf_downloads/              # PDF 副本下载导出目录 (按省份子文件夹归档)
│   ├── 吉林/
│   ├── 广东/
│   └── ...
├── manifest/                   # 抓取元数据及数据清单
│   └── downloads_manifest.csv  # 下载清单记录表
└── temp_scratch/               # 开发调试过程中的中间文件与测试脚本
```

## 使用说明

### 环境准备

使用 `bidding-files-download` 项目中配置好的 Python 解释器：
`c:\Users\hubin\workspace\bidding-files-download\.venv-build\Scripts\python.exe`

### 运行命令

#### 1. 下载吉林省数据（默认）
```bash
c:\Users\hubin\workspace\bidding-files-download\.venv-build\Scripts\python.exe main.py --start-page 1 --max-pages 5
```

#### 2. 下载其他省份数据（如广东省、北京市、四川省等）
```bash
# 广东省
c:\Users\hubin\workspace\bidding-files-download\.venv-build\Scripts\python.exe main.py --province 广东 --start-page 1 --max-pages 5

# 北京市
c:\Users\hubin\workspace\bidding-files-download\.venv-build\Scripts\python.exe main.py -p 北京 -s 1 -m 3

# 四川省
c:\Users\hubin\workspace\bidding-files-download\.venv-build\Scripts\python.exe main.py -p 四川 -s 1 -m 5
```

#### 3. 指定代理 IP 节点运行
```bash
c:\Users\hubin\workspace\bidding-files-download\.venv-build\Scripts\python.exe main.py -p 吉林 --proxy http://127.0.0.1:7897
```
