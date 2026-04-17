#!/usr/bin/env python3
"""
SciPlot Academic 测试运行脚本

提供便捷的测试运行方式，支持多种测试场景。
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(cmd, description):
    """运行命令并输出结果"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    print(f"命令: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="运行 SciPlot Academic 测试套件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run_tests.py                    # 运行所有测试
  python run_tests.py --unit             # 仅运行单元测试
  python run_tests.py --integration      # 仅运行集成测试
  python run_tests.py --regression       # 仅运行回归测试
  python run_tests.py --cov              # 带覆盖率报告
  python run_tests.py --quick            # 快速测试（排除慢测试）
  python run_tests.py --verbose          # 详细输出
        """
    )
    
    parser.add_argument(
        "--unit", "-u",
        action="store_true",
        help="仅运行单元测试"
    )
    parser.add_argument(
        "--integration", "-i",
        action="store_true",
        help="仅运行集成测试"
    )
    parser.add_argument(
        "--regression", "-r",
        action="store_true",
        help="仅运行回归测试"
    )
    parser.add_argument(
        "--cov", "-c",
        action="store_true",
        help="生成覆盖率报告"
    )
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="快速模式（排除慢测试）"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细输出"
    )
    parser.add_argument(
        "--failfast", "-f",
        action="store_true",
        help="遇到第一个失败就停止"
    )
    
    args = parser.parse_args()
    
    # 构建 pytest 命令
    cmd = [sys.executable, "-m", "pytest"]
    
    # 测试选择
    if args.unit:
        cmd.append("tests/unit/")
    elif args.integration:
        cmd.append("tests/integration/")
    elif args.regression:
        cmd.append("tests/regression/")
    else:
        cmd.append("tests/")
    
    # 选项
    if args.verbose:
        cmd.append("-v")
    
    if args.failfast:
        cmd.append("-x")
    
    if args.quick:
        cmd.append("-m")
        cmd.append("not slow")
    
    if args.cov:
        cmd.append("--cov=sciplot")
        cmd.append("--cov-report=term-missing")
        cmd.append("--cov-report=html:htmlcov")
    
    # 运行测试
    exit_code = run_command(cmd, "运行测试")
    
    # 输出总结
    print(f"\n{'='*60}")
    if exit_code == 0:
        print("✅ 所有测试通过！")
    else:
        print(f"❌ 测试失败（退出码: {exit_code}）")
    print(f"{'='*60}\n")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
