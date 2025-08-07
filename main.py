#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESG评分系统主启动文件

基于甲模型设计理念的企业ESG评分系统
包含完整的数据预处理、权重分配、因子计算和非线性调整功能

使用方法:
    python main.py

作者: ESG评分系统
版本: 1.0.0
"""

import sys
import os
import warnings

warnings.filterwarnings("ignore")

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gradio_app import ESGGradioApp
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已安装所有依赖包:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def main():
    """
    主函数：启动ESG评分系统
    """
    print("=" * 60)
    print("🌱 ESG评分系统启动中...")
    print("=" * 60)
    print()
    print("系统特点:")
    print("📊 多维度ESG指标评估")
    print("🔄 智能数据预处理")
    print("⚖️ 组合赋权法（主观+客观权重）")
    print("📈 交叉项效应建模")
    print("🎯 非线性事件调整")
    print("📋 详细分析报告")
    print()
    print("基于甲模型设计理念，实现科学、透明、可操作的ESG评分")
    print()

    try:
        # 创建应用实例
        app = ESGGradioApp()

        # 创建界面
        interface = app.create_interface()

        print("🚀 系统启动成功！")
        print("📱 请在浏览器中访问: http://localhost:7860")
        print("⏹️  按 Ctrl+C 停止服务")
        print("=" * 60)

        # 启动界面（不使用队列以避免WebSocket连接问题）
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True,
            quiet=False,
            inbrowser=False,
            prevent_thread_lock=False,
        )

    except KeyboardInterrupt:
        print("\n👋 系统已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("\n请检查:")
        print("1. 是否已安装所有依赖包")
        print("2. 端口7860是否被占用")
        print("3. 网络连接是否正常")
        sys.exit(1)


if __name__ == "__main__":
    main()
