import yaml
from typing import List, Dict, Set
from .policy_parser import PolicyParser
from .news_cluster import NewsCluster
from collections import defaultdict
from pathlib import Path

class TopicMatcher:
    """主题匹配器"""
    
    def __init__(self, topics_config: str = 'config/topics.yaml'):
        with open(topics_config, 'r', encoding='utf-8') as f:
            self.topics = yaml.safe_load(f)['topics']
        self.parser = PolicyParser()
        self.cluster = NewsCluster()
        
    def match_text(self, text: str) -> List[str]:
        """关键词匹配主题"""
        if not text:
            return []
        text_lower = text.lower()
        matched = []
        for topic_name, keywords in self.topics.items():
            for kw in keywords:
                if kw.lower() in text_lower:
                    matched.append(topic_name)
                    break
        return matched
        
    def extract_topics_from_news(self, news_list: List[Dict]) -> Dict[str, List[Dict]]:
        """从新闻列表中提取主题"""
        topic_news = defaultdict(list)
        for news in news_list:
            content = news.get('content', '') + ' ' + news.get('title', '')
            matched_topics = self.match_text(content)
            for t in matched_topics:
                topic_news[t].append(news)
        return dict(topic_news)
        
    def match_news_cluster(self, clusters: List[List[Dict]]) -> Dict[str, List[List[Dict]]]:
        """将新闻聚类匹配到主题"""
        topic_clusters = defaultdict(list)
        for cluster in clusters:
            if not cluster:
                continue
            # 取聚类第一条作为代表
            sample = cluster[0]
            content = sample.get('content', '') + ' ' + sample.get('title', '')
            matched_topics = self.match_text(content)
            for t in matched_topics:
                topic_clusters[t].append(cluster)
        return dict(topic_cluster)