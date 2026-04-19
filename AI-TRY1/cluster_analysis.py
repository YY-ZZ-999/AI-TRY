# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
import json
import warnings
warnings.filterwarnings('ignore')

# 读取数据
print("正在读取数据...")
df = pd.read_csv(r'C:\Users\HONOR\Desktop\项目数据\kprototypes_input.csv', encoding='gbk')

# 清理数据
df = df.drop(columns=['Unnamed: 12', 'Unnamed: 13'], errors='ignore')

print(f"数据量: {len(df)} 行")

# 选择用于聚类的特征
cluster_features = ['性别', '内容偏好', '垂类聚合', '年龄', '操作系统', '城市线', '消费水平', 'all_dura', 'ctr_rate', 'interaction_rate']

# 准备数据
df_cluster = df[cluster_features].copy()

# 对类别变量进行编码
label_encoders = {}
categorical_cols = ['性别', '内容偏好', '垂类聚合', '年龄', '操作系统', '城市线', '消费水平']

for col in categorical_cols:
    le = LabelEncoder()
    df_cluster[col + '_encoded'] = le.fit_transform(df_cluster[col].astype(str))
    label_encoders[col] = le

# 数值特征标准化
numerical_cols = ['all_dura', 'ctr_rate', 'interaction_rate']
scaler = StandardScaler()
df_cluster[numerical_cols] = scaler.fit_transform(df_cluster[numerical_cols])

# 准备聚类特征矩阵
feature_cols = [col + '_encoded' for col in categorical_cols] + numerical_cols
X = df_cluster[feature_cols].values

# K-Means聚类 (尝试不同的k值)
print("\n正在尝试不同的聚类数...")
inertias = []
K_range = range(2, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)
    print(f"k={k}, inertia={kmeans.inertia_:.2f}")

# 使用k=6进行最终聚类
print("\n正在进行最终聚类 (k=6)...")
kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X)

# 分析每个簇的特征
print("\n" + "="*60)
print("各个人群特征分析")
print("="*60)

cluster_profiles = {}

for cluster_id in range(6):
    cluster_data = df[df['cluster'] == cluster_id]
    n_users = len(cluster_data)

    print(f"\n【人群 {cluster_id + 1}】({n_users}人, 占比 {n_users/len(df)*100:.1f}%)")

    # 性别分布
    gender_dist = cluster_data['性别'].value_counts(normalize=True).head(2)
    main_gender = gender_dist.index[0]

    # 内容偏好
    content_dist = cluster_data['内容偏好'].value_counts(normalize=True)
    main_content = content_dist.index[0]

    # 垂类聚合
    category_dist = cluster_data['垂类聚合'].value_counts(normalize=True).head(3)
    main_categories = list(category_dist.index)

    # 年龄
    age_dist = cluster_data['年龄'].value_counts(normalize=True)
    main_age = age_dist.index[0]

    # 操作系统
    os_dist = cluster_data['操作系统'].value_counts(normalize=True)
    main_os = os_dist.index[0]

    # 城市线
    city_dist = cluster_data['城市线'].value_counts(normalize=True)
    main_city = city_dist.index[0]

    # 消费水平
    consume_dist = cluster_data['消费水平'].value_counts(normalize=True)
    main_consume = consume_dist.index[0]

    # 数值指标均值
    avg_dura = cluster_data['all_dura'].mean()
    avg_ctr = cluster_data['ctr_rate'].mean()
    avg_interaction = cluster_data['interaction_rate'].mean()

    print(f"  性别: {main_gender} ({gender_dist.iloc[0]*100:.1f}%)")
    print(f"  内容偏好: {main_content} ({content_dist.iloc[0]*100:.1f}%)")
    print(f"  主要垂类: {', '.join(main_categories)}")
    print(f"  年龄段: {main_age}")
    print(f"  操作系统: {main_os}")
    print(f"  城市线: {main_city}")
    print(f"  消费水平: {main_consume}")
    print(f"  平均观看时长: {avg_dura:.1f}秒")
    print(f"  平均点击率: {avg_ctr*100:.1f}%")
    print(f"  平均互动率: {avg_interaction*100:.2f}%")

    # 保存到字典
    cluster_profiles[f'cluster_{cluster_id}'] = {
        'name': f'人群 {cluster_id + 1}',
        'count': int(n_users),
        'percentage': round(n_users/len(df)*100, 1),
        'main_gender': main_gender,
        'gender_ratio': {k: round(v*100, 1) for k, v in gender_dist.items()},
        'main_content': main_content,
        'content_ratio': {k: round(v*100, 1) for k, v in content_dist.items()},
        'main_categories': main_categories,
        'main_age': main_age,
        'main_os': main_os,
        'main_city': main_city,
        'main_consume': main_consume,
        'avg_dura': round(avg_dura, 1),
        'avg_ctr': round(avg_ctr*100, 2),
        'avg_interaction': round(avg_interaction*100, 2)
    }

# 保存聚类结果
with open(r'C:\Users\HONOR\Documents\trae_projects\AI-TRY1\dashboard\cluster_profiles.json', 'w', encoding='utf-8') as f:
    json.dump(cluster_profiles, f, ensure_ascii=False, indent=2)

print("\n\n聚类结果已保存到 cluster_profiles.json")
print(f"总用户数: {len(df)}")
