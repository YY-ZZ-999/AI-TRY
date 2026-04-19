# -*- coding: utf-8 -*-
import pandas as pd

# 读取数据
df = pd.read_csv(r'C:\Users\HONOR\Desktop\项目数据\kprototypes_input.csv', encoding='gbk')

# 清理数据 - 删除空列
df = df.drop(columns=['Unnamed: 12', 'Unnamed: 13'], errors='ignore')

# 统计各维度的分布
stats = {}

# 性别分布
stats['gender'] = df['性别'].value_counts().to_dict()

# 内容偏好
stats['content_pref'] = df['内容偏好'].value_counts().to_dict()

# 垂类分布 (取前10)
stats['category'] = df['垂类'].value_counts().head(10).to_dict()

# 垂类聚合
stats['category_agg'] = df['垂类聚合'].value_counts().to_dict()

# 年龄分布
stats['age'] = df['年龄'].value_counts().to_dict()

# 操作系统
stats['os'] = df['操作系统'].value_counts().to_dict()

# 城市线
stats['city_level'] = df['城市线'].value_counts().to_dict()

# 消费水平
stats['consumption'] = df['消费水平'].value_counts().to_dict()

# 数值统计
stats['numerical'] = {
    'all_dura': {
        'mean': float(df['all_dura'].mean()),
        'median': float(df['all_dura'].median()),
        'std': float(df['all_dura'].std()),
        'min': float(df['all_dura'].min()),
        'max': float(df['all_dura'].max())
    },
    'ctr_rate': {
        'mean': float(df['ctr_rate'].mean()),
        'median': float(df['ctr_rate'].median()),
        'std': float(df['ctr_rate'].std())
    },
    'interaction_rate': {
        'mean': float(df['interaction_rate'].mean()),
        'median': float(df['interaction_rate'].median()),
        'std': float(df['interaction_rate'].std())
    }
}

# 性别与各指标的关系
gender_stats = df.groupby('性别').agg({
    'all_dura': 'mean',
    'ctr_rate': 'mean',
    'interaction_rate': 'mean'
}).to_dict()

stats['gender_metrics'] = gender_stats

# 内容偏好与指标关系
content_stats = df.groupby('内容偏好').agg({
    'all_dura': 'mean',
    'ctr_rate': 'mean',
    'interaction_rate': 'mean'
}).to_dict()

stats['content_metrics'] = content_stats

# 操作系统与指标关系
os_stats = df.groupby('操作系统').agg({
    'all_dura': 'mean',
    'ctr_rate': 'mean',
    'interaction_rate': 'mean'
}).to_dict()

stats['os_metrics'] = os_stats

# 保存统计数据为JSON
import json
with open(r'C:\Users\HONOR\Documents\trae_projects\AI-TRY1\dashboard\stats.json', 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

print("统计数据已保存!")
print(f"总用户数: {len(df)}")
