#!/usr/bin/env python3
"""
Pipeline Manager for article-workflow

用于跟踪和管理流水线执行状态，包括：
- 创建新的流水线执行记录
- 更新阶段执行状态
- 记录错误和重试
- 查询流水线历史
"""

import os
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List

# 获取插件根目录
PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(PLUGIN_ROOT, "config")
METADATA_DIR = os.path.join(CONFIG_DIR, "pipeline_metadata")

# 确保目录存在
os.makedirs(METADATA_DIR, exist_ok=True)


class PipelineManager:
    """流水线管理器"""

    def __init__(self, pipeline_id: Optional[str] = None):
        """
        初始化流水线管理器

        Args:
            pipeline_id: 流水线 ID，如果为 None 则自动生成
        """
        if pipeline_id is None:
            pipeline_id = self._generate_pipeline_id()
        
        self.pipeline_id = pipeline_id
        self.metadata_file = os.path.join(METADATA_DIR, f"{pipeline_id}.yaml")
        self.metadata = self._load_or_create_metadata()

    @staticmethod
    def _generate_pipeline_id() -> str:
        """生成唯一的流水线 ID"""
        now = datetime.now()
        count = 1
        base_id = now.strftime("%Y-%m-%d")
        
        # 检查是否已存在同日期的流水线
        for i in range(1, 1000):
            candidate_id = f"{base_id}-{i:03d}"
            if not os.path.exists(os.path.join(METADATA_DIR, f"{candidate_id}.yaml")):
                return candidate_id
        
        return f"{base_id}-999"

    def _load_or_create_metadata(self) -> Dict:
        """加载或创建元数据文件"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        else:
            return self._create_empty_metadata()

    @staticmethod
    def _create_empty_metadata() -> Dict:
        """创建空的元数据结构"""
        return {
            "pipeline_id": None,
            "start_time": None,
            "user_id": None,
            "execution": {
                "current_stage": "draft",
                "status": "pending",
                "retry_count": 0,
                "max_retries": 3,
                "error_message": None,
            },
            "article": {
                "title": "",
                "description": "",
                "file_path": "",
                "file_size_kb": 0,
                "word_count": 0,
                "tags": [],
                "status": "draft",
            },
            "stages": {},
            "confirmations": {
                "seo_title_confirmed": False,
                "preview_confirmed": False,
                "publish_confirmed": False,
            },
            "error_history": [],
            "summary": {
                "total_duration_seconds": 0,
                "stages_completed": 0,
                "stages_total": 8,
                "completion_percentage": 0,
                "success": False,
                "final_status": "in_progress",
                "notes": "",
            },
        }

    def save(self):
        """保存元数据到文件"""
        os.makedirs(os.path.dirname(self.metadata_file), exist_ok=True)
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            yaml.dump(self.metadata, f, allow_unicode=True, default_flow_style=False)

    def start_pipeline(self, article_file: str, user_id: Optional[str] = None):
        """
        启动流水线

        Args:
            article_file: 文章文件路径
            user_id: 用户 ID
        """
        self.metadata["pipeline_id"] = self.pipeline_id
        self.metadata["start_time"] = datetime.now().isoformat()
        self.metadata["user_id"] = user_id
        self.metadata["execution"]["status"] = "in_progress"
        self.metadata["article"]["file_path"] = article_file
        
        # 更新文件大小
        if os.path.exists(article_file):
            file_size_kb = os.path.getsize(article_file) / 1024
            self.metadata["article"]["file_size_kb"] = round(file_size_kb, 2)
        
        self.save()

    def update_stage(self, stage_name: str, status: str, 
                    output_file: Optional[str] = None, 
                    error: Optional[str] = None,
                    **kwargs):
        """
        更新阶段执行状态

        Args:
            stage_name: 阶段名称 (planner|generator|reviewer|seo|converter|publish|repurpose|analytics)
            status: 状态 (pending|completed|skipped|failed)
            output_file: 输出文件路径
            error: 错误信息
            **kwargs: 其他阶段特定信息
        """
        if stage_name not in self.metadata["stages"]:
            self.metadata["stages"][stage_name] = {
                "executed": False,
                "start_time": None,
                "end_time": None,
                "duration_seconds": 0,
                "status": "pending",
                "error": None,
            }
        
        stage_info = self.metadata["stages"][stage_name]
        
        if status == "in_progress" and not stage_info["start_time"]:
            stage_info["start_time"] = datetime.now().isoformat()
            stage_info["executed"] = True
        elif status == "completed" or status == "failed":
            stage_info["end_time"] = datetime.now().isoformat()
            if stage_info["start_time"]:
                start = datetime.fromisoformat(stage_info["start_time"])
                end = datetime.fromisoformat(stage_info["end_time"])
                stage_info["duration_seconds"] = int((end - start).total_seconds())
        
        stage_info["status"] = status
        
        if output_file:
            stage_info["output_file"] = output_file
        
        if error:
            stage_info["error"] = error
            self.metadata["error_history"].append({
                "stage": stage_name,
                "error": error,
                "timestamp": datetime.now().isoformat(),
                "retry_count": self.metadata["execution"]["retry_count"],
            })
        
        # 更新阶段特定信息
        for key, value in kwargs.items():
            if key in stage_info:
                stage_info[key] = value
        
        self.metadata["execution"]["current_stage"] = stage_name
        self.save()

    def increment_retry(self):
        """增加重试计数"""
        self.metadata["execution"]["retry_count"] += 1
        self.save()

    def record_confirmation(self, confirmation_type: str):
        """
        记录用户确认

        Args:
            confirmation_type: 确认类型 (seo_title|preview|publish)
        """
        key = f"{confirmation_type}_confirmed"
        if key in self.metadata["confirmations"]:
            self.metadata["confirmations"][key] = True
            self.metadata["confirmations"][f"{confirmation_type}_confirmed_at"] = datetime.now().isoformat()
            self.save()

    def complete_pipeline(self, success: bool = True, notes: str = ""):
        """
        完成流水线

        Args:
            success: 是否成功
            notes: 备注信息
        """
        self.metadata["execution"]["status"] = "completed" if success else "failed"
        self.metadata["summary"]["success"] = success
        self.metadata["summary"]["final_status"] = "completed" if success else "failed"
        self.metadata["summary"]["notes"] = notes
        
        # 计算统计数据
        stages_completed = sum(1 for s in self.metadata["stages"].values() if s["status"] == "completed")
        self.metadata["summary"]["stages_completed"] = stages_completed
        self.metadata["summary"]["completion_percentage"] = int(stages_completed / 8 * 100)
        
        self.save()

    def get_status(self) -> Dict:
        """获取当前流水线状态"""
        return {
            "pipeline_id": self.pipeline_id,
            "current_stage": self.metadata["execution"]["current_stage"],
            "status": self.metadata["execution"]["status"],
            "article_title": self.metadata["article"]["title"],
            "completion_percentage": self.metadata["summary"]["completion_percentage"],
            "stages_completed": self.metadata["summary"]["stages_completed"],
        }

    @staticmethod
    def list_pipelines(limit: int = 10) -> List[Dict]:
        """
        列出最近的流水线执行

        Args:
            limit: 返回的最大条数

        Returns:
            流水线列表
        """
        pipelines = []
        if not os.path.exists(METADATA_DIR):
            return pipelines
        
        files = sorted(
            os.listdir(METADATA_DIR),
            reverse=True
        )[:limit]
        
        for filename in files:
            filepath = os.path.join(METADATA_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    pipelines.append({
                        "pipeline_id": data.get("pipeline_id"),
                        "start_time": data.get("start_time"),
                        "status": data.get("execution", {}).get("status"),
                        "article_title": data.get("article", {}).get("title"),
                    })
            except Exception:
                continue
        
        return pipelines


if __name__ == "__main__":
    print("Pipeline Manager for article-workflow")
    print(f"  Metadata directory: {METADATA_DIR}")
    print()
    
    # 示例：创建新流水线
    pm = PipelineManager()
    print(f"  Created pipeline: {pm.pipeline_id}")
    print(f"  Metadata file: {pm.metadata_file}")
    print()
    
    # 列出最近的流水线
    pipelines = PipelineManager.list_pipelines(5)
    print(f"  Recent pipelines ({len(pipelines)}):")
    for p in pipelines:
        print(f"    - {p['pipeline_id']}: {p['status']}")
