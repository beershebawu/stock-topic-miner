# Stock Topic Miner

基于免费数据源的A股/港股题材挖掘系统，通过政策、新闻等大数据分析，自动识别热点投资题材并推荐相关个股。

## 功能特点

- 📈 支持A股+港股数据
- 🆓 全部免费数据源（AKShare、Yahoo Finance、RSS）
- 🔍 政策解读 + 新闻聚类
- ⚖️ 个股-题材关联度评分
- 📊 Streamlit Web可视化界面
- 🐳 Docker一键部署
- ⏰ 自动定时采集与报告生成

## 快速启动

### 方式1：Docker Compose（推荐）

```bash
git clone https://github.com/你的用户名/stock-topic-miner.git
cd stock-topic-miner
docker compose up -d
# 访问 http://localhost:8501
```

### 方式2：Python虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py --web
```

## 配置说明

编辑 `config/topics.yaml` 自定义题材关键词，`config/settings.yaml` 调整调度时间。

## 免责声明

本项目仅供学习研究使用，不构成任何投资建议。股市有风险，投资需谨慎。

## 许可证

MIT License