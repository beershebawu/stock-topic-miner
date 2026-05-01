\"\"\"
基础功能测试
\"\"\"


def test_imports():
    \"\"\"测试所有模块能否正常导入\"\"\"
    try:
        import src
        from src.data import models, database, collector
        from src.nlp import policy_parser, news_cluster, topic_matcher
        from src.engine import scorer, scheduler
        from src.web import app
        print("✅ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False


def test_config():
    \"\"\"测试配置文件加载\"\"\"
    import yaml
    with open("config/topics.yaml", "r", encoding="utf-8") as f:
        topics = yaml.safe_load(f)
    assert "新能源车" in topics["topics"]
    print(f"✅ 配置文件加载成功，包含 {len(topics['topics'])} 个题材")
    return True


if __name__ == "__main__":
    print("开始基础测试...")
    test_imports()
    test_config()
    print("测试完成！")
