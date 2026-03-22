#!/usr/bin/env python3
"""
content-analytics 数据分析器

功能：分析微信公众号等平台的内容表现数据
支持数据源：微信后台导出数据、流水线元数据、手动上传数据
输出：多维度分析报告和优化建议
"""

import os
import sys
import json
import csv
import yaml
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import matplotlib
matplotlib.use('Agg')  # 非交互式后端
import matplotlib.pyplot as plt

# 添加共享模块路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))

from shared import ConfigLoader, PipelineManager


class DataSource:
    """数据源基类"""
    
    def __init__(self, source_type: str):
        self.source_type = source_type
        self.data = None
        
    def load(self, source_path: str) -> bool:
        """加载数据"""
        raise NotImplementedError
        
    def get_articles(self) -> List[Dict[str, Any]]:
        """获取文章列表"""
        return []
        
    def get_metrics(self, article_id: str) -> Dict[str, Any]:
        """获取文章指标"""
        return {}


class WeChatDataSource(DataSource):
    """微信后台数据源"""
    
    def __init__(self):
        super().__init__("wechat")
        self.articles = []
        
    def load(self, source_path: str) -> bool:
        """加载微信后台导出的CSV/Excel数据"""
        try:
            if source_path.endswith('.csv'):
                df = pd.read_csv(source_path, encoding='utf-8')
            elif source_path.endswith('.xlsx') or source_path.endswith('.xls'):
                df = pd.read_excel(source_path)
            else:
                print(f"❌ 不支持的文件格式: {source_path}")
                return False
            
            # 解析微信数据格式
            self.articles = self.parse_wechat_data(df)
            self.data = df
            print(f"✅ 加载微信数据: {len(self.articles)} 篇文章")
            return True
            
        except Exception as e:
            print(f"❌ 微信数据加载失败: {e}")
            return False
    
    def parse_wechat_data(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """解析微信后台数据格式"""
        articles = []
        
        # 微信数据列名映射
        column_mapping = {
            '文章标题': 'title',
            '发布时间': 'publish_time',
            '阅读数': 'read_count',
            '在看数': 'view_count',
            '点赞数': 'like_count',
            '分享数': 'share_count',
            '收藏数': 'favorite_count',
            '评论数': 'comment_count'
        }
        
        for _, row in df.iterrows():
            article = {}
            
            for wechat_col, internal_col in column_mapping.items():
                if wechat_col in row:
                    article[internal_col] = row[wechat_col]
            
            # 计算衍生指标
            if 'read_count' in article and article['read_count'] > 0:
                article['like_rate'] = article.get('like_count', 0) / article['read_count'] * 100
                article['share_rate'] = article.get('share_count', 0) / article['read_count'] * 100
                article['comment_rate'] = article.get('comment_count', 0) / article['read_count'] * 100
            
            # 解析发布时间
            if 'publish_time' in article:
                try:
                    publish_time = pd.to_datetime(article['publish_time'])
                    article['publish_date'] = publish_time.date()
                    article['publish_weekday'] = publish_time.strftime('%A')
                    article['publish_hour'] = publish_time.hour
                except:
                    pass
            
            articles.append(article)
        
        return articles
    
    def get_articles(self) -> List[Dict[str, Any]]:
        return self.articles
    
    def get_metrics(self, article_id: str) -> Dict[str, Any]:
        """获取指定文章指标（这里article_id是标题）"""
        for article in self.articles:
            if article.get('title') == article_id:
                return article
        return {}


class PipelineDataSource(DataSource):
    """流水线元数据源"""
    
    def __init__(self, pipeline_manager: PipelineManager):
        super().__init__("pipeline")
        self.pipeline_manager = pipeline_manager
        self.articles = []
        
    def load(self, source_path: str = None) -> bool:
        """从流水线元数据加载文章信息"""
        try:
            # 获取所有流水线数据
            pipelines = self.pipeline_manager.get_pipeline_stats()
            
            articles = []
            for pipeline in pipelines.get('pipelines', []):
                if pipeline.get('status') != 'completed':
                    continue
                    
                # 从流水线元数据提取文章信息
                article = self.extract_article_from_pipeline(pipeline)
                if article:
                    articles.append(article)
            
            self.articles = articles
            print(f"✅ 加载流水线数据: {len(self.articles)} 篇文章")
            return True
            
        except Exception as e:
            print(f"❌ 流水线数据加载失败: {e}")
            return False
    
    def extract_article_from_pipeline(self, pipeline: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """从流水线数据提取文章信息"""
        try:
            article = {}
            
            # 从流水线ID或元数据获取文章标题
            if 'metadata' in pipeline and 'topic' in pipeline['metadata']:
                article['title'] = pipeline['metadata']['topic']
            else:
                article['title'] = f"流水线 {pipeline.get('id', 'unknown')}"
            
            # 获取发布时间
            if 'created_at' in pipeline:
                try:
                    publish_time = pd.to_datetime(pipeline['created_at'])
                    article['publish_time'] = publish_time
                    article['publish_date'] = publish_time.date()
                except:
                    article['publish_time'] = datetime.now()
            
            # 从流水线阶段获取指标
            if 'stages' in pipeline:
                stages = pipeline['stages']
                
                # 审查评分
                for stage in stages:
                    if stage.get('name') == 'content_reviewer' and 'metrics' in stage:
                        if 'score' in stage['metrics']:
                            article['review_score'] = stage['metrics']['score']
                    
                    # 文章统计
                    if stage.get('name') == 'article_generator' and 'metrics' in stage:
                        if 'word_count' in stage['metrics']:
                            article['word_count'] = stage['metrics']['word_count']
                        if 'images_generated' in stage['metrics']:
                            article['images_generated'] = stage['metrics']['images_generated']
            
            # 设置默认值
            article['read_count'] = article.get('read_count', 0)
            article['like_count'] = article.get('like_count', 0)
            article['share_count'] = article.get('share_count', 0)
            
            return article
            
        except Exception as e:
            print(f"⚠️  提取流水线文章信息失败: {e}")
            return None
    
    def get_articles(self) -> List[Dict[str, Any]]:
        return self.articles
    
    def get_metrics(self, article_id: str) -> Dict[str, Any]:
        for article in self.articles:
            if article.get('title') == article_id:
                return article
        return {}


class ContentAnalyzer:
    """内容分析器"""
    
    def __init__(self, data_source: DataSource):
        self.data_source = data_source
        self.articles = data_source.get_articles()
        
    def analyze_performance(self) -> Dict[str, Any]:
        """分析内容表现"""
        if not self.articles:
            return {"error": "没有数据可分析"}
        
        df = pd.DataFrame(self.articles)
        
        analysis = {
            "summary": self.get_summary_stats(df),
            "performance": self.analyze_performance_metrics(df),
            "trends": self.analyze_trends(df),
            "recommendations": self.generate_recommendations(df)
        }
        
        return analysis
    
    def get_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """获取汇总统计"""
        return {
            "total_articles": len(df),
            "total_reads": int(df['read_count'].sum()) if 'read_count' in df.columns else 0,
            "avg_reads": float(df['read_count'].mean()) if 'read_count' in df.columns else 0,
            "avg_like_rate": float(df['like_rate'].mean()) if 'like_rate' in df.columns else 0,
            "avg_share_rate": float(df['share_rate'].mean()) if 'share_rate' in df.columns else 0,
            "period": {
                "start_date": str(df['publish_date'].min()) if 'publish_date' in df.columns else "未知",
                "end_date": str(df['publish_date'].max()) if 'publish_date' in df.columns else "未知"
            }
        }
    
    def analyze_performance_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """分析表现指标"""
        metrics = {}
        
        # 阅读量分析
        if 'read_count' in df.columns:
            metrics['read_analysis'] = {
                "top_articles": self.get_top_articles(df, 'read_count', 5),
                "distribution": {
                    "min": int(df['read_count'].min()),
                    "max": int(df['read_count'].max()),
                    "median": int(df['read_count'].median()),
                    "std": float(df['read_count'].std())
                }
            }
        
        # 互动率分析
        if 'like_rate' in df.columns:
            metrics['interaction_analysis'] = {
                "top_like_rate": self.get_top_articles(df, 'like_rate', 5),
                "top_share_rate": self.get_top_articles(df, 'share_rate', 5) if 'share_rate' in df.columns else [],
                "avg_interaction_rate": {
                    "like": float(df['like_rate'].mean()),
                    "share": float(df['share_rate'].mean()) if 'share_rate' in df.columns else 0,
                    "comment": float(df['comment_rate'].mean()) if 'comment_rate' in df.columns else 0
                }
            }
        
        return metrics
    
    def analyze_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """分析趋势"""
        trends = {}
        
        # 时间趋势
        if 'publish_date' in df.columns:
            try:
                # 按日期分组
                df['publish_date'] = pd.to_datetime(df['publish_date'])
                daily_stats = df.groupby(df['publish_date'].dt.date).agg({
                    'read_count': 'sum',
                    'like_count': 'sum',
                    'share_count': 'sum'
                }).reset_index()
                
                trends['daily_trend'] = {
                    "dates": daily_stats['publish_date'].astype(str).tolist(),
                    "reads": daily_stats['read_count'].tolist(),
                    "likes": daily_stats['like_count'].tolist(),
                    "shares": daily_stats['share_count'].tolist()
                }
            except Exception as e:
                print(f"⚠️  时间趋势分析失败: {e}")
        
        # 星期几趋势
        if 'publish_weekday' in df.columns:
            try:
                weekday_stats = df.groupby('publish_weekday').agg({
                    'read_count': 'mean',
                    'like_rate': 'mean'
                }).reset_index()
                
                # 排序星期几
                weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                weekday_stats['publish_weekday'] = pd.Categorical(
                    weekday_stats['publish_weekday'], 
                    categories=weekday_order, 
                    ordered=True
                )
                weekday_stats = weekday_stats.sort_values('publish_weekday')
                
                trends['weekday_trend'] = {
                    "weekdays": weekday_stats['publish_weekday'].tolist(),
                    "avg_reads": weekday_stats['read_count'].tolist(),
                    "avg_like_rate": weekday_stats['like_rate'].tolist()
                }
            except Exception as e:
                print(f"⚠️  星期几趋势分析失败: {e}")
        
        # 发布时间趋势
        if 'publish_hour' in df.columns:
            try:
                hour_stats = df.groupby('publish_hour').agg({
                    'read_count': 'mean',
                    'like_rate': 'mean'
                }).reset_index()
                hour_stats = hour_stats.sort_values('publish_hour')
                
                trends['hour_trend'] = {
                    "hours": hour_stats['publish_hour'].tolist(),
                    "avg_reads": hour_stats['read_count'].tolist(),
                    "avg_like_rate": hour_stats['like_rate'].tolist()
                }
            except Exception as e:
                print(f"⚠️  发布时间趋势分析失败: {e}")
        
        return trends
    
    def generate_recommendations(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """生成优化建议"""
        recommendations = []
        
        # 基于表现数据的建议
        if 'read_count' in df.columns:
            avg_reads = df['read_count'].mean()
            low_performing = df[df['read_count'] < avg_reads * 0.5]
            
            if len(low_performing) > 0:
                recommendations.append({
                    "type": "内容优化",
                    "title": "低表现内容优化",
                    "description": f"发现 {len(low_performing)} 篇阅读量低于平均50%的文章",
                    "suggestions": [
                        "重新优化标题和摘要",
                        "在高峰时段重新发布",
                        "增加互动元素（投票、问答等）"
                    ]
                })
        
        # 基于互动率的建议
        if 'like_rate' in df.columns:
            avg_like_rate = df['like_rate'].mean()
            low_like_rate = df[df['like_rate'] < avg_like_rate * 0.5]
            
            if len(low_like_rate) > 0:
                recommendations.append({
                    "type": "互动优化",
                    "title": "提高内容互动性",
                    "description": f"发现 {len(low_like_rate)} 篇点赞率偏低的文章",
                    "suggestions": [
                        "增加号召性用语（CTA）",
                        "优化内容结尾，鼓励互动",
                        "添加更多实用技巧和价值点"
                    ]
                })
        
        # 基于发布时间建议
        if 'publish_hour' in df.columns and 'read_count' in df.columns:
            try:
                # 找出最佳发布时间
                hour_stats = df.groupby('publish_hour')['read_count'].mean()
                best_hour = hour_stats.idxmax()
                best_reads = hour_stats.max()
                
                recommendations.append({
                    "type": "发布时间优化",
                    "title": "优化发布时间",
                    "description": f"最佳发布时间: {best_hour}:00 (平均阅读量: {best_reads:.0f})",
                    "suggestions": [
                        f"建议在 {best_hour}:00 左右发布新内容",
                        "测试其他时间段的发布效果",
                        "考虑目标用户的活跃时间"
                    ]
                })
            except:
                pass
        
        # 基于内容类型建议（如果有分类信息）
        if 'review_score' in df.columns and 'read_count' in df.columns:
            try:
                # 分析审查评分和阅读量的关系
                correlation = df['review_score'].corr(df['read_count'])
                
                if correlation > 0.3:
                    recommendations.append({
                        "type": "质量保证",
                        "title": "内容质量与表现正相关",
                        "description": f"审查评分与阅读量相关性: {correlation:.2f}",
                        "suggestions": [
                            "继续重视内容审查和质量控制",
                            "优化审查维度，提高通过标准",
                            "将高质量内容优先分发"
                        ]
                    })
            except:
                pass
        
        return recommendations
    
    def get_top_articles(self, df: pd.DataFrame, metric: str, n: int = 5) -> List[Dict[str, Any]]:
        """获取表现最佳的文章"""
        if metric not in df.columns:
            return []
        
        top_articles = df.nlargest(n, metric)[['title', metric]]
        return top_articles.to_dict('records')


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self, analysis: Dict[str, Any], format: str = "markdown") -> str:
        """生成分析报告"""
        if format == "markdown":
            return self.generate_markdown_report(analysis)
        elif format == "html":
            return self.generate_html_report(analysis)
        else:
            return self.generate_markdown_report(analysis)
    
    def generate_markdown_report(self, analysis: Dict[str, Any]) -> str:
        """生成Markdown格式报告"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# 内容数据分析报告

**生成时间**: {now}  
**分析范围**: {analysis['summary']['total_articles']} 篇文章  
**时间范围**: {analysis['summary']['period']['start_date']} - {analysis['summary']['period']['end_date']}

## 📊 数据概览

| 指标 | 数值 |
|------|------|
| 文章总数 | {analysis['summary']['total_articles']} 篇 |
| 总阅读量 | {analysis['summary']['total_reads']:,} 次 |
| 平均阅读量 | {analysis['summary']['avg_reads']:.0f} 次/篇 |
| 平均点赞率 | {analysis['summary']['avg_like_rate']:.2f}% |
| 平均分享率 | {analysis['summary']['avg_share_rate']:.2f}% |

"""
        
        # 表现分析
        if 'performance' in analysis:
            report += "\n## 🏆 表现分析\n\n"
            
            # 阅读量分析
            if 'read_analysis' in analysis['performance']:
                read_analysis = analysis['performance']['read_analysis']
                
                report += "### 阅读量分析\n\n"
                report += f"- **分布范围**: {read_analysis['distribution']['min']:,} - {read_analysis['distribution']['max']:,} 次\n"
                report += f"- **中位数**: {read_analysis['distribution']['median']:,} 次\n"
                report += f"- **标准差**: {read_analysis['distribution']['std']:.0f} 次\n\n"
                
                report += "**阅读量最高的文章**:\n"
                for article in read_analysis['top_articles']:
                    report += f"- {article['title']}: {article['read_count']:,} 次\n"
                report += "\n"
            
            # 互动率分析
            if 'interaction_analysis' in analysis['performance']:
                interaction_analysis = analysis['performance']['interaction_analysis']
                
                report += "### 互动率分析\n\n"
                report += f"- **平均点赞率**: {interaction_analysis['avg_interaction_rate']['like']:.2f}%\n"
                report += f"- **平均分享率**: {interaction_analysis['avg_interaction_rate']['share']:.2f}%\n\n"
                
                report += "**点赞率最高的文章**:\n"
                for article in interaction_analysis['top_like_rate']:
                    report += f"- {article['title']}: {article['like_rate']:.2f}%\n"
                report += "\n"
        
        # 趋势分析
        if 'trends' in analysis:
            report += "\n## 📈 趋势分析\n\n"
            
            # 时间趋势
            if 'daily_trend' in analysis['trends']:
                daily_trend = analysis['trends']['daily_trend']
                if len(daily_trend['dates']) > 1:
                    report += "### 日趋势\n"
                    report += "- 每日阅读量波动情况\n"
                    report += "- 需关注连续下降或上升趋势\n\n"
            
            # 星期几趋势
            if 'weekday_trend' in analysis['trends']:
                weekday_trend = analysis['trends']['weekday_trend']
                
                report += "### 星期几表现\n\n"
                for i, weekday in enumerate(weekday_trend['weekdays']):
                    avg_reads = weekday_trend['avg_reads'][i]
                    avg_like_rate = weekday_trend['avg_like_rate'][i]
                    report += f"- **{weekday}**: 平均阅读量 {avg_reads:.0f} 次，点赞率 {avg_like_rate:.2f}%\n"
                report += "\n"
            
            # 发布时间趋势
            if 'hour_trend' in analysis['trends']:
                hour_trend = analysis['trends']['hour_trend']
                
                # 找出最佳时间
                best_idx = hour_trend['avg_reads'].index(max(hour_trend['avg_reads']))
                best_hour = hour_trend['hours'][best_idx]
                best_reads = hour_trend['avg_reads'][best_idx]
                
                report += "### 发布时间分析\n\n"
                report += f"- **最佳发布时间**: {best_hour}:00 (平均阅读量: {best_reads:.0f} 次)\n"
                report += "- 建议在最佳时间前后发布新内容\n\n"
        
        # 优化建议
        if 'recommendations' in analysis and analysis['recommendations']:
            report += "\n## 🎯 优化建议\n\n"
            
            for i, rec in enumerate(analysis['recommendations'], 1):
                report += f"### {i}. {rec['title']}\n\n"
                report += f"**类型**: {rec['type']}\n\n"
                report += f"**描述**: {rec['description']}\n\n"
                report += "**具体建议**:\n"
                for suggestion in rec['suggestions']:
                    report += f"- {suggestion}\n"
                report += "\n"
        
        report += "\n---\n"
        report += "*报告由 article-workflow content-analytics 生成*\n"
        
        return report
    
    def generate_html_report(self, analysis: Dict[str, Any]) -> str:
        """生成HTML格式报告（简化版）"""
        markdown_report = self.generate_markdown_report(analysis)
        
        # 简单的Markdown转HTML
        html_report = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>内容数据分析报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
        h1 {{ color: #333; border-bottom: 2px solid #4CAF50; }}
        h2 {{ color: #555; margin-top: 30px; }}
        h3 {{ color: #777; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .recommendation {{ background-color: #f9f9f9; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50; }}
        .summary {{ background-color: #e8f5e8; padding: 15px; border-radius: 5px; }}
    </style>
</head>
<body>
"""
        
        # 简单的Markdown解析
        lines = markdown_report.split('\n')
        for line in lines:
            if line.startswith('# '):
                html_report += f'<h1>{line[2:]}</h1>\n'
            elif line.startswith('## '):
                html_report += f'<h2>{line[3:]}</h2>\n'
            elif line.startswith('### '):
                html_report += f'<h3>{line[4:]}</h3>\n'
            elif line.startswith('|'):
                # 表格行
                if '---' in line:
                    continue
                cells = line.split('|')[1:-1]
                if len(cells) == 2:
                    html_report += f'<tr><td>{cells[0]}</td><td>{cells[1]}</td></tr>\n'
                else:
                    html_report += f'<p>{line}</p>\n'
            elif line.strip() == '':
                html_report += '<br>\n'
            else:
                html_report += f'<p>{line}</p>\n'
        
        html_report += """
</body>
</html>
"""
        
        return html_report
    
    def save_report(self, report: str, filename: str = None):
        """保存报告"""
        if filename is None:
            filename = f"content_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Markdown报告
        md_path = self.output_dir / f"{filename}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # HTML报告
        html_report = self.generate_html_report(
            json.loads(report) if 'summary' not in report else {}
        )
        html_path = self.output_dir / f"{filename}.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"✅ 报告已生成: {md_path}")
        print(f"✅ HTML版本: {html_path}")
        
        return str(md_path), str(html_path)


class ContentAnalytics:
    """内容数据分析器主类"""
    
    def __init__(self, config_loader: ConfigLoader, pipeline_manager: PipelineManager):
        self.config_loader = config_loader
        self.pipeline_manager = pipeline_manager
        self.data_sources = {}
        self.analyzers = {}
        self.output_dir = Path("output/analytics")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def load_config(self):
        """加载配置"""
        config = self.config_loader.load_config()
        analytics_config = config.get("content_analytics", {})
        
        # 设置输出目录
        custom_output_dir = analytics_config.get("output_dir")
        if custom_output_dir:
            self.output_dir = Path(custom_output_dir)
            self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置数据源
        self.enabled_sources = analytics_config.get("enabled_sources", ["wechat", "pipeline"])
    
    def analyze_content(self, data_source_type: str = None, data_path: str = None) -> Dict[str, Any]:
        """
        分析内容数据
        
        Args:
            data_source_type: 数据源类型 (wechat, pipeline, file)
            data_path: 数据文件路径（仅对wechat和file类型需要）
            
        Returns:
            分析结果字典
        """
        print(f"🔍 开始内容数据分析...")
        
        # 确定数据源
        if data_source_type is None:
            data_source_type = self.enabled_sources[0] if self.enabled_sources else "pipeline"
        
        # 加载数据源
        data_source = self.get_data_source(data_source_type, data_path)
        if not data_source:
            return {"error": f"数据源 {data_source_type} 加载失败"}
        
        # 创建分析器并分析
        analyzer = ContentAnalyzer(data_source)
        analysis = analyzer.analyze_performance()
        
        # 生成报告
        report_generator = ReportGenerator(self.output_dir)
        report = report_generator.generate_report(analysis, "markdown")
        md_path, html_path = report_generator.save_report(report)
        
        # 添加报告路径到分析结果
        analysis["report_paths"] = {
            "markdown": md_path,
            "html": html_path
        }
        
        return analysis
    
    def get_data_source(self, source_type: str, data_path: str = None) -> Optional[DataSource]:
        """获取数据源实例"""
        if source_type == "wechat":
            if not data_path:
                print("❌ 微信数据源需要指定数据文件路径")
                return None
            
            data_source = WeChatDataSource()
            if data_source.load(data_path):
                return data_source
        
        elif source_type == "pipeline":
            data_source = PipelineDataSource(self.pipeline_manager)
            if data_source.load():
                return data_source
        
        elif source_type == "file":
            if not data_path:
                print("❌ 文件数据源需要指定数据文件路径")
                return None
            
            # 根据文件扩展名选择合适的数据源
            if data_path.endswith(('.csv', '.xlsx', '.xls')):
                data_source = WeChatDataSource()
                if data_source.load(data_path):
                    return data_source
        
        print(f"❌ 不支持的数据源类型: {source_type}")
        return None
    
    def compare_sources(self, source1_type: str, source1_path: str, 
                        source2_type: str, source2_path: str) -> Dict[str, Any]:
        """比较两个数据源"""
        print(f"🔍 比较数据源: {source1_type} vs {source2_type}")
        
        # 加载两个数据源
        source1 = self.get_data_source(source1_type, source1_path)
        source2 = self.get_data_source(source2_type, source2_path)
        
        if not source1 or not source2:
            return {"error": "数据源加载失败"}
        
        # 分析两个数据源
        analyzer1 = ContentAnalyzer(source1)
        analyzer2 = ContentAnalyzer(source2)
        
        analysis1 = analyzer1.analyze_performance()
        analysis2 = analyzer2.analyze_performance()
        
        # 生成对比报告
        comparison = {
            "source1": analysis1,
            "source2": analysis2,
            "differences": self.find_differences(analysis1, analysis2)
        }
        
        return comparison
    
    def find_differences(self, analysis1: Dict[str, Any], analysis2: Dict[str, Any]) -> Dict[str, Any]:
        """找出两个分析的差异"""
        differences = {}
        
        # 比较汇总统计
        if 'summary' in analysis1 and 'summary' in analysis2:
            summary1 = analysis1['summary']
            summary2 = analysis2['summary']
            
            diff_summary = {}
            for key in summary1:
                if key in summary2:
                    val1 = summary1[key]
                    val2 = summary2[key]
                    
                    if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                        diff = abs(val1 - val2)
                        if diff > 0:
                            diff_summary[key] = {
                                "source1": val1,
                                "source2": val2,
                                "difference": diff,
                                "percent_diff": abs(val1 - val2) / max(abs(val1), abs(val2)) * 100 if max(abs(val1), abs(val2)) > 0 else 0
                            }
            
            if diff_summary:
                differences['summary'] = diff_summary
        
        return differences


def main():
    """主函数"""
    print("📊 content-analytics - 内容数据分析器")
    print("=" * 50)
    
    # 加载配置
    config_loader = ConfigLoader()
    
    try:
        config_loader.load_config()
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        print("请先运行配置向导: python scripts/config_wizard.py")
        sys.exit(1)
    
    # 创建流水线管理器
    pipeline_manager = PipelineManager()
    
    # 创建数据分析器
    analytics = ContentAnalytics(config_loader, pipeline_manager)
    analytics.load_config()
    
    # 解析命令行参数
    import argparse
    parser = argparse.ArgumentParser(description="内容数据分析器")
    parser.add_argument("--source", help="数据源类型 (wechat, pipeline, file)")
    parser.add_argument("--data", help="数据文件路径（对wechat和file类型需要）")
    parser.add_argument("--compare", nargs=2, help="比较两个数据源，格式: 类型1:路径1 类型2:路径2")
    
    args = parser.parse_args()
    
    if args.compare:
        # 比较模式
        source1_spec = args.compare[0].split(':')
        source2_spec = args.compare[1].split(':')
        
        if len(source1_spec) != 2 or len(source2_spec) != 2:
            print("❌ 比较参数格式错误，应为: 类型:路径")
            sys.exit(1)
        
        source1_type, source1_path = source1_spec
        source2_type, source2_path = source2_spec
        
        result = analytics.compare_sources(
            source1_type, source1_path,
            source2_type, source2_path
        )
        
        if "error" in result:
            print(f"❌ 比较失败: {result['error']}")
        else:
            print("✅ 比较完成")
            print(f"📊 差异数量: {len(result.get('differences', {}))}")
            
            # 保存比较结果
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            result_file = analytics.output_dir / f"comparison_{now}.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"📁 结果文件: {result_file}")
    
    else:
        # 分析模式
        result = analytics.analyze_content(args.source, args.data)
        
        if "error" in result:
            print(f"❌ 分析失败: {result['error']}")
        else:
            print("✅ 分析完成")
            print(f"📊 分析文章: {result['summary']['total_articles']} 篇")
            print(f"📈 总阅读量: {result['summary']['total_reads']:,} 次")
            print(f"📁 报告文件: {result['report_paths']['markdown']}")
            
            # 显示关键建议
            if 'recommendations' in result and result['recommendations']:
                print("\n🎯 关键建议:")
                for i, rec in enumerate(result['recommendations'][:3], 1):
                    print(f"  {i}. {rec['title']}: {rec['description']}")


if __name__ == "__main__":
    main()