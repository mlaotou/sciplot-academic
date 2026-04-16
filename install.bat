@echo off
chcp 65001 >nul
echo ==========================================
echo SciPlot 安装脚本
echo ==========================================
echo.
echo 正在检查 uv 是否可用...

where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未找到 uv 命令
    echo 请先安装 uv: https://github.com/astral-sh/uv
    pause
    exit /b 1
)

echo [OK] uv 已找到
echo.
echo 安装方式选择:
echo   1. 开发模式安装 (推荐) - 修改代码即时生效
echo   2. 普通安装 - 安装后修改需重新安装
echo.
set /p choice="请选择 (1/2): "

if "%choice%"=="1" (
    echo.
    echo 正在以开发模式安装 sciplot...
    uv pip install -e .
) else if "%choice%"=="2" (
    echo.
    echo 正在安装 sciplot...
    uv pip install .
) else (
    echo 无效选择，默认使用开发模式安装...
    uv pip install -e .
)

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo [成功] SciPlot 安装完成！
    echo ==========================================
    echo.
    echo 现在你可以在任何项目中使用:
    echo   import sciplot as sp
    echo.
    echo 测试安装:
    echo   python -c "import sciplot; print(sciplot.__version__)"
) else (
    echo.
    echo [错误] 安装失败，请检查错误信息
)

pause
