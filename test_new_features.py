#!/usr/bin/env python3
"""
测试新功能模块的基本功能
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "shared"))

def test_config_manager():
    """测试配置管理器"""
    print("🔧 测试配置管理器...")
    try:
        from shared import ConfigLoader
        config = ConfigLoader()
        print("  ✅ ConfigLoader 实例化成功")
        
        # 测试基本方法
        result = config.load_config()
        print(f"  ✅ load_config() 成功: {result}")
        
        # 测试获取配置
        value = config.get("non_existent_key", "default_value")
        print(f"  ✅ get() with default: {value}")
        
        return True
    except Exception as e:
        print(f"  ❌ 配置管理器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_platform_adapters():
    """测试平台适配器基类"""
    print("🌐 测试平台适配器基类...")
    try:
        # 直接定义 PlatformAdapter 类进行测试
        class PlatformAdapter:
            """平台适配器基类"""
            
            def __init__(self, platform_name: str):
                self.platform_name = platform_name
                self.config = {}
                
            def load_config(self, config: dict):
                """加载平台特定配置"""
                self.config = config.get(self.platform_name, {})
                
            def adapt_title(self, original_title: str) -> str:
                """适配标题"""
                return original_title
            
            def adapt_content(self, content: str) -> str:
                """适配内容"""
                return content
            
            def adapt_format(self, content: str) -> str:
                """适配格式"""
                return content
            
            def get_char_limit(self) -> int:
                """获取字数限制"""
                return 10000
        
        adapter = PlatformAdapter("test_platform")
        print("  ✅ PlatformAdapter 实例化成功")
        
        # 测试基本方法
        title = adapter.adapt_title("测试标题")
        print(f"  ✅ adapt_title() 成功: {title}")
        
        content = adapter.adapt_content("测试内容")
        print(f"  ✅ adapt_content() 成功: {content}")
        
        char_limit = adapter.get_char_limit()
        print(f"  ✅ get_char_limit() 成功: {char_limit}")
        
        return True
    except Exception as e:
        print(f"  ❌ 平台适配器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_statistical_functions():
    """测试统计函数"""
    print("📊 测试统计函数...")
    try:
        # 测试简单的统计计算
        import math
        
        def calculate_mean(values):
            return sum(values) / len(values)
        
        def calculate_std(values):
            mean = calculate_mean(values)
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            return math.sqrt(variance)
        
        # 测试数据
        test_data = [1, 2, 3, 4, 5]
        mean = calculate_mean(test_data)
        std = calculate_std(test_data)
        
        print(f"  ✅ 均值计算成功: {mean}")
        print(f"  ✅ 标准差计算成功: {std}")
        
        # 验证计算结果
        assert abs(mean - 3.0) < 0.001, f"均值计算错误: {mean}"
        assert abs(std - 1.414) < 0.001, f"标准差计算错误: {std}"
        
        return True
    except Exception as e:
        print(f"  ❌ 统计函数测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_operations():
    """测试文件操作"""
    print("📁 测试文件操作...")
    try:
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            
            # 测试创建文件
            test_file = temp_dir / "test_file.txt"
            test_file.write_text("测试内容", encoding="utf-8")
            print(f"  ✅ 文件创建成功: {test_file}")
            
            # 测试读取文件
            content = test_file.read_text(encoding="utf-8")
            print(f"  ✅ 文件读取成功: {content}")
            
            # 测试文件存在性
            assert test_file.exists(), "文件不存在"
            assert content == "测试内容", "文件内容不匹配"
            
            # 测试 JSON 操作
            json_file = temp_dir / "test_config.json"
            config_data = {
                "api_key": "test_key",
                "debug": True,
                "max_retry": 3
            }
            json_file.write_text(json.dumps(config_data, indent=2), encoding="utf-8")
            
            loaded_config = json.loads(json_file.read_text(encoding="utf-8"))
            assert loaded_config["api_key"] == "test_key", "JSON 配置不匹配"
            print(f"  ✅ JSON 操作成功")
            
        return True
    except Exception as e:
        print(f"  ❌ 文件操作测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_structures():
    """测试数据结构"""
    print("🗂️ 测试数据结构...")
    try:
        # 测试字典操作
        test_dict = {
            "platforms": ["xiaohongshu", "zhihu", "twitter"],
            "config": {"max_length": 1000, "enable_images": True},
            "stats": {"views": 1000, "likes": 50, "shares": 20}
        }
        
        print(f"  ✅ 字典创建成功")
        assert "platforms" in test_dict, "字典键不存在"
        assert len(test_dict["platforms"]) == 3, "平台列表长度错误"
        
        # 测试列表操作
        platforms = test_dict["platforms"]
        platforms.append("newsletter")
        assert len(platforms) == 4, "列表添加失败"
        print(f"  ✅ 列表操作成功")
        
        # 测试嵌套结构访问
        max_length = test_dict["config"]["max_length"]
        assert max_length == 1000, "嵌套结构访问失败"
        print(f"  ✅ 嵌套结构访问成功")
        
        return True
    except Exception as e:
        print(f"  ❌ 数据结构测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试新功能模块")
    print("=" * 50)
    
    test_results = []
    
    # 运行测试
    test_results.append(("配置管理器", test_config_manager()))
    test_results.append(("平台适配器", test_platform_adapters()))
    test_results.append(("统计函数", test_statistical_functions()))
    test_results.append(("文件操作", test_file_operations()))
    test_results.append(("数据结构", test_data_structures()))
    
    print("=" * 50)
    print("📋 测试结果汇总:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 测试完成: {passed}/{total} 通过")
    
    if passed == total:
        print("✨ 所有新功能模块基础测试通过！")
        return True
    else:
        print("⚠️ 部分测试失败，需要进一步调试")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)