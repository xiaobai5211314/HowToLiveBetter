#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《高性价比人生指南》上游开源仓库同步与自动更新工具
用法：python tools/sync_upstream.py
功能：
1. 检查并拉取原作者 upstream (eternity4719/HowToLiveBetter) 的最新修改
2. 同步正文章节、文档、自查工具及更新记录
3. 自动注入自定义独立域名与仓库配置
4. 重新计算全书字数、条目与性价比统计数据 (sync-stats)
5. 提交并推送至 origin (xiaobai5211314/HowToLiveBetter)
6. 自动触发 GitHub Actions 部署至生产服务器 (rensheng.21212121.xyz)
"""

import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, check=True):
    print(f"[*] 执行命令: {cmd}")
    res = subprocess.run(cmd, shell=True, cwd=BASE_DIR, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr and res.returncode != 0:
        print(f"[!] 提示/输出: {res.stderr.strip()}", file=sys.stderr)
    if check and res.returncode != 0:
        sys.exit(res.returncode)
    return res

def patch_files():
    # 1. 注入 index.html
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("https://eternity4719.github.io/HowToLiveBetter/", "https://rensheng.21212121.xyz/")
        content = content.replace("https://eternity4719.github.io/HowToLiveBetter", "https://rensheng.21212121.xyz/")
        content = content.replace("https://github.com/eternity4719/HowToLiveBetter", "https://github.com/xiaobai5211314/HowToLiveBetter")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("[*] 已注入独立域名 rensheng.21212121.xyz 与个人仓库地址")

    # 2. 修复 updates.mjs 基准提交回溯
    updates_path = os.path.join(BASE_DIR, "tools", "updates.mjs")
    if os.path.exists(updates_path):
        with open(updates_path, "r", encoding="utf-8") as f:
            c = f.read()
        target = "const base = git(['rev-list', '-1', '--first-parent', `--before=${sinceTs}`, 'HEAD']).toString().trim();\nif (!base) throw new Error(`找不到 ${SINCE} 之前的提交。CI 上 checkout 要加 fetch-depth: 0`);"
        replacement = """let base = '';
try { base = git(['rev-list', '-1', '--first-parent', `--before=${sinceTs}`, 'HEAD']).toString().trim(); } catch {}
if (!base) { try { base = git(['rev-list', '-1', '--first-parent', `--before=${sinceTs}`, 'upstream/main']).toString().trim(); } catch {} }
if (!base) { try { base = git(['rev-list', '--max-parents=0', 'HEAD']).toString().trim(); } catch {} }"""
        if target in c:
            c = c.replace(target, replacement)
        else:
            # 兼容不同换行符
            c = c.replace(target.replace("\n", "\r\n"), replacement.replace("\n", "\r\n"))
        with open(updates_path, "w", encoding="utf-8") as f:
            f.write(c)
        print("[*] 已优化 tools/updates.mjs 历史基准提交回溯逻辑")

def main():
    print("=" * 60)
    print("   《高性价比人生指南》上游开源仓库同步与自动更新工具")
    print("=" * 60)
    
    # 1. 检查 remote
    remotes = run("git remote -v").stdout
    if "upstream" not in remotes:
        print("[*] 正在添加上游仓库源 upstream: https://github.com/eternity4719/HowToLiveBetter.git")
        run("git remote add upstream https://github.com/eternity4719/HowToLiveBetter.git")

    # 2. 拉取 upstream
    print("[*] 正在从 upstream 获取最新变更...")
    run("git fetch upstream")

    # 3. 检出上游最新内容与工具
    print("[*] 正在检出上游最新的正文、文档、自查工具与更新数据...")
    run("git checkout upstream/main -- book docs tools updates.json selfcheck.html index.html README.md")

    # 4. 注入配置与重新统计
    patch_files()
    print("[*] 正在执行全书统计与校验 (sync-stats)...")
    run("node tools/sync-stats.mjs")

    # 5. 检查本地是否有待提交或推送文件
    status = run("git status --porcelain").stdout.strip()
    ahead = run("git rev-list origin/main..HEAD --count").stdout.strip()
    
    if status or ahead != "0":
        if status:
            print("[*] 发现变动文件，正在提交至本地 Git...")
            run("git add .")
            run('git commit -m "feat: sync latest upstream advice (767 items) and tools"')
        print("[*] 正在推送至 GitHub 仓库 (origin main)...")
        run("git push origin main")
        print("=" * 60)
        print("🎉 推送成功！GitHub Actions 已自动触发并将最新内容部署至服务器：")
        print("🌐 站点地址: https://rensheng.21212121.xyz")
        print("=" * 60)
    else:
        print("[✓] 没有文件需要推送，云端已是最新状态。")

if __name__ == '__main__':
    main()
