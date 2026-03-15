# 迁移指南

本文档将指导您从旧版本迁移到 article-workflow v2.0。

## 从 v1.x 迁移到 v2.0

### 🚨 重大变更

#### 1. 配置结构变更
**v1.x 配置文件**：
```json
{
  "gemini_api_key": "your-key",
  "wechat_appid": "your-appid",
  "wechat_secret": "your-secret",
  "default_author": "Your Name"
}
```

**v2.0 配置文件**：
```json
{
  "gemini_api_key": "your-key",
  "wechat_appid": "your-appid",
  "wechat_secret": "your-secret",
  "default_author": "Your Name",
  
  "article_generation": {
    "default_word_count": 1500,
    "auto_generate_images": true
  },
  
  "pipeline_settings": {
    "max_review_retries": 3,
    "max_error_retries": 2
  }
}
```

#### 2. 新增依赖
v2.0 需要新增 Python 依赖：
- `pyyaml`: YAML 配置文件支持
- `colorama`: 终端颜色输出

#### 3. 数据目录结构变更
新增流水线元数据目录：
```
config/
├── config.json
└── pipeline_metadata/     # 新增目录
    ├── 2025-03-15-001.yaml
    └── 2025-03-15-002.yaml
```

### 🛠️ 迁移步骤

#### 步骤 1：备份现有数据
```bash
# 备份配置文件
cp ~/.claude/plugins/article-workflow/config/config.json config_backup.json

# 备份输出目录
cp -r output/ output_backup/
```

#### 步骤 2：更新插件
```bash
# 重新安装插件
/plugin uninstall article-workflow
/plugin install article-workflow@article-workflow-marketplace
```

#### 步骤 3：安装新增依赖
```bash
pip install pyyaml colorama
```

#### 步骤 4：迁移配置文件
使用配置向导自动迁移：
```bash
python scripts/config_wizard.py --migrate config_backup.json
```

或手动编辑新配置文件。

#### 步骤 5：测试迁移结果
```bash
# 运行测试
python scripts/pipeline_cli.py test

# 创建测试流水线
python scripts/pipeline_cli.py create --topic "迁移测试"
python scripts/pipeline_cli.py run
```

### 🆕 新功能使用指南

#### 1. CLI 工具使用
```bash
# 查看所有命令
python scripts/pipeline_cli.py --help

# 创建和管理流水线
python scripts/pipeline_cli.py create --topic "文章主题"
python scripts/pipeline_cli.py list
python scripts/pipeline_cli.py show <pipeline_id>

# 监控和清理
python scripts/pipeline_cli.py stats
python scripts/pipeline_cli.py cleanup --keep 10
```

#### 2. 配置向导使用
```bash
# 交互式配置
python scripts/config_wizard.py

# 验证配置
python scripts/config_wizard.py --validate

# 导出配置
python scripts/config_wizard.py --export my_config.json
```

#### 3. 快速开始脚本
```bash
# 一键安装和配置
./scripts/quick_start.sh
```

### 🔧 故障排除

#### 问题 1：导入旧配置失败
**解决方案**：
```bash
# 手动创建新配置
cp config/config.example.json config/config.json

# 编辑配置文件，复制旧配置项
# 然后使用配置向导验证
python scripts/config_wizard.py --validate
```

#### 问题 2：依赖安装失败
**解决方案**：
```bash
# 单独安装依赖
pip install --upgrade pip
pip install pyyaml colorama --user

# 或使用系统包管理器
# Ubuntu/Debian
sudo apt-get install python3-pyyaml

# macOS
brew install pyyaml
```

#### 问题 3：权限问题
**解决方案**：
```bash
# 设置脚本权限
python scripts/setup_permissions.py

# 或手动设置
chmod +x scripts/*.sh
chmod +x scripts/*.py
```

### 📊 性能优化建议

#### 1. 配置优化
```json
{
  "pipeline_settings": {
    "auto_cleanup_days": 7,     // 减少数据保留时间
    "parallel_execution": false // 关闭并行执行（如内存不足）
  }
}
```

#### 2. 内存优化
```bash
# 限制并发任务
export ARTICLE_WORKFLOW_MAX_WORKERS=2

# 减少日志级别
export ARTICLE_WORKFLOW_LOG_LEVEL=WARNING
```

### 🔄 回滚指南

如果需要回滚到旧版本：

#### 步骤 1：备份 v2.0 数据
```bash
# 备份配置文件
cp config/config.json config_v2_backup.json

# 备份流水线数据
cp -r config/pipeline_metadata/ pipeline_metadata_backup/
```

#### 步骤 2：安装旧版本
```bash
# 指定版本安装
/plugin install article-workflow@v1.2.0
```

#### 步骤 3：恢复配置
```bash
# 恢复旧配置
cp config_v1_backup.json config/config.json
```

### 📚 学习资源

#### 新功能教程
1. **CLI 工具教程**：查看 `EXAMPLES.md` 中的 CLI 使用示例
2. **配置向导教程**：运行 `python scripts/config_wizard.py --help`
3. **错误处理指南**：查看 `agents/content-pipeline.md`

#### 最佳实践
1. **定期清理**：使用 `python scripts/pipeline_cli.py cleanup`
2. **监控状态**：使用 `python scripts/pipeline_cli.py list --watch`
3. **导出数据**：定期导出重要流水线数据

### 🤝 获取帮助

- **GitHub Issues**：报告迁移问题
- **文档**：查看 `EXAMPLES.md` 和 `README.md`
- **测试工具**：使用 `python scripts/pipeline_cli.py test`

## 总结

v2.0 版本带来了显著的改进和新功能，虽然迁移需要一些步骤，但新版本提供了更好的稳定性、性能和用户体验。按照本指南的步骤操作，您可以顺利完成迁移并开始享受新功能带来的便利。