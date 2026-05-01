from typing import List, Dict, Tuple
from datetime import datetime
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class NewsCluster:
    """新闻聚类器"""
    
    def __init__(self, stopwords_path: str = None):
        self.stopwords = set()
        if stopwords_path:
            try:
                with open(stopwords_path, 'r', encoding='utf-8') as f:
                    self.stopwords = set([line.strip() for line in f])
            except:
                pass
                
    def preprocess(self, text: str) -> str:
        """中文分词并去停用词"""
        if not text:
            return ""
        words = jieba.cut(text)
        filtered = [w for w in words if w.strip() and w not in self.stopwords and len(w) > 1]
        return ' '.join(filtered)
        
    def cluster_by_similarity(self, news_list: List[Dict], threshold: float = 0.3) -> List[List[Dict]]:
        """基于TF-IDF余弦相似度聚类"""
        if not news_list:
            return []
            
        texts = [self.preprocess(n.get('content', '')[:500] + ' ' + n.get('title', '')) for n in news_list]
        try:
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(texts)
        except ValueError:
            # 如果所有文本都为空，返回单条聚类
            return [[n] for n in news_list]
        
        n = len(news_list)
        visited = [False] * n
        clusters = []
        
        for i in range(n):
            if visited[i]:
                continue
            cluster = [news_list[i]]
            visited[i] = True
            for j in range(i + 1, n):
                if not visited[j]:
                    sim = cosine_similarity(tfidf_matrix[i], tfidf_matrix[j])[0][0]
                    if sim > threshold:
                        cluster.append(news_list[j])
                        visited[j] = True
            clusters.append(cluster)
            
        return clusters
        
    def calculate_cluster_hotness(self, cluster: List[Dict]) -> float:
        """计算聚类热度"""
        count = len(cluster)
        sources = len(set(n.get('source', '') for n in cluster))
        # 基于新闻数量、来源多样性、时间（简化）
        return count * 0.6 + sources * 0.4