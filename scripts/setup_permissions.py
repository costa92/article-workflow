#!/usr/bin/env python3
"""
设置脚本权限
"""

import os
import stat

def set_executable_permissions():
    """设置脚本执行权限"""
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    
    scripts_to_make_executable = [
        "quick_start.sh",
        "config_wizard.py",
        "pipeline_cli.py"
    ]
    
    for script_name in scripts_to_make_executable:
        script_path = os.path.join(scripts_dir, script_name)
        if os.path.exists(script_path):
            try:
                # 添加执行权限
                current_permissions = os.stat(script_path).st_mode
                os.chmod(script_path, current_permissions | stat.S_IEXEC)
                print(f"✅ 设置执行权限: {script_name}")
            except Exception as e:
                print(f"⚠️  无法设置 {script_name} 权限: {e}")
        else:
            print(f"⚠️  文件不存在: {script_name}")

if __name__ == "__main__":
    print("🔧 设置脚本执行权限")
    set_executable_permissions()
    print("🎉 权限设置完成")
    print("\n现在可以运行:")
    print("  ./scripts/quick_start.sh")
    print("  或")
    print("  python scripts/quick_start.sh")