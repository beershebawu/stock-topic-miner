import re
from typing import List, Dict
from ..data.models import Policy

class PolicyParser:
    """政策文件解析器"""
    
    INDUSTRY_KEYWORDS = {
        '新能源': ['新能源', '光伏', '风电', '氢能', '储能', '电动汽车', '锂电池', '动力电池', '充电桩'],
        '科技': ['人工智能', '芯片', '半导体', '5G', '云计算', '大数据', '区块链', '算力'],
        '医药': ['创新药', '医疗器械', '疫苗', '生物医药', '基因', '中医药', '临床试验'],
        '金融': ['银行', '保险', '证券', '期货', '金融科技', '数字货币', '监管'],
        '消费': ['零售', '电商', '物流', '旅游', '食品', '白酒', '餐饮'],
        '基建': ['交通', '建筑', '房地产', '城市更新', '新基建', '市政'],
        '制造': ['高端制造', '工业互联网', '机器人', '自动化', '新材料', '智能制造'],
        '农业': ['农业', '农村', '粮食', '种业', '乡村振兴'],
    }
    
    @staticmethod
    def extract_industries(text: str) -> List[str]:
        """从文本中提取行业关键词"""
        text_lower = text.lower()
        matched = []
        for industry, keywords in PolicyParser.INDUSTRY_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in text_lower:
                    matched.append(industry)
                    break
        return matched
        
    @staticmethod
    def analyze_sentiment(text: str) -> float:
        """简单的政策情感分析（0-1，1为最正面）"""
        positive_words = ['支持', '鼓励', '推动', '加快', '完善', '优化', '加强', '提升', '发展', '繁荣']
        negative_words = ['限制', '禁止', '取消', '缩减', '严格', '监管', '打击', '遏制']
        
        pos_count = sum(1 for w in positive_words if w in text)
        neg_count = sum(1 for w in negative_words if w in text)
        
        if pos_count + neg_count == 0:
            return 0.5
        return pos_count / (pos_count + neg_count)
        
    def parse(self, policy: Policy) -> Dict:
        """解析政策，返回分析结果"""
        text = policy.content
        if not text and policy.title:
            text = policy.title
            
        industries = self.extract_industries(text)
        sentiment = self.analyze_sentiment(text)
        
        return {
            'policy_id': policy.id,
            'title': policy.title,
            'industries': industries,
            'sentiment': sentiment,
            'impact': 'positive' if sentiment > 0.6 else 'negative' if sentiment < 0.4 else 'neutral'
        }