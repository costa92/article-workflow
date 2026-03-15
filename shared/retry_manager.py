#!/usr/bin/env python3
"""
Retry Manager for article-workflow

处理流水线中的重试逻辑，包括：
- 检查重试条件
- 管理重试计数
- 决定何时停止重试
- 提供重建议
"""

import os
import time
from typing import Dict, Optional, Tuple
from enum import Enum


class RetryableErrorType(Enum):
    """可重试的错误类型"""
    
    # 网络相关错误
    NETWORK_TIMEOUT = "network_timeout"
    NETWORK_ERROR = "network_error"
    
    # API 相关错误
    API_RATE_LIMIT = "api_rate_limit"
    API_TEMPORARY_ERROR = "api_temporary_error"
    API_QUOTA_EXCEEDED = "api_quota_exceeded"
    
    # 内容相关错误
    CONTENT_REVIEW_FAILED = "content_review_failed"
    SEO_TITLE_UNSATISFIED = "seo_title_unsatisfied"
    IMAGE_GENERATION_FAILED = "image_generation_failed"
    
    # 文件系统错误
    FILE_SYSTEM_ERROR = "file_system_error"
    PERMISSION_ERROR = "permission_error"
    
    # 其他可恢复错误
    OTHER_RECOVERABLE = "other_recoverable"


class NonRetryableErrorType(Enum):
    """不可重试的错误类型（致命错误）"""
    
    # 认证相关错误
    AUTHENTICATION_FAILED = "authentication_failed"
    IP_WHITELIST_ERROR = "ip_whitelist_error"
    INVALID_APP_CONFIG = "invalid_app_config"
    
    # 资源错误
    MATERIAL_LIMIT_EXCEEDED = "material_limit_exceeded"
    DRAFT_BOX_FULL = "draft_box_full"
    
    # 业务逻辑错误
    INVALID_INPUT = "invalid_input"
    FILE_NOT_FOUND = "file_not_found"
    
    # 用户决策错误
    USER_CANCELLED = "user_cancelled"
    USER_REJECTED = "user_rejected"


class RetryManager:
    """重试管理器"""
    
    # 重试配置
    DEFAULT_RETRY_CONFIG = {
        # 网络相关错误
        "network_error": {"max_retries": 2, "backoff_base": 2.0, "max_backoff": 30},
        "network_timeout": {"max_retries": 2, "backoff_base": 2.0, "max_backoff": 30},
        
        # API 相关错误
        "api_rate_limit": {"max_retries": 3, "backoff_base": 2.0, "max_backoff": 60},
        "api_temporary_error": {"max_retries": 2, "backoff_base": 2.0, "max_backoff": 30},
        "api_quota_exceeded": {"max_retries": 0, "backoff_base": 0, "max_backoff": 0},  # 不可重试
        
        # 内容相关错误
        "content_review_failed": {"max_retries": 3, "backoff_base": 1.0, "max_backoff": 0},
        "seo_title_unsatisfied": {"max_retries": 1, "backoff_base": 1.0, "max_backoff": 0},
        "image_generation_failed": {"max_retries": 2, "backoff_base": 2.0, "max_backoff": 10},
        
        # 文件系统错误
        "file_system_error": {"max_retries": 1, "backoff_base": 1.0, "max_backoff": 5},
        "permission_error": {"max_retries": 0, "backoff_base": 0, "max_backoff": 0},  # 不可重试
        
        # 其他可恢复错误
        "other_recoverable": {"max_retries": 1, "backoff_base": 1.0, "max_backoff": 5},
        
        # 枚举值映射
        RetryableErrorType.NETWORK_TIMEOUT.value: {"max_retries": 2, "backoff_base": 2.0, "max_backoff": 30},
        RetryableErrorType.NETWORK_ERROR.value: {"max_retries": 2, "backoff_base": 2.0, "max_backoff": 30},
        RetryableErrorType.API_RATE_LIMIT.value: {"max_retries": 3, "backoff_base": 2.0, "max_backoff": 60},
        RetryableErrorType.API_TEMPORARY_ERROR.value: {"max_retries": 2, "backoff_base": 2.0, "max_backoff": 30},
        RetryableErrorType.API_QUOTA_EXCEEDED.value: {"max_retries": 0, "backoff_base": 0, "max_backoff": 0},
        RetryableErrorType.CONTENT_REVIEW_FAILED.value: {"max_retries": 3, "backoff_base": 1.0, "max_backoff": 0},
        RetryableErrorType.SEO_TITLE_UNSATISFIED.value: {"max_retries": 1, "backoff_base": 1.0, "max_backoff": 0},
        RetryableErrorType.IMAGE_GENERATION_FAILED.value: {"max_retries": 2, "backoff_base": 2.0, "max_backoff": 10},
        RetryableErrorType.FILE_SYSTEM_ERROR.value: {"max_retries": 1, "backoff_base": 1.0, "max_backoff": 5},
        RetryableErrorType.PERMISSION_ERROR.value: {"max_retries": 0, "backoff_base": 0, "max_backoff": 0},
        RetryableErrorType.OTHER_RECOVERABLE.value: {"max_retries": 1, "backoff_base": 1.0, "max_backoff": 5},
    }
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化重试管理器
        
        Args:
            config: 自定义重试配置
        """
        self.config = config or self.DEFAULT_RETRY_CONFIG
        self.error_history = []
    
    def classify_error(self, error_message: str) -> Tuple[str, bool]:
        """
        根据错误消息分类错误类型
        
        Args:
            error_message: 错误消息
            
        Returns:
            (error_type, is_retryable)
        """
        error_message_lower = error_message.lower()
        
        # 检查不可重试的错误类型
        if any(keyword in error_message_lower for keyword in [
            "invalid ip", "not in whitelist", "ip whitelist",
        ]):
            return (NonRetryableErrorType.IP_WHITELIST_ERROR.value, False)
        
        if any(keyword in error_message_lower for keyword in [
            "invalid appid", "invalid secret", "invalid app", "appid not exist",
        ]):
            return (NonRetryableErrorType.AUTHENTICATION_FAILED.value, False)
        
        if any(keyword in error_message_lower for keyword in [
            "material limit exceeded", "draft box full",
        ]):
            return (NonRetryableErrorType.MATERIAL_LIMIT_EXCEEDED.value, False)
        
        if any(keyword in error_message_lower for keyword in [
            "file not found", "no such file", "cannot find",
        ]):
            return (NonRetryableErrorType.FILE_NOT_FOUND.value, False)
        
        # 检查可重试的错误类型
        if any(keyword in error_message_lower for keyword in [
            "timeout", "timed out", "connection timeout", "request timeout",
        ]):
            return (RetryableErrorType.NETWORK_TIMEOUT.value, True)
        
        if any(keyword in error_message_lower for keyword in [
            "network error", "connection refused", "connection reset", "socket error",
        ]):
            return (RetryableErrorType.NETWORK_ERROR.value, True)
        
        if any(keyword in error_message_lower for keyword in [
            "rate limit", "too many requests", "429", "rate exceeded",
        ]):
            return (RetryableErrorType.API_RATE_LIMIT.value, True)
        
        if any(keyword in error_message_lower for keyword in [
            "quota exceeded", "insufficient quota", "quota limit",
        ]):
            return (RetryableErrorType.API_QUOTA_EXCEEDED.value, True)
        
        # 内容相关错误（通过消息中的关键词判断）
        if any(keyword in error_message_lower for keyword in [
            "score <", "score less than", "review failed", "not passed",
        ]):
            return (RetryableErrorType.CONTENT_REVIEW_FAILED.value, True)
        
        if any(keyword in error_message_lower for keyword in [
            "image generation failed", "failed to generate image", "gemini api error",
        ]):
            return (RetryableErrorType.IMAGE_GENERATION_FAILED.value, True)
        
        # 默认返回可恢复错误
        return (RetryableErrorType.OTHER_RECOVERABLE.value, True)
    
    def can_retry(self, error_type: str, retry_count: int) -> Tuple[bool, str]:
        """
        检查是否可以重试
        
        Args:
            error_type: 错误类型
            retry_count: 当前重试次数
            
        Returns:
            (can_retry, reason_message)
        """
        # 首先检查是否是枚举值（去掉后缀的value）
        if hasattr(NonRetryableErrorType, error_type.upper()):
            return (False, "此错误类型不可重试")
        
        if error_type not in self.config:
            # 如果错误类型不在配置中，检查是否是枚举值
            enum_value = None
            for enum_cls in [RetryableErrorType, NonRetryableErrorType]:
                for member in enum_cls:
                    if member.value == error_type:
                        enum_value = member
                        break
            
            if enum_value is None:
                return (False, f"未知错误类型: {error_type}")
            
            # 如果是不可重试错误类型
            if isinstance(enum_value, NonRetryableErrorType):
                return (False, "此错误类型不可重试")
        
        # 检查配置
        max_retries = self.config.get(error_type, {}).get("max_retries", 0)
        
        if max_retries <= 0:
            return (False, "此错误类型不可重试")
        
        if retry_count >= max_retries:
            return (False, f"已达到最大重试次数 ({max_retries})")
        
        return (True, "可以重试")
    
    def get_backoff_seconds(self, error_type: str, retry_count: int) -> float:
        """
        获取退避时间（秒）
        
        Args:
            error_type: 错误类型
            retry_count: 当前重试次数（0为第一次重试）
            
        Returns:
            等待秒数
        """
        if error_type not in self.config:
            # 检查是否是枚举值
            config = self.config.get(RetryableErrorType.OTHER_RECOVERABLE.value, {})
        else:
            config = self.config[error_type]
        
        backoff_base = config.get("backoff_base", 1.0)
        max_backoff = config.get("max_backoff", 0)
        
        if backoff_base <= 1.0:
            return 0
        
        # 指数退避
        backoff = min(backoff_base ** retry_count, max_backoff)
        
        # 添加随机抖动（±20%）
        import random
        jitter = random.uniform(0.8, 1.2)
        
        return backoff * jitter
    
    def record_error(self, error_type: str, error_message: str, stage: str):
        """
        记录错误
        
        Args:
            error_type: 错误类型
            error_message: 错误消息
            stage: 发生错误的阶段
        """
        self.error_history.append({
            "timestamp": time.time(),
            "error_type": error_type,
            "error_message": error_message,
            "stage": stage,
        })
    
    def get_recommendation(self, error_type: str, retry_count: int) -> str:
        """
        获取重试建议
        
        Args:
            error_type: 错误类型
            retry_count: 当前重试次数
            
        Returns:
            建议消息
        """
        recommendations = {
            # 网络相关错误
            "network_timeout": "网络超时，建议检查网络连接",
            "network_error": "网络错误，建议稍后重试",
            
            # API 相关错误
            "api_rate_limit": "API 频率限制，建议等待一段时间后重试",
            "api_quota_exceeded": "API 配额已用完，请检查账户余额",
            "api_temporary_error": "API 临时错误，建议稍后重试",
            
            # 内容相关错误
            "content_review_failed": f"内容审查未通过，第 {retry_count + 1} 次尝试修改",
            "seo_title_unsatisfied": "SEO 标题不满意，建议重新生成标题方案",
            "image_generation_failed": "图片生成失败，可以跳过或使用本地图片",
            
            # 认证错误
            "ip_whitelist_error": "IP 不在白名单中，请登录微信公众号平台配置 IP 白名单",
            "authentication_failed": "认证失败，请检查 AppID 和 Secret 配置",
            
            # 资源错误
            "material_limit_exceeded": "素材数量超限，请清理微信公众号素材库",
            "draft_box_full": "草稿箱已满，请清理微信公众号草稿箱",
            
            # 其他
            "file_not_found": "文件不存在，请检查文件路径",
            "user_cancelled": "用户取消操作",
            "user_rejected": "用户拒绝操作",
        }
        
        # 检查枚举值
        if error_type in recommendations:
            return recommendations[error_type]
        
        # 尝试匹配枚举成员
        for enum_cls in [RetryableErrorType, NonRetryableErrorType]:
            for member in enum_cls:
                if member.value == error_type:
                    # 返回通用建议
                    if isinstance(member, NonRetryableErrorType):
                        return "此错误不可重试，需要手动处理"
                    else:
                        return f"可恢复错误，建议稍后重试（第 {retry_count + 1} 次）"
        
        return "未知错误，请检查日志"
    
    def should_fallback(self, error_type: str, retry_count: int) -> Tuple[bool, str]:
        """
        检查是否应该回退到备选方案
        
        Args:
            error_type: 错误类型
            retry_count: 当前重试次数
            
        Returns:
            (should_fallback, fallback_action)
        """
        fallback_actions = {
            "image_generation_failed": "跳过自动图片生成，使用默认图片或手动添加",
            "seo_title_unsatisfied": "使用原标题，不进行 SEO 优化",
            "content_review_failed": "用户手动修改内容",
        }
        
        if error_type in fallback_actions:
            config = self.config.get(error_type, {"max_retries": 0})
            if retry_count >= config["max_retries"]:
                return (True, fallback_actions[error_type])
        
        return (False, "")


if __name__ == "__main__":
    print("Retry Manager for article-workflow")
    print()
    
    # 测试示例
    manager = RetryManager()
    
    test_errors = [
        "invalid ip 192.168.1.1, not in whitelist",
        "network timeout while connecting to api",
        "score < 55, need revision",
        "Gemini API error: quota exceeded",
        "file not found: /path/to/article.md",
    ]
    
    for error in test_errors:
        error_type, is_retryable = manager.classify_error(error)
        can_retry, reason = manager.can_retry(error_type, 0)
        backoff = manager.get_backoff_seconds(error_type, 0)
        recommendation = manager.get_recommendation(error_type, 0)
        
        print(f"错误: {error[:50]}...")
        print(f"  类型: {error_type}")
        print(f"  可重试: {is_retryable}")
        print(f"  可以重试: {can_retry} ({reason})")
        print(f"  退避时间: {backoff:.1f} 秒")
        print(f"  建议: {recommendation}")
        print()
