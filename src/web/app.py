import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
from src.data.database import Database
from src.engine.scorer import StockScorer
from src.nlp.topic_matcher import TopicMatcher
from src.data.collector import DataCollector

st.set_page_config(
    page_title="股票题材挖掘系统",
    page_icon="📈",
    layout="wide"
)

DB = Database()

def main():
    st.title("📈 股票题材挖掘系统")
    st.markdown("---")
    
    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 控制面板")
        if st.button("🔄 刷新数据", type="primary", use_container_width=True):
            with st.spinner("正在采集数据..."):
                collector = DataCollector()
                collector.collect_all()
            st.success("数据采集完成！")
            
        st.markdown("---")
        st.subheader("📊 数据状态")
        # 显示最后更新时间
        try:
            # 从数据库获取最新股票更新时间
            import sqlite3
            conn = sqlite3.connect('data/db.sqlite')
            cur = conn.cursor()
            cur.execute("SELECT MAX(updated_at) FROM stocks")
            last_update = cur.fetchone()[0]
            conn.close()
            if last_update:
                st.info(f"最后更新: {last_update}")
            else:
                st.warning("暂无数据，请点击刷新")
        except Exception as e:
            st.error(f"数据库错误: {e}")
    
    # 主界面
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔥 热门题材榜单")
        matcher = TopicMatcher()
        topics = list(matcher.topics.keys())
        
        # 展示题材卡片
        for i, topic in enumerate(topics[:15]):
            with st.container():
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"**{i+1}. {topic}**")
                with col_b:
                    st.button("查看", key=f"btn_{topic}", help=f"查看{topic}相关个股")
                st.divider()
                
    with col2:
        st.subheader("📈 个股推荐")
        scorer = StockScorer()
        recommendations = scorer.generate_report(top_n=10)
        
        if recommendations:
            df = pd.DataFrame([
                {
                    '股票': f"{r['stock'].name}({r['stock'].code})",
                    '题材': r['topic'],
                    '分数': r['score'],
                    '新闻数': r.get('news_count', 0)
                }
                for r in recommendations
            ])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("暂无推荐，请点击刷新数据")
            
    # 底部：最新新闻和政策
    st.subheader("📰 最新政策解读")
    try:
        # 从数据库读取最新政策
        import sqlite3
        conn = sqlite3.connect('data/db.sqlite')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('''
            SELECT * FROM policies 
            ORDER BY published_at DESC 
            LIMIT 5
        ''')
        rows = cur.fetchall()
        if rows:
            for row in rows:
                with st.expander(f"{row['title']} ({row['source']})"):
                    st.write(row['content'][:500] + "...")
                    st.markdown(f"[原文链接]({row['url']})")
        else:
            st.info("暂无政策数据")
        conn.close()
    except Exception as e:
        st.error(f"读取政策数据失败: {e}")
    
    st.subheader("🔥 新闻热点聚类")
    try:
        # 读取最新新闻（最近1小时）
        from src.data.database import Database
        db = Database()
        cutoff = datetime.now().timestamp() - 3600
        import sqlite3
        conn = sqlite3.connect('data/db.sqlite')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('''
            SELECT * FROM news 
            WHERE published_at > datetime(?, 'unixepoch')
            ORDER BY published_at DESC 
            LIMIT 20
        ''', (cutoff,))
        rows = cur.fetchall()
        if rows:
            # 简单按来源分组显示
            sources = {}
            for row in rows:
                src = row['source']
                if src not in sources:
                    sources[src] = []
                sources[src].append(row)
            for src, items in sources.items():
                with st.expander(f"{src} ({len(items)} 条)"):
                    for item in items:
                        st.markdown(f"**{item['title']}**")
                        st.caption(item['url'])
        else:
            st.info("暂无最新新闻")
        conn.close()
    except Exception as e:
        st.error(f"读取新闻数据失败: {e}")

if __name__ == "__main__":
    main()