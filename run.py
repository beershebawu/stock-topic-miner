#!/usr/bin/env python
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="股票题材挖掘系统")
    parser.add_argument("--web", action="store_true", help="启动Web界面")
    parser.add_argument("--collect", action="store_true", help="手动数据采集")
    parser.add_argument("--report", action="store_true", help="生成报告")
    
    args = parser.parse_args()
    
    if args.collect:
        from src.data.collector import DataCollector
        collector = DataCollector()
        collector.collect_all()
        print("✅ 数据采集完成")
    elif args.report:
        from src.engine.scorer import StockScorer
        scorer = StockScorer()
        results = scorer.generate_report()
        print(f"✅ 报告生成完成，筛选出 {len(results)} 只股票")
    elif args.web:
        from src.web.app import main
        main()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()