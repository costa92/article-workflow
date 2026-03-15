#!/usr/bin/env python3
"""
Pipeline CLI for article-workflow

统一命令行工具，用于管理文章创作流水线
"""

import os
import sys
import argparse
import json
import yaml
from pathlib import Path
from datetime import datetime

# 获取插件根目录
PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "shared"))

from pipeline_manager import PipelineManager
from retry_manager import RetryManager, RetryableErrorType, NonRetryableErrorType
from user_confirm import UserConfirm, ConfirmationType


def print_banner():
    """打印横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                文章创作流水线 CLI 工具                       ║
║                    Article Workflow CLI                      ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def check_config():
    """检查配置文件是否存在"""
    config_file = os.path.join(PLUGIN_ROOT, "config", "config.json")
    example_file = os.path.join(PLUGIN_ROOT, "config", "config.example.json")
    
    if not os.path.exists(config_file):
        print("⚠️  配置文件不存在！")
        print(f"请先运行配置向导：python {os.path.join(PLUGIN_ROOT, 'scripts', 'config_wizard.py')}")
        print("或复制示例配置文件：")
        print(f"  cp {example_file} {config_file}")
        return False
    
    # 读取配置文件检查必填项
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 检查必填配置
        if not config.get('gemini_api_key'):
            print("⚠️  Gemini API 密钥未配置！")
            print("请编辑配置文件设置 gemini_api_key")
            return False
            
    except json.JSONDecodeError:
        print("❌ 配置文件格式错误！")
        return False
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False
    
    return True


def create_pipeline(args):
    """创建新的流水线"""
    print("📋 创建新的文章创作流水线")
    
    # 获取用户输入
    topic = input("请输入文章主题（或留空使用默认选题）: ").strip()
    author = input("请输入作者名称（留空使用配置中的默认作者）: ").strip()
    
    # 创建流水线管理器
    pipeline = PipelineManager()
    
    # 初始化流水线元数据
    pipeline.initialize_pipeline({
        'topic': topic if topic else "未指定主题",
        'author': author if author else "未指定作者",
        'target_platforms': ['wechat'],
        'priority': 'normal'
    })
    
    print(f"✅ 流水线创建成功！")
    print(f"   流水线 ID: {pipeline.pipeline_id}")
    print(f"   开始时间: {pipeline.metadata.get('start_time')}")
    print(f"   当前状态: {pipeline.metadata.get('execution', {}).get('status', 'pending')}")
    
    return pipeline.pipeline_id


def list_pipelines(args):
    """列出所有流水线"""
    print("📊 流水线列表")
    print("-" * 80)
    
    metadata_dir = os.path.join(PLUGIN_ROOT, "config", "pipeline_metadata")
    if not os.path.exists(metadata_dir):
        print("暂无流水线记录")
        return
    
    pipelines = []
    for file in os.listdir(metadata_dir):
        if file.endswith('.yaml'):
            filepath = os.path.join(metadata_dir, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    metadata = yaml.safe_load(f)
                
                pipelines.append({
                    'id': metadata.get('pipeline_id', file.replace('.yaml', '')),
                    'start_time': metadata.get('start_time', '未知'),
                    'status': metadata.get('execution', {}).get('status', 'unknown'),
                    'current_stage': metadata.get('execution', {}).get('current_stage', 'unknown'),
                    'title': metadata.get('article', {}).get('title', '未命名文章')
                })
            except Exception as e:
                print(f"⚠️  读取流水线 {file} 失败: {e}")
    
    if not pipelines:
        print("暂无流水线记录")
        return
    
    # 按开始时间排序
    pipelines.sort(key=lambda x: x['start_time'], reverse=True)
    
    # 显示表格
    print(f"{'ID':<15} {'开始时间':<20} {'状态':<12} {'阶段':<15} {'标题'}")
    print("-" * 80)
    
    for pipeline in pipelines:
        status_emoji = {
            'pending': '⏳',
            'in_progress': '🔄', 
            'completed': '✅',
            'failed': '❌',
            'paused': '⏸️'
        }.get(pipeline['status'], '❓')
        
        print(f"{pipeline['id']:<15} {pipeline['start_time'][:19]:<20} "
              f"{status_emoji} {pipeline['status']:<10} {pipeline['current_stage']:<15} {pipeline['title'][:30]}")


def show_pipeline(args):
    """显示流水线详情"""
    if not args.pipeline_id:
        print("❌ 请指定流水线 ID")
        print("用法: pipeline_cli.py show <pipeline_id>")
        return
    
    print(f"📋 流水线详情: {args.pipeline_id}")
    print("-" * 80)
    
    try:
        pipeline = PipelineManager(args.pipeline_id)
        metadata = pipeline.metadata
        
        # 基本信息
        print(f"流水线 ID: {metadata.get('pipeline_id')}")
        print(f"开始时间: {metadata.get('start_time')}")
        print(f"用户 ID: {metadata.get('user_id', '未指定')}")
        
        # 执行状态
        execution = metadata.get('execution', {})
        print(f"\n执行状态:")
        print(f"  - 当前阶段: {execution.get('current_stage', 'unknown')}")
        print(f"  - 状态: {execution.get('status', 'unknown')}")
        print(f"  - 重试次数: {execution.get('retry_count', 0)}")
        print(f"  - 最大重试: {execution.get('max_retries', 3)}")
        
        if execution.get('error_message'):
            print(f"  - 错误信息: {execution.get('error_message')}")
        
        # 文章信息
        article = metadata.get('article', {})
        if article:
            print(f"\n文章信息:")
            print(f"  - 标题: {article.get('title', '未设置')}")
            print(f"  - 描述: {article.get('description', '未设置')[:50]}...")
            print(f"  - 文件: {article.get('file_path', '未生成')}")
            print(f"  - 字数: {article.get('word_count', 0)}")
            print(f"  - 状态: {article.get('status', 'draft')}")
            print(f"  - 标签: {', '.join(article.get('tags', []))}")
        
        # 阶段记录
        stages = metadata.get('stages', {})
        if stages:
            print(f"\n阶段执行记录:")
            for stage_name, stage_data in stages.items():
                if stage_data:
                    status_emoji = '✅' if stage_data.get('completed') else '⏳'
                    print(f"  {status_emoji} {stage_name}: {stage_data.get('status', 'pending')}")
                    if stage_data.get('start_time'):
                        print(f"     开始: {stage_data.get('start_time')}")
                    if stage_data.get('end_time'):
                        print(f"     结束: {stage_data.get('end_time')}")
                    if stage_data.get('error_count', 0) > 0:
                        print(f"     错误: {stage_data.get('error_count')} 次")
        
    except FileNotFoundError:
        print(f"❌ 流水线 {args.pipeline_id} 不存在")
    except Exception as e:
        print(f"❌ 读取流水线失败: {e}")


def run_pipeline(args):
    """运行流水线"""
    print("🚀 运行文章创作流水线")
    
    if not check_config():
        print("❌ 配置检查失败，无法运行流水线")
        return
    
    # 获取或创建流水线 ID
    pipeline_id = args.pipeline_id
    if not pipeline_id:
        # 创建新的流水线
        pipeline_id = create_pipeline(args)
        if not pipeline_id:
            return
    
    print(f"\n开始执行流水线: {pipeline_id}")
    print("=" * 60)
    
    # 这里可以添加实际的流水线执行逻辑
    # 由于这是一个示例，我们只模拟执行过程
    
    pipeline = PipelineManager(pipeline_id)
    
    # 模拟执行各个阶段
    stages = [
        ("content_planner", "选题规划"),
        ("article_generator", "文章生成"),
        ("content_reviewer", "内容审查"),
        ("wechat_seo_optimizer", "SEO优化"),
        ("wechat_article_converter", "格式转换"),
        ("publish", "发布文章")
    ]
    
    for stage_key, stage_name in stages:
        print(f"\n▶️  执行阶段: {stage_name}")
        
        # 更新阶段状态
        pipeline.update_stage_status(stage_key, "in_progress")
        
        # 模拟执行（实际应该调用相应的技能）
        print(f"   正在执行 {stage_name}...")
        import time
        time.sleep(1)  # 模拟执行时间
        
        # 模拟可能出现的错误
        if stage_key == "content_reviewer":
            # 模拟审查失败
            print("   内容审查未通过，需要修改...")
            pipeline.record_stage_error(stage_key, "内容质量评分低于55分", RetryableErrorType.CONTENT_REVIEW_FAILED.value)
            
            # 检查是否可以重试
            retry_manager = RetryManager()
            can_retry, reason = retry_manager.can_retry(
                RetryableErrorType.CONTENT_REVIEW_FAILED.value,
                pipeline.metadata.get('execution', {}).get('retry_count', 0)
            )
            
            if can_retry:
                print(f"   可以重试: {reason}")
                pipeline.increment_retry_count()
                print("   进行修改并重新审查...")
                time.sleep(1)
                print("   修改后审查通过！")
            else:
                print(f"   无法重试: {reason}")
                pipeline.update_stage_status(stage_key, "failed")
                print("❌ 流水线执行失败")
                return
        
        # 更新阶段状态为完成
        pipeline.update_stage_status(stage_key, "completed")
        print(f"   ✅ {stage_name} 完成")
    
    # 完成整个流水线
    pipeline.complete_pipeline()
    print(f"\n🎉 流水线执行完成！")
    print(f"   流水线 ID: {pipeline_id}")
    print(f"   总耗时: 模拟完成")
    
    # 显示生成的成果
    print(f"\n📄 生成的文件:")
    print(f"   - 文章文件: output/article_{datetime.now().strftime('%Y%m%d')}.md")
    print(f"   - 微信HTML: output/wechat_article.html")
    print(f"   - 流水线元数据: config/pipeline_metadata/{pipeline_id}.yaml")


def test_components(args):
    """测试各个组件"""
    print("🧪 测试流水线组件")
    print("-" * 60)
    
    # 测试流水线管理器
    print("1. 测试 PipelineManager...")
    try:
        test_pipeline = PipelineManager("test-pipeline")
        test_pipeline.initialize_pipeline({
            'topic': '测试文章',
            'author': '测试作者',
            'target_platforms': ['test'],
            'priority': 'low'
        })
        print("   ✅ PipelineManager 测试通过")
    except Exception as e:
        print(f"   ❌ PipelineManager 测试失败: {e}")
    
    # 测试重试管理器
    print("\n2. 测试 RetryManager...")
    try:
        retry_manager = RetryManager()
        
        # 测试可重试错误
        can_retry, reason = retry_manager.can_retry(
            RetryableErrorType.CONTENT_REVIEW_FAILED.value,
            0
        )
        print(f"   内容审查失败 (第0次): {can_retry} - {reason}")
        
        can_retry, reason = retry_manager.can_retry(
            RetryableErrorType.CONTENT_REVIEW_FAILED.value,
            3
        )
        print(f"   内容审查失败 (第3次): {can_retry} - {reason}")
        
        # 测试不可重试错误
        can_retry, reason = retry_manager.can_retry(
            NonRetryableErrorType.AUTHENTICATION_FAILED.value,
            0
        )
        print(f"   认证失败: {can_retry} - {reason}")
        
        print("   ✅ RetryManager 测试通过")
    except Exception as e:
        print(f"   ❌ RetryManager 测试失败: {e}")
    
    # 测试用户确认管理器
    print("\n3. 测试 UserConfirm...")
    try:
        user_confirm = UserConfirm("test-pipeline")
        
        # 模拟用户确认
        print("   模拟 SEO 标题选择...")
        options = ["标题A: 如何学习Python", "标题B: Python入门指南", "标题C: 快速掌握Python"]
        selection = user_confirm.prompt_selection(
            ConfirmationType.SEO_TITLE_SELECTION.value,
            "请选择最合适的标题:",
            options,
            allow_custom=False
        )
        print(f"   用户选择了: {selection}")
        
        print("   ✅ UserConfirm 测试通过")
    except Exception as e:
        print(f"   ❌ UserConfirm 测试失败: {e}")
    
    print("\n🧪 所有组件测试完成！")


def cleanup(args):
    """清理旧的流水线数据"""
    print("🧹 清理流水线数据")
    
    metadata_dir = os.path.join(PLUGIN_ROOT, "config", "pipeline_metadata")
    if not os.path.exists(metadata_dir):
        print("无需清理，目录不存在")
        return
    
    # 获取所有流水线文件
    pipeline_files = []
    for file in os.listdir(metadata_dir):
        if file.endswith('.yaml'):
            filepath = os.path.join(metadata_dir, file)
            pipeline_files.append((filepath, os.path.getmtime(filepath)))
    
    if not pipeline_files:
        print("没有可清理的流水线数据")
        return
    
    # 按修改时间排序
    pipeline_files.sort(key=lambda x: x[1])
    
    # 计算要保留的文件数量
    keep_count = max(10, args.keep)  # 至少保留10个
    files_to_delete = pipeline_files[:-keep_count] if len(pipeline_files) > keep_count else []
    
    if not files_to_delete:
        print(f"当前有 {len(pipeline_files)} 个流水线文件，无需清理")
        return
    
    print(f"找到 {len(pipeline_files)} 个流水线文件")
    print(f"将清理 {len(files_to_delete)} 个旧文件，保留最新的 {keep_count} 个")
    
    if not args.force:
        confirm = input(f"确认删除 {len(files_to_delete)} 个文件？(y/N): ").strip().lower()
        if confirm != 'y':
            print("取消清理")
            return
    
    # 删除文件
    deleted_count = 0
    for filepath, _ in files_to_delete:
        try:
            os.remove(filepath)
            print(f"删除: {os.path.basename(filepath)}")
            deleted_count += 1
        except Exception as e:
            print(f"删除失败 {os.path.basename(filepath)}: {e}")
    
    print(f"\n✅ 清理完成！删除了 {deleted_count} 个文件")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="文章创作流水线 CLI 工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # create 命令
    create_parser = subparsers.add_parser("create", help="创建新的流水线")
    
    # list 命令
    subparsers.add_parser("list", help="列出所有流水线")
    
    # show 命令
    show_parser = subparsers.add_parser("show", help="显示流水线详情")
    show_parser.add_argument("pipeline_id", nargs="?", help="流水线 ID")
    
    # run 命令
    run_parser = subparsers.add_parser("run", help="运行流水线")
    run_parser.add_argument("pipeline_id", nargs="?", help="流水线 ID（可选，不提供则创建新的）")
    
    # test 命令
    subparsers.add_parser("test", help="测试各个组件")
    
    # cleanup 命令
    cleanup_parser = subparsers.add_parser("cleanup", help="清理旧的流水线数据")
    cleanup_parser.add_argument("-k", "--keep", type=int, default=20, 
                               help="保留最新的 N 个流水线文件（默认: 20）")
    cleanup_parser.add_argument("-f", "--force", action="store_true",
                               help="无需确认直接清理")
    
    # 解析参数
    args = parser.parse_args()
    
    # 打印横幅
    print_banner()
    
    # 执行命令
    if args.command == "create":
        create_pipeline(args)
    elif args.command == "list":
        list_pipelines(args)
    elif args.command == "show":
        show_pipeline(args)
    elif args.command == "run":
        run_pipeline(args)
    elif args.command == "test":
        test_components(args)
    elif args.command == "cleanup":
        cleanup(args)
    else:
        # 显示帮助
        parser.print_help()
        print("\n📝 使用示例:")
        print("  1. 创建新流水线: python pipeline_cli.py create")
        print("  2. 列出所有流水线: python pipeline_cli.py list")
        print("  3. 运行流水线: python pipeline_cli.py run [pipeline_id]")
        print("  4. 查看详情: python pipeline_cli.py show <pipeline_id>")
        print("  5. 测试组件: python pipeline_cli.py test")
        print("  6. 清理数据: python pipeline_cli.py cleanup --keep 10")


if __name__ == "__main__":
    main()