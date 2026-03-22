#!/usr/bin/env python3
"""
content-repurposer 多平台分发器

功能：将同一篇文章适配到不同内容平台的格式要求
支持平台：小红书、知乎、Twitter、Newsletter、短视频脚本、Medium
"""

import os
import sys
import json
import yaml
import re
from typing import Dict, List, Optional, Any
from pathlib import Path

# 添加共享模块路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))

from shared import ConfigLoader, PipelineManager


class PlatformAdapter:
    """平台适配器基类"""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.config = {}
        
    def load_config(self, config: Dict[str, Any]):
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
    
    def get_image_count(self) -> int:
        """获取建议图片数量"""
        return 3
    
    def get_output_format(self) -> str:
        """获取输出格式"""
        return "md"
    
    def validate_content(self, content: str) -> bool:
        """验证内容是否符合平台要求"""
        return True


class XiaohongshuAdapter(PlatformAdapter):
    """小红书适配器"""
    
    def __init__(self):
        super().__init__("xiaohongshu")
        
    def adapt_title(self, original_title: str) -> str:
        """小红书标题：短小精悍，适合图片标题"""
        # 移除技术术语，增加生活化表述
        title = original_title
        title = re.sub(r'[^\u4e00-\u9fa5A-Za-z0-9\s]', '', title)
        title = title.strip()
        
        if len(title) > 20:
            title = title[:18] + "..."
        
        # 添加小红书常用标签
        hashtags = " #技术分享 #程序员日常 #学习笔记"
        return f"{title}{hashtags}"
    
    def adapt_content(self, content: str) -> str:
        """小红书内容：图片为主，文字简短，分点说明"""
        lines = content.split('\n')
        adapted_lines = []
        
        for line in lines:
            # 移除长段落，简化表述
            if len(line) > 100:
                continue
            
            # 将技术内容转化为通俗表述
            if "docker" in line.lower():
                line = line.replace("Docker", "容器技术")
            if "python" in line.lower():
                line = line.replace("Python", "编程语言")
            
            adapted_lines.append(line)
        
        # 添加小红书特色格式
        adapted_content = "\n".join(adapted_lines)
        adapted_content += "\n\n---\n"
        adapted_content += "💡 小贴士：点击主页查看更多技术分享"
        
        return adapted_content
    
    def get_char_limit(self) -> int:
        return 1000
    
    def get_image_count(self) -> int:
        return 9  # 小红书支持9张图片
    
    def get_output_format(self) -> str:
        return "txt"


class ZhihuAdapter(PlatformAdapter):
    """知乎适配器"""
    
    def __init__(self):
        super().__init__("zhihu")
        
    def adapt_title(self, original_title: str) -> str:
        """知乎标题：问题式、悬念式"""
        title = original_title
        
        # 转换为知乎风格的问题式标题
        question_starters = [
            "如何评价", "如何理解", "怎样学习", "有哪些技巧",
            "为什么", "是什么体验", "有什么建议"
        ]
        
        import random
        starter = random.choice(question_starters)
        return f"{starter}{title}？"
    
    def adapt_content(self, content: str) -> str:
        """知乎内容：专业、深入、结构化"""
        lines = content.split('\n')
        adapted_lines = []
        
        # 添加知乎特色的开头
        adapted_lines.append("## 前言")
        adapted_lines.append("作为一名长期关注技术发展的从业者，我想分享一下我的理解和经验。")
        adapted_lines.append("")
        
        for line in lines:
            if line.startswith('# '):
                # 主标题
                adapted_lines.append(f"## {line[2:]}")
            elif line.startswith('## '):
                # 子标题
                adapted_lines.append(f"### {line[3:]}")
            elif line.startswith('### '):
                # 小标题
                adapted_lines.append(f"#### {line[4:]}")
            else:
                adapted_lines.append(line)
        
        # 添加知乎特色的结尾
        adapted_lines.append("")
        adapted_lines.append("## 总结")
        adapted_lines.append("以上就是我对这个问题的理解，希望对大家有所帮助。如果有什么问题，欢迎在评论区讨论。")
        
        return "\n".join(adapted_lines)
    
    def get_char_limit(self) -> int:
        return 20000
    
    def get_image_count(self) -> int:
        return 5


class TwitterAdapter(PlatformAdapter):
    """Twitter适配器"""
    
    def __init__(self):
        super().__init__("twitter")
        
    def adapt_title(self, original_title: str) -> str:
        """Twitter标题：简洁、醒目、带话题"""
        title = original_title
        
        # 提取关键词作为话题标签
        keywords = ["技术", "编程", "AI", "开发", "工具"]
        matched_keywords = []
        
        for keyword in keywords:
            if keyword.lower() in title.lower():
                matched_keywords.append(keyword)
        
        if matched_keywords:
            hashtags = " " + " ".join([f"#{kw}" for kw in matched_keywords])
        else:
            hashtags = " #技术分享 #编程"
        
        # 截断到适合长度
        max_length = 280 - len(hashtags) - 5  # 留出空间
        if len(title) > max_length:
            title = title[:max_length-3] + "..."
        
        return f"{title}{hashtags}"
    
    def adapt_content(self, content: str) -> str:
        """Twitter内容：简短、分线程、吸引人"""
        lines = content.split('\n')
        twitter_thread = []
        current_tweet = ""
        tweet_count = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 每个新段落可能开始新推文
            if len(current_tweet) + len(line) + 1 > 270:
                twitter_thread.append(current_tweet.strip())
                tweet_count += 1
                current_tweet = ""
            
            if current_tweet:
                current_tweet += " "
            current_tweet += line
        
        if current_tweet:
            twitter_thread.append(current_tweet.strip())
        
        # 如果只有一条推文，直接返回
        if len(twitter_thread) == 1:
            return twitter_thread[0]
        
        # 多线程格式
        thread_content = ""
        for i, tweet in enumerate(twitter_thread):
            thread_content += f"({i+1}/{len(twitter_thread)}) {tweet}\n\n"
        
        return thread_content.strip()
    
    def get_char_limit(self) -> int:
        return 280  # 单推文限制
    
    def get_output_format(self) -> str:
        return "txt"


class NewsletterAdapter(PlatformAdapter):
    """Newsletter适配器"""
    
    def __init__(self):
        super().__init__("newsletter")
        
    def adapt_title(self, original_title: str) -> str:
        """Newsletter标题：正式、吸引订阅者"""
        return f"【技术周刊】{original_title}"
    
    def adapt_content(self, content: str) -> str:
        """Newsletter内容：结构化、有引言有总结"""
        lines = content.split('\n')
        adapted_lines = []
        
        # 添加Newsletter特色的开头
        adapted_lines.append("# 📬 技术周刊")
        adapted_lines.append("")
        adapted_lines.append("亲爱的订阅者，")
        adapted_lines.append("")
        adapted_lines.append("本周我们为大家带来一篇精彩的技术分享：")
        adapted_lines.append("")
        
        # 主要内容
        for line in lines:
            if line.startswith('# ') and not line.startswith('# 📬'):
                # 添加章节编号
                adapted_lines.append(line)
            else:
                adapted_lines.append(line)
        
        # 添加Newsletter特色的结尾
        adapted_lines.append("")
        adapted_lines.append("---")
        adapted_lines.append("")
        adapted_lines.append("## 🔗 相关阅读")
        adapted_lines.append("- [往期内容归档](https://example.com/archive)")
        adapted_lines.append("- [技术讨论社区](https://example.com/community)")
        adapted_lines.append("")
        adapted_lines.append("感谢您的订阅！")
        adapted_lines.append("如有任何问题或建议，欢迎回复此邮件。")
        
        return "\n".join(adapted_lines)
    
    def get_char_limit(self) -> int:
        return 5000
    
    def get_image_count(self) -> int:
        return 3


class MultiPlatformRepurposer:
    """多平台分发器主类"""
    
    def __init__(self, config_loader: ConfigLoader):
        self.config_loader = config_loader
        self.platforms = {
            "xiaohongshu": XiaohongshuAdapter(),
            "zhihu": ZhihuAdapter(),
            "twitter": TwitterAdapter(),
            "newsletter": NewsletterAdapter(),
        }
        self.output_dir = Path("output/repurposed")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_config(self):
        """加载配置"""
        config = self.config_loader.load_config()
        platform_config = config.get("platform_repurposing", {})
        
        # 为每个平台适配器加载配置
        for platform_name, adapter in self.platforms.items():
            adapter.load_config(platform_config)
            
        # 获取启用的平台
        self.enabled_platforms = platform_config.get("enabled_platforms", list(self.platforms.keys()))
        
        # 获取输出目录
        custom_output_dir = platform_config.get("output_dir")
        if custom_output_dir:
            self.output_dir = Path(custom_output_dir)
            self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def repurpose_article(self, article_path: str, target_platforms: Optional[List[str]] = None) -> Dict[str, str]:
        """
        将文章适配到多个平台
        
        Args:
            article_path: 原始文章路径
            target_platforms: 目标平台列表，如为None则使用所有启用的平台
            
        Returns:
            字典：平台名 -> 适配后的内容路径
        """
        # 读取原始文章
        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 确定目标平台
        if target_platforms is None:
            target_platforms = self.enabled_platforms
        else:
            # 过滤掉未启用的平台
            target_platforms = [p for p in target_platforms if p in self.enabled_platforms]
        
        results = {}
        
        # 为每个平台适配内容
        for platform_name in target_platforms:
            if platform_name not in self.platforms:
                print(f"⚠️  平台 {platform_name} 不支持，跳过")
                continue
                
            adapter = self.platforms[platform_name]
            
            try:
                # 适配内容
                adapted_title = adapter.adapt_title(self.extract_title(content))
                adapted_content = adapter.adapt_content(content)
                adapted_content = adapter.adapt_format(adapted_content)
                
                # 生成输出文件名
                article_stem = Path(article_path).stem
                output_filename = f"{article_stem}_{platform_name}.{adapter.get_output_format()}"
                output_path = self.output_dir / output_filename
                
                # 写入文件
                with open(output_path, 'w', encoding='utf-8') as f:
                    if adapter.get_output_format() == "txt":
                        f.write(f"{adapted_title}\n\n")
                        f.write(adapted_content)
                    elif adapter.get_output_format() == "md":
                        f.write(f"# {adapted_title}\n\n")
                        f.write(adapted_content)
                    else:
                        f.write(adapted_content)
                
                results[platform_name] = str(output_path)
                print(f"✅  {platform_name}: 已生成 {output_path}")
                
            except Exception as e:
                print(f"❌  {platform_name} 处理失败: {e}")
                continue
        
        return results
    
    def extract_title(self, content: str) -> str:
        """从文章内容中提取标题"""
        # 尝试从Markdown标题提取
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        
        # 如果没有标题，使用前20个字符
        if len(content) > 20:
            return content[:20] + "..."
        return content.strip()
    
    def list_platforms(self) -> List[str]:
        """列出所有支持的平台"""
        return list(self.platforms.keys())
    
    def get_platform_info(self, platform_name: str) -> Dict[str, Any]:
        """获取平台详细信息"""
        if platform_name not in self.platforms:
            return {"error": f"平台 {platform_name} 不支持"}
        
        adapter = self.platforms[platform_name]
        return {
            "name": platform_name,
            "char_limit": adapter.get_char_limit(),
            "image_count": adapter.get_image_count(),
            "output_format": adapter.get_output_format(),
            "description": self.get_platform_description(platform_name)
        }
    
    def get_platform_description(self, platform_name: str) -> str:
        """获取平台描述"""
        descriptions = {
            "xiaohongshu": "小红书 - 图片为主的生活分享平台，适合技术生活化内容",
            "zhihu": "知乎 - 问答社区，适合深度技术讨论和教程",
            "twitter": "Twitter - 社交网络，适合技术动态和短内容",
            "newsletter": "Newsletter - 邮件订阅，适合定期技术总结和深度内容"
        }
        return descriptions.get(platform_name, "未知平台")


def main():
    """主函数"""
    print("🎯 content-repurposer - 多平台内容分发器")
    print("=" * 50)
    
    # 加载配置
    config_loader = ConfigLoader()
    
    try:
        config_loader.load_config()
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        print("请先运行配置向导: python scripts/config_wizard.py")
        sys.exit(1)
    
    # 创建分发器
    repurposer = MultiPlatformRepurposer(config_loader)
    repurposer.load_config()
    
    # 解析命令行参数
    import argparse
    parser = argparse.ArgumentParser(description="多平台内容分发器")
    parser.add_argument("article_path", help="原始文章路径")
    parser.add_argument("--platforms", nargs="+", help="目标平台列表")
    parser.add_argument("--list", action="store_true", help="列出所有支持的平台")
    parser.add_argument("--info", help="获取平台详细信息")
    
    args = parser.parse_args()
    
    if args.list:
        # 列出平台
        platforms = repurposer.list_platforms()
        print(f"📋 支持的平台 ({len(platforms)} 个):")
        for platform in platforms:
            info = repurposer.get_platform_info(platform)
            print(f"  • {platform}: {info['char_limit']}字符限制，{info['image_count']}张图片建议")
        return
    
    if args.info:
        # 显示平台信息
        info = repurposer.get_platform_info(args.info)
        if "error" in info:
            print(f"❌ {info['error']}")
        else:
            print(f"📊 平台信息: {args.info}")
            print(f"  描述: {info['description']}")
            print(f"  字数限制: {info['char_limit']} 字符")
            print(f"  图片建议: {info['image_count']} 张")
            print(f"  输出格式: {info['output_format']}")
        return
    
    # 执行分发
    print(f"📄 处理文章: {args.article_path}")
    print(f"🎯 目标平台: {args.platforms or '所有启用的平台'}")
    print("-" * 50)
    
    results = repurposer.repurpose_article(
        args.article_path,
        args.platforms
    )
    
    print("-" * 50)
    print(f"✅ 完成! 生成了 {len(results)} 个平台适配版本")
    print(f"📁 输出目录: {repurposer.output_dir}")
    
    # 保存结果记录
    if results:
        result_file = repurposer.output_dir / "repurpose_results.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump({
                "article": args.article_path,
                "platforms": list(results.keys()),
                "output_files": results
            }, f, ensure_ascii=False, indent=2)
        print(f"📝 结果记录: {result_file}")


if __name__ == "__main__":
    main()