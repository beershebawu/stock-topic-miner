from typing import List, Dict
from datetime import datetime, timedelta
from ..data.database import Database
from ..nlp.topic_matcher import TopicMatcher
from ..data.models import Stock
import numpy as np

class StockScorer:
    """股票评分引擎"""
    
    def __init__(self):
        self.db = Database()
        self.matcher = TopicMatcher()
        self.weights = {
            'industry_match': 0.30,
            'news_volume': 0.35,
            'concept_overlap': 0.20,
            'turnover_ratio': 0.10,
            'market_cap_penalty': 0.05
        }
        
    def get_active_topics(self) -> Dict[str, List[Dict]]:
        """获取当前活跃主题（基于新闻和政策）"""
        # 获取最近24小时新闻
        news_list = self.db.get_news_since(hours=24)
        if not news_list:
            # 如果没有新闻，使用预定义热门主题
            return {k: [] for k in self.matcher.topics.keys()}
            
        # 将新闻对象转为字典以便处理
        news_dicts = [
            {
                'title': n.title,
                'content': n.content,
                'source': n.source,
                'url': n.url,
                'published_at': n.published_at
            }
            for n in news_list
        ]
        # 提取主题新闻
        topic_news = self.matcher.extract_topics_from_news(news_dicts)
        return topic_news
        
    def calculate_stock_score(self, stock: Stock, topic_name: str, news_volume: int) -> float:
        """计算单股票-主题分数"""
        score = 0.0
        
        topic_keywords = self.matcher.topics.get(topic_name, [])
        
        # 1. 行业匹配度
        industry_match = 0
        stock_industry_lower = stock.industry.lower() if stock.industry else ""
        for kw in topic_keywords:
            if kw.lower() in stock_industry_lower:
                industry_match = 1
                break
        score += industry_match * self.weights['industry_match'] * 100
        
        # 2. 新闻热度（基于该主题下新闻总数，简化）
        # 这里直接用传入的该主题的新闻数作为热度指标
        news_score = min(news_volume * 10, 100)
        score += news_score * self.weights['news_volume']
        
        # 3. 概念叠加
        if stock.concepts:
            concept_overlap = len(set(stock.concepts) & set(topic_keywords))
        else:
            concept_overlap = 0
        score += concept_overlap * 5 * self.weights['concept_overlap'] * 100
        
        # 4. 换手率活跃度
        if stock.turnover > 0.05:  # 换手率>5%
            score += 100 * self.weights['turnover_ratio']
            
        # 5. 市值惩罚（这里简化，假设小盘加分）
        # 可根据市值数据调整，暂时用固定惩罚
        score -= self.weights['market_cap_penalty'] * 20
        
        return min(score, 100)
        
    def generate_report(self, top_n: int = 20) -> List[Dict]:
        """生成投资主题报告"""
        print("📊 生成投资报告...")
        active_topics = self.get_active_topics()
        
        recommendations = []
        stocks = self.db.get_latest_stocks(limit=500)
        
        for topic_name, topic_news in active_topics.items():
            news_count = len(topic_news)
            for stock in stocks:
                score = self.calculate_stock_score(stock, topic_name, news_count)
                if score > 30:  # 阈值，可调整
                    recommendations.append({
                        'stock': stock,
                        'topic': topic_name,
                        'score': round(score, 1),
                        'reason': f"行业匹配度+{score:.1f}",
                        'news_count': news_count
                    })
                    
        # 按分数排序
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:top_n]