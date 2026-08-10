# 国家排污许可申请公开平台 - 企业排污许可证副本批量下载工具

基于 Python + `curl_cffi` + `Pillow` 构建的多省份企业排污许可证副本（PDF）自动化下载工具。

## 项目目录结构

```
PDP-download/
├── main.py                     # 程序唯一主入口脚本
├── requirements.txt            # 项目依赖包配置文件
├── README.md                   # 项目使用说明文档
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

## 环境准备与依赖安装

### 1. 创建 Python 虚拟环境

在项目根目录下打开终端/命令行，执行以下命令创建虚拟环境：

```bash
python -m venv .venv
```

### 2. 激活虚拟环境

- **Windows (PowerShell)**:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Windows (CMD)**:
  ```cmd
  .\.venv\Scripts\activate.bat
  ```
- **Linux / macOS**:
  ```bash
  source .venv/bin/activate
  ```

### 3. 安装项目依赖

激活虚拟环境后，安装项目所需的第三方依赖包（包含 `curl_cffi` 和 `Pillow`）：

```bash
pip install -r requirements.txt
```

---

## 使用说明与运行示例

在已激活虚拟环境的终端中，运行 `main.py` 脚本：

### 1. 下载吉林省数据（默认）
```bash
python main.py --start-page 1 --max-pages 5
```

### 2. 下载其他省份数据（如广东省、北京市、四川省等）
```bash
# 广东省
python main.py --province 广东 --start-page 1 --max-pages 5

# 北京市
python main.py -p 北京 -s 1 -m 3

# 四川省
python main.py -p 四川 -s 1 -m 5
```

### 3. 备用参数选项

| 参数 | 缩写 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `--province` | `-p` | `吉林` | 省份名称或 12 位行政区划编码（如 `广东`、`北京`、`四川`、`220000000000`） |
| `--start-page` | `-s` | `1` | 起始页码 |
| `--max-pages` | `-m` | `5` | 结束页码 |
| `--proxy` | | `""` | 可选。HTTP/HTTPS 代理服务 URL（如 `http://127.0.0.1:7897`，通常无需设置，直接直连即可） |
