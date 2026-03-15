#!/bin/bash
# article-workflow 快速开始脚本

set -e  # 遇到错误立即退出

echo "🚀 article-workflow 快速开始"
echo "================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# 检查是否在插件目录
check_plugin_dir() {
    if [ ! -f "README.md" ] || [ ! -d "skills" ]; then
        print_error "请确保在 article-workflow 插件目录下运行此脚本"
        echo "当前目录: $(pwd)"
        echo "预期目录应包含: README.md 和 skills/ 目录"
        exit 1
    fi
    print_success "目录检查通过"
}

# 检查 Python 环境
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "未找到 Python，请先安装 Python 3.8+"
        exit 1
    fi
    
    # 检查 Python 版本
    PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if [ $(echo "$PYTHON_VERSION < 3.8" | bc) -eq 1 ]; then
        print_error "需要 Python 3.8+，当前版本: $PYTHON_VERSION"
        exit 1
    fi
    
    print_success "Python 版本: $PYTHON_VERSION"
    echo "Python 命令: $PYTHON_CMD"
}

# 检查 pip
check_pip() {
    if $PYTHON_CMD -m pip --version &> /dev/null; then
        print_success "pip 已安装"
    else
        print_warning "pip 未安装，尝试安装..."
        if [ "$(uname)" == "Darwin" ]; then
            # macOS
            brew install python3
        elif [ -f /etc/debian_version ]; then
            # Debian/Ubuntu
            sudo apt-get update
            sudo apt-get install python3-pip -y
        elif [ -f /etc/redhat-release ]; then
            # CentOS/RHEL
            sudo yum install python3-pip -y
        else
            print_error "无法自动安装 pip，请手动安装"
            exit 1
        fi
    fi
}

# 安装依赖
install_dependencies() {
    print_info "安装 Python 依赖..."
    
    # 检查并安装 article-generator 依赖
    if [ -f "skills/article-generator/requirements.txt" ]; then
        print_info "安装文章生成依赖..."
        $PYTHON_CMD -m pip install -r skills/article-generator/requirements.txt
        print_success "文章生成依赖安装完成"
    else
        print_warning "未找到 article-generator 依赖文件"
    fi
    
    # 检查并安装 wechat-article-converter 依赖
    if [ -f "skills/wechat-article-converter/requirements.txt" ]; then
        print_info "安装微信格式转换依赖..."
        $PYTHON_CMD -m pip install -r skills/wechat-article-converter/requirements.txt
        print_success "微信格式转换依赖安装完成"
    else
        print_warning "未找到 wechat-article-converter 依赖文件"
    fi
    
    # 安装共享模块依赖
    print_info "安装共享模块依赖..."
    $PYTHON_CMD -m pip install pyyaml colorama
    print_success "共享模块依赖安装完成"
}

# 配置插件
setup_config() {
    print_info "配置插件..."
    
    # 检查配置文件
    if [ -f "config/config.json" ]; then
        print_warning "配置文件已存在，跳过配置向导"
        echo "如需重新配置，请运行: $PYTHON_CMD scripts/config_wizard.py"
    else
        print_info "运行配置向导..."
        if [ -f "scripts/config_wizard.py" ]; then
            $PYTHON_CMD scripts/config_wizard.py
        else
            print_warning "配置向导未找到，手动创建配置文件..."
            cp config/config.example.json config/config.json
            print_success "配置文件已创建，请编辑 config/config.json"
        fi
    fi
}

# 测试安装
test_installation() {
    print_info "测试安装..."
    
    # 测试 Python 模块导入
    if $PYTHON_CMD -c "import yaml, json, colorama" &> /dev/null; then
        print_success "Python 模块导入测试通过"
    else
        print_error "Python 模块导入失败"
        exit 1
    fi
    
    # 测试 CLI 工具
    if [ -f "scripts/pipeline_cli.py" ]; then
        if $PYTHON_CMD scripts/pipeline_cli.py --help &> /dev/null; then
            print_success "CLI 工具测试通过"
        else
            print_warning "CLI 工具测试失败（可能缺少依赖）"
        fi
    fi
    
    # 测试配置向导
    if [ -f "scripts/config_wizard.py" ]; then
        if $PYTHON_CMD scripts/config_wizard.py --help &> /dev/null; then
            print_success "配置向导测试通过"
        else
            print_warning "配置向导测试失败"
        fi
    fi
}

# 创建输出目录
create_output_dirs() {
    print_info "创建输出目录..."
    
    mkdir -p output/{drafts,published,reviews,wechat,analytics,images}
    print_success "输出目录结构创建完成"
    
    echo "输出目录结构:"
    tree output/ --dirsfirst -L 2 2>/dev/null || find output/ -type d | sed 's|[^/]*/|- |g'
}

# 显示使用说明
show_usage() {
    echo ""
    echo "🎉 安装完成！"
    echo "================================"
    echo ""
    echo "接下来你可以："
    echo ""
    echo "1. 📝 写一篇文章"
    echo "   在 Claude Code 中输入："
    echo "   请帮我写一篇关于 [主题] 的技术文章"
    echo ""
    echo "2. 🔍 审查文章质量"
    echo "   审查文章 output/你的文章.md"
    echo ""
    echo "3. 🚀 运行完整流水线"
    echo "   $PYTHON_CMD scripts/pipeline_cli.py run"
    echo ""
    echo "4. ⚙️  管理配置"
    echo "   $PYTHON_CMD scripts/config_wizard.py"
    echo ""
    echo "5. 🧪 运行测试"
    echo "   $PYTHON_CMD scripts/pipeline_cli.py test"
    echo ""
    echo "6. 📖 查看详细示例"
    echo "   查看 EXAMPLES.md 文件获取更多使用示例"
    echo ""
    echo "7. 🆘 获取帮助"
    echo "   $PYTHON_CMD scripts/pipeline_cli.py --help"
    echo ""
    echo "配置文件位置:"
    echo "  - 插件配置: config/config.json"
    echo "  - 环境变量: 支持 GEMINI_API_KEY, WECHAT_APPID 等"
    echo "  - Claude 环境: ~/.claude/env.json"
    echo ""
    echo "输出目录:"
    echo "  - 文章文件: output/drafts/, output/published/"
    echo "  - 审查报告: output/reviews/"
    echo "  - 微信格式: output/wechat/"
    echo "  - 分析报告: output/analytics/"
    echo ""
    echo "常见问题请参考 README.md 中的 FAQ 部分"
    echo ""
}

# 主函数
main() {
    echo ""
    print_info "开始 article-workflow 快速安装"
    echo ""
    
    # 执行各个步骤
    check_plugin_dir
    check_python
    check_pip
    install_dependencies
    setup_config
    create_output_dirs
    test_installation
    show_usage
}

# 运行主函数
main "$@"