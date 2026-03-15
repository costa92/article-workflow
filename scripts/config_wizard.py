#!/usr/bin/env python3
"""
Configuration Wizard for article-workflow

交互式配置向导，帮助用户快速设置插件配置
"""

import os
import sys
import json
import shutil
from pathlib import Path

# 获取插件根目录
PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(PLUGIN_ROOT, "config")
CONFIG_EXAMPLE = os.path.join(CONFIG_DIR, "config.example.json")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# 颜色定义
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    """打印标题"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_success(text):
    """打印成功消息"""
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")


def print_warning(text):
    """打印警告消息"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")


def print_error(text):
    """打印错误消息"""
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")


def print_step(text):
    """打印步骤信息"""
    print(f"{Colors.CYAN}📝 {text}{Colors.ENDC}")


def get_input(prompt, default=None, required=False):
    """
    获取用户输入
    
    Args:
        prompt: 提示信息
        default: 默认值
        required: 是否必须输入
        
    Returns:
        用户输入的值
    """
    while True:
        if default:
            display_prompt = f"{prompt} [{default}]: "
        else:
            display_prompt = f"{prompt}: "
        
        value = input(display_prompt).strip()
        
        if not value and default:
            return default
        elif not value and required:
            print_error("此项为必填项，请重新输入")
        else:
            return value


def get_yes_no(prompt, default=True):
    """
    获取是/否选择
    
    Args:
        prompt: 提示信息
        default: 默认值
        
    Returns:
        True/False
    """
    default_text = "Y/n" if default else "y/N"
    while True:
        response = input(f"{prompt} [{default_text}]: ").strip().lower()
        
        if not response:
            return default
        elif response in ["y", "yes", "是"]:
            return True
        elif response in ["n", "no", "否"]:
            return False
        else:
            print_error("请输入 y/n 或 是/否")


def get_choice(prompt, options, default=None):
    """
    获取选择
    
    Args:
        prompt: 提示信息
        options: 选项列表 [(key, description), ...]
        default: 默认选项的 key
        
    Returns:
        选择的 key
    """
    print(f"\n{prompt}:")
    for i, (key, desc) in enumerate(options, 1):
        print(f"  {i}. {desc}")
    
    while True:
        if default:
            default_idx = next(i for i, (k, _) in enumerate(options, 1) if k == default)
            choice = input(f"\n请选择 [1-{len(options)}] (默认 {default_idx}): ").strip()
        else:
            choice = input(f"\n请选择 [1-{len(options)}]: ").strip()
        
        if not choice and default:
            return default
        elif choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(options):
                return options[idx-1][0]
        
        print_error(f"请输入 1-{len(options)} 之间的数字")


def setup_gemini_api():
    """设置 Gemini API 配置"""
    print_header("Gemini API 配置")
    print("Gemini API 用于 AI 图片生成功能。")
    print("1. 访问 https://makersuite.google.com/app/apikey")
    print("2. 登录 Google 账号")
    print("3. 点击「Create API Key」创建新的 API 密钥")
    print("4. 复制生成的密钥\n")
    
    api_key = get_input("请输入 Gemini API 密钥", required=True)
    return {"gemini_api_key": api_key}


def setup_wechat_api():
    """设置微信公众号 API 配置"""
    print_header("微信公众号 API 配置")
    print("微信公众号 API 用于草稿箱上传功能。")
    print("获取方法：")
    print("1. 登录 https://mp.weixin.qq.com")
    print("2. 进入「设置与开发」→「基本配置」")
    print("3. 在「开发者ID」部分找到 AppID")
    print("4. 在「开发者密码」部分点击「重置」获取 AppSecret")
    print("5. 配置 IP 白名单（必须）\n")
    
    use_wechat = get_yes_no("是否配置微信公众号 API？", default=False)
    if not use_wechat:
        return {}
    
    appid = get_input("请输入微信公众号 AppID", required=True)
    secret = get_input("请输入微信公众号 AppSecret", required=True)
    
    print("\n📋 IP 白名单配置：")
    print("1. 登录 mp.weixin.qq.com → 设置与开发 → 基本配置")
    print("2. 找到「IP白名单」配置项，点击「配置」")
    print("3. 添加你的公网 IP 地址")
    print("4. 查看本机公网 IP 命令：curl ifconfig.me\n")
    
    get_yes_no("请确认已配置 IP 白名单（按回车继续）", default=True)
    
    return {
        "wechat_appid": appid,
        "wechat_secret": secret
    }


def setup_openai_api():
    """设置 OpenAI 兼容 API 配置"""
    print_header("OpenAI 兼容 API 配置")
    print("OpenAI 兼容 API 用于 Go 后端的图片生成功能（可选）。")
    print("支持的平台：DeepSeek、Moonshot、智谱 AI、OpenAI 等。\n")
    
    use_openai = get_yes_no("是否配置 OpenAI 兼容 API？", default=False)
    if not use_openai:
        return {}
    
    api_key = get_input("请输入 API 密钥", required=True)
    api_base = get_input("请输入 API 地址", default="https://api.openai.com/v1")
    
    return {
        "image_api_key": api_key,
        "image_api_base": api_base
    }


def setup_author_info():
    """设置作者信息"""
    print_header("作者信息配置")
    print("设置文章默认作者名。\n")
    
    author = get_input("请输入默认作者名", default="Anonymous")
    
    return {"default_author": author}


def setup_cdn_config():
    """设置 CDN 配置"""
    print_header("CDN 配置")
    print("CDN 用于图片加速（可选）。")
    print("如果使用 PicGo 上传到 GitHub 图床，可以配置 CDN 域名。\n")
    
    use_cdn = get_yes_no("是否配置 CDN？", default=False)
    if not use_cdn:
        return {}
    
    cdn_domain = get_input("请输入 CDN 域名", default="cdn.jsdelivr.net")
    
    return {"cdn_domain": cdn_domain}


def setup_github_images():
    """设置 GitHub 图床配置"""
    print_header("GitHub 图床配置")
    print("PicGo 图床配置，用于将图片上传到 GitHub 仓库。")
    print("1. 在 GitHub 上创建一个公开仓库（如 username/images）")
    print("2. 生成 GitHub Token：Settings → Developer settings → Personal access tokens → Tokens (classic)")
    print("3. 在 PicGo 中配置 GitHub 图床\n")
    
    use_github = get_yes_no("是否配置 GitHub 图床？", default=False)
    if not use_github:
        return {}
    
    repo = get_input("请输入 GitHub 仓库名（格式：username/repo）", required=True)
    
    return {"github_images_repo": repo}


def setup_obsidian_paths():
    """设置 Obsidian 路径配置"""
    print_header("Obsidian 路径配置")
    print("设置 Obsidian 笔记库中的目录路径（可选）。\n")
    
    use_obsidian = get_yes_no("是否使用 Obsidian 管理文章？", default=False)
    if not use_obsidian:
        return {}
    
    tech_dir = get_input("请输入技术文章存放目录", default="02-技术")
    publish_dir = get_input("请输入已发布文章存放目录", default="03-创作/已发布")
    
    return {
        "obsidian_tech_dir": tech_dir,
        "obsidian_publish_dir": publish_dir
    }


def create_config_file(config_data):
    """创建配置文件"""
    print_header("创建配置文件")
    
    # 确保配置目录存在
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    # 检查是否已存在配置文件
    if os.path.exists(CONFIG_FILE):
        backup_file = f"{CONFIG_FILE}.backup"
        shutil.copy2(CONFIG_FILE, backup_file)
        print_warning(f"已备份现有配置文件到: {backup_file}")
    
    # 写入配置文件
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)
    
    print_success(f"配置文件已创建: {CONFIG_FILE}")
    
    # 显示配置内容
    print("\n📋 配置内容：")
    for key, value in config_data.items():
        display_value = value
        if "key" in key.lower() or "secret" in key.lower():
            display_value = value[:4] + "****" + value[-4:] if len(value) > 8 else "****"
        print(f"  {key}: {display_value}")
    
    return True


def show_environment_vars(config_data):
    """显示环境变量设置方法"""
    print_header("环境变量设置方法")
    
    print("如果不想使用配置文件，也可以设置环境变量：\n")
    
    env_map = {
        "gemini_api_key": "GEMINI_API_KEY",
        "wechat_appid": "WECHAT_APPID",
        "wechat_secret": "WECHAT_SECRET",
        "image_api_key": "IMAGE_API_KEY",
        "image_api_base": "IMAGE_API_BASE",
        "default_author": "ARTICLE_AUTHOR",
        "cdn_domain": "CDN_DOMAIN",
        "github_images_repo": "GITHUB_IMAGES_REPO",
        "obsidian_tech_dir": "OBSIDIAN_TECH_DIR",
        "obsidian_publish_dir": "OBSIDIAN_PUBLISH_DIR",
    }
    
    for config_key, env_var in env_map.items():
        if config_key in config_data and config_data[config_key]:
            print(f"export {env_var}=\"{config_data[config_key]}\"")
    
    print("\n💡 可以将以上命令添加到 ~/.zshrc 或 ~/.bashrc 中永久生效")
    print("   然后运行: source ~/.zshrc")


def show_next_steps():
    """显示后续步骤"""
    print_header("配置完成！")
    
    print("🎉 恭喜！article-workflow 插件已配置完成。\n")
    
    print("下一步：")
    print("1. 安装 Python 依赖：")
    print("   pip install -r skills/article-generator/requirements.txt")
    print("   pip install -r skills/wechat-article-converter/requirements.txt")
    print()
    print("2. 测试功能：")
    print("   - 写一篇文章: 请帮我写一篇关于 RAG 优化技巧的技术文章")
    print("   - 审查文章: 审查文章 output/article.md")
    print("   - 转微信格式: 把文章转成微信格式，用 coffee 主题")
    print()
    print("3. 端到端流水线：")
    print("   帮我完成一篇关于 Claude Code 的文章，从写作到发布微信公众号")
    print()
    print("💡 更多信息请查看 README.md")


def main():
    """主函数"""
    print_header("article-workflow 配置向导")
    print("欢迎使用 article-workflow 插件配置向导！")
    print("本向导将帮助你快速完成插件配置。\n")
    
    # 收集配置信息
    config_data = {}
    
    # 1. Gemini API 配置（必填）
    config_data.update(setup_gemini_api())
    
    # 2. 微信公众号 API 配置（可选）
    config_data.update(setup_wechat_api())
    
    # 3. OpenAI 兼容 API 配置（可选）
    config_data.update(setup_openai_api())
    
    # 4. 作者信息配置
    config_data.update(setup_author_info())
    
    # 5. CDN 配置（可选）
    config_data.update(setup_cdn_config())
    
    # 6. GitHub 图床配置（可选）
    config_data.update(setup_github_images())
    
    # 7. Obsidian 路径配置（可选）
    config_data.update(setup_obsidian_paths())
    
    # 创建配置文件
    if create_config_file(config_data):
        # 显示环境变量设置方法
        show_environment_vars(config_data)
        
        # 显示后续步骤
        show_next_steps()
        
        return True
    else:
        print_error("配置文件创建失败")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  配置向导被用户中断")
        sys.exit(1)
    except Exception as e:
        print_error(f"配置向导运行出错: {e}")
        sys.exit(1)
