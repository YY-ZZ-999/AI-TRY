# -*- coding: utf-8 -*-
import pandas as pd

# 读取CSV文件（GBK编码）
df = pd.read_csv(r'C:\Users\HONOR\Desktop\项目数据\kprototypes_input.csv', encoding='gbk')

print("=== 数据基本信息 ===")
print(f"数据量: {len(df)} 行, {len(df.columns)} 列")
print("\n=== 列名 ===")
print(df.columns.tolist())
print("\n=== 前5行数据 ===")
print(df.head())
print("\n=== 数据类型 ===")
print(df.dtypes)
