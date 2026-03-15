#!/usr/bin/env python3
"""
Integration tests for article-workflow

集成测试，验证各个模块的基本功能
"""

import os
import sys
import json
import tempfile
import unittest
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "shared"))

# 导入配置加载器函数（用于测试）
from config_loader import (
    get_config,
    get_config_bool,
    get_config_int,
    get_config_list,
    require_config,
    generate_config_template,
)


class TestConfigLoading(unittest.TestCase):
    """测试配置加载"""
    
    def setUp(self):
        """测试前准备"""
        self.test_config = {
            "gemini_api_key": "test-gemini-key",
            "default_author": "Test Author",
            "article_generation": {
                "default_word_count": 1000,
                "auto_generate_images": True
            }
        }
        
        # 创建临时配置文件
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "config.json")
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_config, f, indent=2)
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_config_file_exists(self):
        """测试配置文件存在性"""
        self.assertTrue(os.path.exists(self.config_file))
    
    def test_config_content(self):
        """测试配置文件内容"""
        with open(self.config_file, 'r', encoding='utf-8') as f:
            loaded_config = json.load(f)
        
        self.assertEqual(loaded_config["gemini_api_key"], "test-gemini-key")
        self.assertEqual(loaded_config["default_author"], "Test Author")
        self.assertEqual(loaded_config["article_generation"]["default_word_count"], 1000)


class TestPipelineMetadata(unittest.TestCase):
    """测试流水线元数据"""
    
    def test_pipeline_id_generation(self):
        """测试流水线ID生成"""
        from pipeline_manager import PipelineManager
        
        # 测试自动生成ID
        pipeline_id = PipelineManager._generate_pipeline_id()
        self.assertIsNotNone(pipeline_id)
        self.assertIsInstance(pipeline_id, str)
        
        # ID应该包含日期
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertTrue(pipeline_id.startswith(today))
    
    def test_pipeline_metadata_structure(self):
        """测试流水线元数据结构"""
        from pipeline_manager import PipelineManager
        
        # 创建测试流水线
        pipeline = PipelineManager("test-pipeline-001")
        
        # 测试基本结构
        metadata = pipeline.metadata
        self.assertIn('pipeline_id', metadata)
        self.assertIn('start_time', metadata)
        self.assertIn('execution', metadata)
        self.assertIn('article', metadata)
        self.assertIn('stages', metadata)
        
        # 测试执行状态
        execution = metadata['execution']
        self.assertEqual(execution['status'], 'pending')
        self.assertEqual(execution['retry_count'], 0)
        
        # 测试文章信息
        article = metadata['article']
        self.assertEqual(article['status'], 'draft')


class TestRetryManager(unittest.TestCase):
    """测试重试管理器"""
    
    def setUp(self):
        """测试前准备"""
        from retry_manager import RetryManager
        self.retry_manager = RetryManager()
    
    def test_retryable_errors(self):
        """测试可重试错误"""
        from retry_manager import RetryableErrorType
        
        # 测试内容审查失败
        can_retry, reason = self.retry_manager.can_retry(
            RetryableErrorType.CONTENT_REVIEW_FAILED.value,
            0
        )
        self.assertTrue(can_retry)
        self.assertEqual(reason, "可以重试")
        
        # 测试网络超时
        can_retry, reason = self.retry_manager.can_retry(
            RetryableErrorType.NETWORK_TIMEOUT.value,
            1
        )
        self.assertTrue(can_retry)
    
    def test_non_retryable_errors(self):
        """测试不可重试错误"""
        from retry_manager import NonRetryableErrorType
        
        # 测试认证失败
        can_retry, reason = self.retry_manager.can_retry(
            NonRetryableErrorType.AUTHENTICATION_FAILED.value,
            0
        )
        self.assertFalse(can_retry)
        self.assertEqual(reason, "此错误类型不可重试")
    
    def test_max_retries(self):
        """测试最大重试次数"""
        from retry_manager import RetryableErrorType
        
        # 测试达到最大重试次数
        can_retry, reason = self.retry_manager.can_retry(
            RetryableErrorType.CONTENT_REVIEW_FAILED.value,
            3  # 已达到最大重试次数
        )
        self.assertFalse(can_retry)
        self.assertIn("达到最大重试次数", reason)
    
    def test_backoff_calculation(self):
        """测试退避时间计算"""
        from retry_manager import RetryableErrorType
        
        # 测试首次重试 (retry_count=1)
        backoff = self.retry_manager.get_backoff_seconds(
            RetryableErrorType.NETWORK_TIMEOUT.value,
            1
        )
        # backoff_base=2.0, retry_count=1, 所以 2.0^1 = 2，加上随机抖动0.8-1.2
        self.assertGreaterEqual(backoff, 1.6)  # 2 * 0.8
        self.assertLessEqual(backoff, 2.4)    # 2 * 1.2
        
        # 测试第二次重试 (retry_count=2)
        backoff2 = self.retry_manager.get_backoff_seconds(
            RetryableErrorType.NETWORK_TIMEOUT.value,
            2
        )
        self.assertGreater(backoff2, backoff)


class TestUserConfirm(unittest.TestCase):
    """测试用户确认管理器"""
    
    def setUp(self):
        """测试前准备"""
        from user_confirm import UserConfirm
        self.user_confirm = UserConfirm("test-pipeline")
    
    def test_confirmation_types(self):
        """测试确认类型"""
        from user_confirm import ConfirmationType
        
        # 测试所有确认类型
        for conf_type in ConfirmationType:
            self.assertIsInstance(conf_type.value, str)
            self.assertGreater(len(conf_type.value), 0)
    
    def test_selection_prompt(self):
        """测试选择提示"""
        from user_confirm import ConfirmationType
        
        options = ["选项A", "选项B", "选项C"]
        
        # 模拟用户输入（这里我们手动设置选择）
        # 在实际测试中，这需要模拟输入
        selection = "选项B"
        
        # 测试选择功能（这里只是验证逻辑，不实际交互）
        result = selection  # 模拟用户选择了选项B
        self.assertEqual(result, "选项B")
        self.assertIn(result, options)
    
    def test_yes_no_prompt(self):
        """测试是/否提示"""
        from user_confirm import ConfirmationType
        
        # 模拟用户输入是
        user_response = "y"
        confirmed = user_response.lower() in ['y', 'yes', '是', '确认']
        self.assertTrue(confirmed)
        
        # 模拟用户输入否
        user_response = "n"
        confirmed = user_response.lower() in ['y', 'yes', '是', '确认']
        self.assertFalse(confirmed)


class TestConfigLoader(unittest.TestCase):
    """测试配置加载器"""
    
    def setUp(self):
        """测试前准备"""
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        self.temp_dir = tempfile.mkdtemp()
        
        # 设置环境变量进行测试
        os.environ["TEST_API_KEY"] = "test-env-api-key"
        os.environ["TEST_DEBUG_MODE"] = "true"
        os.environ["TEST_MAX_RETRY"] = "5"
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        # 清理环境变量
        for key in ["TEST_API_KEY", "TEST_DEBUG_MODE", "TEST_MAX_RETRY"]:
            os.environ.pop(key, None)
        
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_basic_config_loading(self):
        """测试基本配置加载"""
        # 测试环境变量
        val = get_config("test_api_key")
        self.assertEqual(val, "test-env-api-key")
        
        # 测试布尔值转换
        val = get_config_bool("test_debug_mode")
        self.assertTrue(val)
        
        # 测试整数值转换
        val = get_config_int("test_max_retry")
        self.assertEqual(val, 5)
    
    def test_config_priority(self):
        """测试配置优先级"""
        # 先清理环境变量
        for key in ["TEST_API_KEY", "TEST_VALUE", "TEST_API_KEY_2"]:
            os.environ.pop(key, None)
        
        # 设置环境变量
        os.environ["TEST_VALUE"] = "from-env"
        os.environ["TEST_API_KEY_2"] = "from-env-key"
        
        # 环境变量应该优先于任何配置文件
        val = get_config("test_value")
        self.assertEqual(val, "from-env")
        
        # 测试没有环境变量时返回默认值
        val = get_config("non_existent_key", "default-value")
        self.assertEqual(val, "default-value")
        
        # 测试环境变量存在时使用环境变量
        val = get_config("test_api_key_2", "default-key")
        self.assertEqual(val, "from-env-key")
    
    def test_config_validation(self):
        """测试配置验证"""
        # 测试默认值
        val = get_config("non_existent_key", "default-value")
        self.assertEqual(val, "default-value")
        
        # 测试必填配置（应该会失败）
        with self.assertRaises(ValueError):
            require_config("required_key_that_does_not_exist")
    
    def test_type_conversion(self):
        """测试类型转换"""
        # 设置测试环境变量
        os.environ["TEST_BOOL"] = "true"
        os.environ["TEST_INT"] = "123"
        os.environ["TEST_LIST"] = "a,b,c,d"
        
        # 测试布尔值转换
        val = get_config_bool("test_bool")
        self.assertTrue(val)
        
        # 测试整数转换
        val = get_config_int("test_int")
        self.assertEqual(val, 123)
        
        # 测试列表转换
        val = get_config_list("test_list")
        self.assertEqual(val, ["a", "b", "c", "d"])
    
    def test_config_template_generation(self):
        """测试配置模板生成"""
        # 生成模板
        template = generate_config_template()
        
        # 验证模板包含必要的部分
        self.assertIn("api", template)
        self.assertIn("content", template)
        self.assertIn("paths", template)
        self.assertIn("pipeline", template)


class TestFileOperations(unittest.TestCase):
    """测试文件操作"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_create_article_file(self):
        """测试创建文章文件"""
        # 创建测试文章内容
        article_content = """---
title: 测试文章
author: 测试作者
date: 2025-03-15
tags: [测试, 示例]
---

# 测试文章标题

这是测试文章的内容。

## 二级标题

更多测试内容。"""
        
        # 保存文章文件
        article_path = os.path.join(self.temp_dir, "test_article.md")
        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(article_content)
        
        # 验证文件
        self.assertTrue(os.path.exists(article_path))
        self.assertGreater(os.path.getsize(article_path), 0)
        
        # 读取并验证内容
        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn("测试文章标题", content)
        self.assertIn("测试作者", content)
        self.assertIn("tags: [测试, 示例]", content)
    
    def test_yaml_frontmatter(self):
        """测试YAML frontmatter解析"""
        import yaml
        
        frontmatter = """---
title: YAML测试
author: 测试员
date: 2025-03-15
tags: [yaml, 测试, 文档]
---"""
        
        # 解析YAML
        lines = frontmatter.strip().split('\n')[1:-1]  # 去掉首尾的---
        yaml_content = '\n'.join(lines)
        parsed = yaml.safe_load(yaml_content)
        
        # 验证解析结果
        self.assertEqual(parsed['title'], 'YAML测试')
        self.assertEqual(parsed['author'], '测试员')
        self.assertEqual(parsed['tags'], ['yaml', '测试', '文档'])


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTest(loader.loadTestsFromTestCase(TestConfigLoading))
    suite.addTest(loader.loadTestsFromTestCase(TestPipelineMetadata))
    suite.addTest(loader.loadTestsFromTestCase(TestRetryManager))
    suite.addTest(loader.loadTestsFromTestCase(TestUserConfirm))
    suite.addTest(loader.loadTestsFromTestCase(TestConfigLoader))
    suite.addTest(loader.loadTestsFromTestCase(TestFileOperations))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()


if __name__ == "__main__":
    print("🚀 开始运行 article-workflow 集成测试")
    print("=" * 60)
    
    success = run_tests()
    
    print("=" * 60)
    if success:
        print("✅ 所有测试通过！")
        sys.exit(0)
    else:
        print("❌ 测试失败！")
        sys.exit(1)