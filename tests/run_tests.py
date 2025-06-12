#!/usr/bin/env python3
"""
ReadingTypeID Agent测试运行脚本
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_tests():
    """运行测试的主函数"""
    parser = argparse.ArgumentParser(description="运行ReadingTypeID Agent测试")
    parser.add_argument("--type", choices=["unit", "integration", "all"], 
                       default="all", help="测试类型")
    parser.add_argument("--coverage", action="store_true", help="生成覆盖率报告")
    
    args = parser.parse_args()
    
    # 切换到项目根目录
    script_dir = Path(__file__).parent
    os.chdir(script_dir.parent)
    
    print(f"运行 {args.type} 测试...")
    
    # 构建pytest命令
    cmd = ["python", "-m", "pytest", "-v"]
    
    if args.type == "unit":
        cmd.append("tests/unit/")
    elif args.type == "integration":
        cmd.append("tests/integration/")
    else:
        cmd.append("tests/")
    
    if args.coverage:
        cmd.extend(["--cov=reading_type_agent", "--cov-report=html"])
    
    # 运行测试
    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code) 