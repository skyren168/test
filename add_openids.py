#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
openid批量添加工具
"""

import os
import sys

def add_openids(openids_list):
    """批量添加openid到文件"""
    filename = 'user_openids.txt'
    
    # 读取现有openid
    existing_openids = set()
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    existing_openids.add(line)
    
    # 添加新openid
    new_count = 0
    with open(filename, 'a', encoding='utf-8') as f:
        for openid in openids_list:
            openid = openid.strip()
            if openid and openid not in existing_openids:
                f.write(openid + '\n')
                new_count += 1
                print(f"✅ 添加openid: {openid}")
    
    print(f"\n📊 统计: 新增 {new_count} 个openid，总计 {len(existing_openids) + new_count} 个用户")

def main():
    print("🚀 openid批量添加工具")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # 从命令行参数添加
        openids = sys.argv[1:]
        add_openids(openids)
    else:
        # 交互式添加
        print("请输入openid（每行一个，空行结束）:")
        openids = []
        while True:
            openid = input().strip()
            if not openid:
                break
            openids.append(openid)
        
        if openids:
            add_openids(openids)
        else:
            print("❌ 未输入任何openid")

if __name__ == "__main__":
    main()