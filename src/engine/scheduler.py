from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import time
import yaml
from src.data.collector import DataCollector
from src.engine.scorer import StockScorer
from src.web.app import refresh_data

class TaskScheduler:
    def __init__(self, config_path: str = 'config/settings.yaml'):
        self.scheduler = BackgroundScheduler()
        self.collector = DataCollector()
        self.scorer = StockScorer()
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        self._setup_jobs()
        
    def _setup_jobs(self):
        sched_cfg = self.config['scheduler']
        # 数据采集任务（每天收盘后）
        self.scheduler.add_job(
            self.job_collect_data,
            CronTrigger.from_crontab(sched_cfg['collect_crontab']),
            id='collect_data',
            name='每日数据采集'
        )
        # 新闻采集（每30分钟）
        self.scheduler.add_job(
            self.job_collect_news,
            CronTrigger.from_crontab(sched_cfg['news_crontab']),
            id='collect_news',
            name='新闻采集'
        )
        # 报告生成（每天18:00）
        self.scheduler.add_job(
            self.job_generate_report,
            CronTrigger.from_crontab(sched_cfg['report_crontab']),
            id='generate_report',
            name='生成投资报告'
        )
        
    def job_collect_data(self):
        print(f"[{datetime.now()}] 开始执行数据采集任务...")
        self.collector.collect_all()
        
    def job_collect_news(self):
        print(f"[{datetime.now()}] 开始采集新闻...")
        self.collector.collect_news()
        self.collector.collect_policies()
        
    def job_generate_report(self):
        print(f"[{datetime.now()}] 生成投资报告...")
        results = self.scorer.generate_report()
        print(f"  筛选出 {len(results)} 只推荐股票")
        # 这里可以写入数据库或文件，供Web界面读取
        
    def start(self):
        print("✅ 调度器启动，任务:")
        for job in self.scheduler.get_jobs():
            print(f"  - {job.name}: {job.trigger}")
        self.scheduler.start()
        try:
            while True:
                time.sleep(60)
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()

def start_scheduler():
    scheduler = TaskScheduler()
    scheduler.start()