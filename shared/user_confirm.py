#!/usr/bin/env python3
"""
User Confirmation Manager for article-workflow

处理流水线中的用户确认节点，包括：
- 显示确认选项
- 记录用户选择
- 管理确认状态
- 提供默认值
"""

import os
import sys
import json
from typing import Dict, List, Optional, Any
from enum import Enum


class ConfirmationType(Enum):
    """确认类型"""
    
    # 选题确认
    TOPIC_SELECTION = "topic_selection"
    
    # 内容相关确认
    CONTENT_REVIEW_RESULT = "content_review_result"
    CONTENT_REVISION = "content_revision"
    
    # SEO 相关确认
    SEO_TITLE_SELECTION = "seo_title_selection"
    SEO_DIGEST_CONFIRMATION = "seo_digest_confirmation"
    SEO_COVER_IMAGE = "seo_cover_image"
    
    # 发布相关确认
    PREVIEW_CONFIRMATION = "preview_confirmation"
    DRAFT_UPLOAD_CONFIRMATION = "draft_upload_confirmation"
    FINAL_PUBLISH_CONFIRMATION = "final_publish_confirmation"
    
    # 分发确认
    MULTI_PLATFORM_DISTRIBUTION = "multi_platform_distribution"
    
    # 其他确认
    CONTINUE_PIPELINE = "continue_pipeline"
    RETRY_OPERATION = "retry_operation"


class UserConfirm:
    """用户确认管理器"""
    
    def __init__(self, pipeline_id: Optional[str] = None):
        """
        初始化用户确认管理器
        
        Args:
            pipeline_id: 流水线 ID（可选）
        """
        self.pipeline_id = pipeline_id
        self.confirmations_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config",
            "confirmations"
        )
        os.makedirs(self.confirmations_dir, exist_ok=True)
    
    def _get_confirmation_file(self, confirmation_type: str) -> str:
        """获取确认文件路径"""
        if self.pipeline_id:
            return os.path.join(
                self.confirmations_dir, 
                f"{self.pipeline_id}_{confirmation_type}.json"
            )
        else:
            return os.path.join(
                self.confirmations_dir,
                f"{confirmation_type}.json"
            )
    
    def show_confirmation(
        self,
        confirmation_type: str,
        title: str,
        message: str,
        options: List[Dict[str, Any]],
        default_option: Optional[str] = None,
        require_input: bool = True
    ) -> Dict[str, Any]:
        """
        显示确认对话框
        
        Args:
            confirmation_type: 确认类型
            title: 标题
            message: 消息内容
            options: 选项列表 [{"id": "option1", "label": "选项1", "description": "描述"}]
            default_option: 默认选项 ID
            require_input: 是否必须输入
            
        Returns:
            用户选择
        """
        print(f"\n{'='*60}")
        print(f"📋 {title}")
        print(f"{'='*60}")
        print(f"{message}\n")
        
        # 显示选项
        for i, option in enumerate(options, 1):
            print(f"{i}. {option['label']}")
            if "description" in option:
                print(f"   {option['description']}")
            print()
        
        # 如果有默认选项，提示
        if default_option:
            default_idx = next(
                (i for i, opt in enumerate(options) if opt["id"] == default_option),
                0
            ) + 1
            print(f"💡 建议选择: {default_idx} ({options[default_idx-1]['label']})\n")
        
        # 获取用户输入
        while True:
            try:
                if not require_input and default_option:
                    print("按回车使用默认选项，或输入选择编号:")
                else:
                    print("请输入选择编号:")
                
                choice = input("> ").strip()
                
                if not choice and default_option and not require_input:
                    # 使用默认选项
                    choice_idx = default_idx
                    selected_option = options[choice_idx - 1]
                    print(f"✅ 使用默认选项: {selected_option['label']}")
                    break
                elif choice.isdigit():
                    choice_idx = int(choice)
                    if 1 <= choice_idx <= len(options):
                        selected_option = options[choice_idx - 1]
                        print(f"✅ 已选择: {selected_option['label']}")
                        break
                    else:
                        print(f"❌ 请输入 1-{len(options)} 之间的数字")
                else:
                    print(f"❌ 请输入数字")
            
            except KeyboardInterrupt:
                print("\n⚠️  用户取消操作")
                return {
                    "confirmed": False,
                    "option_id": None,
                    "reason": "user_cancelled"
                }
            except Exception as e:
                print(f"❌ 输入错误: {e}")
                continue
        
        # 记录确认结果
        result = {
            "confirmed": True,
            "option_id": selected_option["id"],
            "option_label": selected_option["label"],
            "pipeline_id": self.pipeline_id,
            "confirmation_type": confirmation_type,
            "timestamp": self._get_timestamp(),
        }
        
        # 保存到文件
        self.save_confirmation(confirmation_type, result)
        
        return result
    
    def save_confirmation(self, confirmation_type: str, data: Dict[str, Any]):
        """保存确认结果"""
        file_path = self._get_confirmation_file(confirmation_type)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_confirmation(self, confirmation_type: str) -> Optional[Dict[str, Any]]:
        """加载确认结果"""
        file_path = self._get_confirmation_file(confirmation_type)
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return None
        return None
    
    def has_confirmed(self, confirmation_type: str) -> bool:
        """检查是否已确认"""
        data = self.load_confirmation(confirmation_type)
        return bool(data and data.get("confirmed", False))
    
    def get_confirmation_value(self, confirmation_type: str, key: str, default: Any = None) -> Any:
        """获取确认结果中的特定值"""
        data = self.load_confirmation(confirmation_type)
        return data.get(key, default) if data else default
    
    @staticmethod
    def _get_timestamp() -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    # 预定义的确认流程
    
    def confirm_topic_selection(self, topics: List[Dict]) -> Dict[str, Any]:
        """
        确认选题选择
        
        Args:
            topics: 选题列表 [{"id": "...", "title": "...", "description": "...", "difficulty": "..."}]
            
        Returns:
            确认结果
        """
        options = []
        for topic in topics:
            options.append({
                "id": topic["id"],
                "label": topic["title"],
                "description": f"难度: {topic.get('difficulty', '中')} | {topic.get('description', '')}"
            })
        
        # 添加"跳过选题规划"选项
        options.append({
            "id": "skip_topic_planning",
            "label": "跳过选题规划，直接指定主题",
            "description": "手动输入文章主题"
        })
        
        return self.show_confirmation(
            confirmation_type=ConfirmationType.TOPIC_SELECTION.value,
            title="选题确认",
            message="请从以下选题中选择一个，或跳过选题规划：",
            options=options,
            default_option=topics[0]["id"] if topics else None,
            require_input=False
        )
    
    def confirm_content_review(self, score: int, passed: bool, suggestions: List[str]) -> Dict[str, Any]:
        """
        确认内容审查结果
        
        Args:
            score: 总分
            passed: 是否通过
            suggestions: 修改建议
            
        Returns:
            确认结果
        """
        title = "内容审查结果"
        if passed:
            message = f"✅ 内容审查通过！\n总分: {score}/70 (≥55分)\n"
            options = [
                {
                    "id": "continue",
                    "label": "继续下一步",
                    "description": "进入 SEO 优化阶段"
                }
            ]
            default_option = "continue"
        else:
            message = f"⚠️ 内容审查未通过\n总分: {score}/70 (<55分)\n\n修改建议：\n"
            for i, suggestion in enumerate(suggestions[:5], 1):
                message += f"{i}. {suggestion}\n"
            
            options = [
                {
                    "id": "modify_and_retry",
                    "label": "修改后重新审查",
                    "description": "根据建议修改内容，然后重新审查"
                },
                {
                    "id": "continue_anyway",
                    "label": "继续下一步（不推荐）",
                    "description": "跳过审查，直接进入 SEO 优化"
                },
                {
                    "id": "abandon",
                    "label": "放弃当前文章",
                    "description": "放弃当前内容，重新开始"
                }
            ]
            default_option = "modify_and_retry"
        
        return self.show_confirmation(
            confirmation_type=ConfirmationType.CONTENT_REVIEW_RESULT.value,
            title=title,
            message=message,
            options=options,
            default_option=default_option
        )
    
    def confirm_seo_title(self, title_options: List[Dict]) -> Dict[str, Any]:
        """
        确认 SEO 标题选择
        
        Args:
            title_options: 标题选项列表 [
                {"id": "option1", "title": "...", "formula": "...", "score": ...}
            ]
            
        Returns:
            确认结果
        """
        message = "请从以下标题方案中选择一个：\n"
        options = []
        
        for i, option in enumerate(title_options, 1):
            score = option.get("score", 0)
            formula = option.get("formula", "")
            title = option.get("title", "")
            
            options.append({
                "id": option["id"],
                "label": f"【{score}分】{title}",
                "description": formula
            })
            
            message += f"\n{i}. {title}\n   公式: {formula}\n   评分: {score}/100\n"
        
        # 添加"重新生成"选项
        options.append({
            "id": "regenerate",
            "label": "重新生成标题方案",
            "description": "生成新的标题方案"
        })
        
        return self.show_confirmation(
            confirmation_type=ConfirmationType.SEO_TITLE_SELECTION.value,
            title="SEO 标题选择",
            message=message,
            options=options,
            default_option=title_options[0]["id"] if title_options else None
        )
    
    def confirm_preview(self, html_path: str) -> Dict[str, Any]:
        """
        确认预览效果
        
        Args:
            html_path: HTML 预览文件路径
            
        Returns:
            确认结果
        """
        message = f"已生成微信格式预览文件：\n{html_path}\n\n"
        message += "请确认预览效果是否满意："
        
        options = [
            {
                "id": "upload_draft",
                "label": "效果满意，上传到草稿箱",
                "description": "将文章上传到微信公众号草稿箱"
            },
            {
                "id": "regenerate",
                "label": "重新生成预览",
                "description": "选择其他主题重新生成"
            },
            {
                "id": "modify_content",
                "label": "返回修改内容",
                "description": "回到内容编辑阶段"
            }
        ]
        
        return self.show_confirmation(
            confirmation_type=ConfirmationType.PREVIEW_CONFIRMATION.value,
            title="预览确认",
            message=message,
            options=options,
            default_option="upload_draft",
            require_input=False
        )
    
    def confirm_publish(self, draft_info: Dict) -> Dict[str, Any]:
        """
        确认最终发布
        
        Args:
            draft_info: 草稿信息 {"title": "...", "author": "...", "draft_media_id": "..."}
            
        Returns:
            确认结果
        """
        message = f"文章已上传到微信公众号草稿箱：\n\n"
        message += f"标题: {draft_info.get('title', '')}\n"
        message += f"作者: {draft_info.get('author', '')}\n"
        message += f"草稿ID: {draft_info.get('draft_media_id', '')[:8]}...\n\n"
        message += "请登录微信公众号后台确认并发布："
        
        options = [
            {
                "id": "publish_now",
                "label": "已确认发布",
                "description": "我已确认发布文章"
            },
            {
                "id": "publish_later",
                "label": "稍后发布",
                "description": "我将在微信公众号后台手动发布"
            },
            {
                "id": "cancel_publish",
                "label": "取消发布",
                "description": "不发布此文章"
            }
        ]
        
        return self.show_confirmation(
            confirmation_type=ConfirmationType.FINAL_PUBLISH_CONFIRMATION.value,
            title="发布确认",
            message=message,
            options=options,
            default_option="publish_now",
            require_input=False
        )


if __name__ == "__main__":
    print("User Confirmation Manager for article-workflow")
    print()
    
    # 测试示例
    uc = UserConfirm(pipeline_id="test-001")
    
    # 测试选题确认
    print("1. 选题确认测试:")
    topics = [
        {"id": "topic1", "title": "AI 编程工具对比", "description": "对比各种 AI 编程工具的优缺点", "difficulty": "中"},
        {"id": "topic2", "title": "Docker 入门教程", "description": "适合新手的 Docker 入门指南", "difficulty": "易"},
        {"id": "topic3", "title": "微服务架构设计", "description": "深入探讨微服务架构的最佳实践", "difficulty": "难"},
    ]
    result = uc.confirm_topic_selection(topics)
    print(f"   结果: {result}")
    print()
    
    # 测试内容审查确认
    print("2. 内容审查确认测试:")
    result = uc.confirm_content_review(
        score=48,
        passed=False,
        suggestions=[
            "标题吸引力不足，建议优化",
            "逻辑结构不够清晰",
            "缺少具体的代码示例"
        ]
    )
    print(f"   结果: {result}")
    print()
    
    # 测试是否已确认
    print(f"3. 已确认内容审查: {uc.has_confirmed('content_review_result')}")
    print()
    
    print("✅ 测试完成")
