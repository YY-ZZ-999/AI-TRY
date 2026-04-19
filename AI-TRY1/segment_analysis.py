# -*- coding: utf-8 -*-
import pandas as pd
import json
import numpy as np

def get_strategy(seg):
    strategies = {
        '高价值活跃用户': [
            {'title': 'VIP专属权益', 'content': '提供会员专属福利、优先体验新功能', 'priority': '高'},
            {'title': '社区荣誉体系', 'content': '建立用户成长体系，赋予特殊标识', 'priority': '高'},
            {'title': '内容共创邀请', 'content': '邀请参与内容创作、优先体验付费内容', 'priority': '中'}
        ],
        '潜力用户': [
            {'title': '个性化推荐优化', 'content': '提升推荐算法精准度', 'priority': '高'},
            {'title': '互动激励计划', 'content': '增加互动道具、点赞评论奖励', 'priority': '高'},
            {'title': '新手引导优化', 'content': '完善功能引导，降低使用门槛', 'priority': '中'}
        ],
        '视频爱好者': [
            {'title': '视频内容池扩充', 'content': '增加优质视频内容供给', 'priority': '高'},
            {'title': '短视频推送优化', 'content': '优化短视频feed流推送策略', 'priority': '中'},
            {'title': '流量包优惠', 'content': '推出专属流量包', 'priority': '低'}
        ],
        '沉默用户': [
            {'title': '流失预警机制', 'content': '7天未活跃用户预警，主动触达', 'priority': '高'},
            {'title': '召回Push策略', 'content': '推送个性化内容、限时福利召回', 'priority': '高'},
            {'title': '简化操作流程', 'content': '优化APP性能，减少卡顿', 'priority': '中'}
        ],
        '普通用户': [
            {'title': '日常活跃激励', 'content': '签到奖励、每日任务体系', 'priority': '中'},
            {'title': '内容多样性引导', 'content': '推荐更多垂类内容', 'priority': '中'},
            {'title': '社交功能曝光', 'content': '强化评论、分享等社交功能', 'priority': '低'}
        ]
    }
    return strategies.get(seg, [])

print("1. 读取数据...", flush=True)
df = pd.read_csv(r'C:\Users\HONOR\Desktop\项目数据\kprototypes_input.csv', encoding='gbk')
df = df.drop(columns=['Unnamed: 12', 'Unnamed: 13'], errors='ignore')
print(f"   完成: {len(df)} 行", flush=True)

print("2. 用户分群...", flush=True)
conditions = [
    ((df['all_dura'] > 2500) & (df['ctr_rate'] > 0.15)) | (df['interaction_rate'] > 0.1),
    (df['all_dura'] > 1500) & (df['interaction_rate'] > 0.05),
    (df['all_dura'] < 800) & (df['interaction_rate'] < 0.02),
    (df['内容偏好'] == '视频') & (df['all_dura'] > 2000)
]
choices = ['高价值活跃用户', '潜力用户', '沉默用户', '视频爱好者']
df['segment'] = np.select(conditions, choices, default='普通用户')

print("3. 统计分群...", flush=True)
segment_counts = df['segment'].value_counts()

print("4. 生成画像...", flush=True)
segment_profiles = {}
segments_order = ['高价值活跃用户', '潜力用户', '视频爱好者', '普通用户', '沉默用户']

for seg_name in segments_order:
    if seg_name not in segment_counts.index:
        continue
    
    s = df[df['segment'] == seg_name]
    n = len(s)
    
    avg_dura = s['all_dura'].mean()
    avg_ctr = s['ctr_rate'].mean()
    avg_inter = s['interaction_rate'].mean()
    
    gender = s['性别'].value_counts(normalize=True)
    content = s['内容偏好'].value_counts(normalize=True)
    category = s['垂类聚合'].value_counts(normalize=True).head(3).index.tolist()
    age = s['年龄'].value_counts(normalize=True).index[0]
    os = s['操作系统'].value_counts(normalize=True).index[0]
    city = s['城市线'].value_counts(normalize=True).index[0]
    consume = s['消费水平'].value_counts(normalize=True).index[0]
    
    segment_profiles[seg_name] = {
        'name': seg_name,
        'count': int(n),
        'percentage': round(n/len(df)*100, 1),
        'main_gender': gender.index[0],
        'gender_ratio': {k: round(v*100,1) for k,v in gender.head(2).items()},
        'main_content': content.index[0],
        'content_ratio': {k: round(v*100,1) for k,v in content.head(2).items()},
        'main_categories': category,
        'main_age': age,
        'main_os': os,
        'main_city': city,
        'main_consume': consume,
        'avg_dura': round(avg_dura,1),
        'avg_ctr': round(avg_ctr*100,2),
        'avg_interaction': round(avg_inter*100,2),
        'strategies': get_strategy(seg_name)
    }
    print(f"   - {seg_name}: {n}人 ({n/len(df)*100:.1f}%)", flush=True)

print("5. 保存结果...", flush=True)
with open(r'C:\Users\HONOR\Documents\trae_projects\AI-TRY1\dashboard\segment_profiles.json', 'w', encoding='utf-8') as f:
    json.dump(segment_profiles, f, ensure_ascii=False, indent=2)

print("✅ 完成!", flush=True)
