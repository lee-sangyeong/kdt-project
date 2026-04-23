import pandas as pd

# 1. 데이터 불러오기
df = pd.read_csv('최종쿼리.csv')

# 2. 전체 평균 계산 (기준선)
avg_price = df['avg_land_price'].mean()
avg_shop  = df['shop_count'].mean()

# 3. 4분면 분류 함수
def classify(row):
    if row['avg_land_price'] >= avg_price and row['shop_count'] >= avg_shop:
        return '① 이미 잘 되는 동네지만, 새로 들어가긴 늦었다'
    elif row['avg_land_price'] >= avg_price and row['shop_count'] < avg_shop:
        return '② 돈 있으면 가능, 소상공인에겐 부담'
    elif row['avg_land_price'] < avg_price and row['shop_count'] < avg_shop:
        return '③ 아직 안 붐볐는데, 들어가기 좋은 타이밍 ⭐'
    else:
        return '④ 싸게 들어가지만, 싸게 싸우는 시장'

# 4. 분류 적용
df['startup_strategy'] = df.apply(classify, axis=1)

# 5. 인구 대비 점포 지표 추가 (설득력용)
df['people_per_shop'] = df['population'] / df['shop_count'].replace(0, pd.NA)

# 6. 정렬 (발표용)
df = df.sort_values(
    by=['startup_strategy', 'people_per_shop'],
    ascending=[True, False]
)

# 7. 결과 저장
df.to_csv('dong_startup_final_result.csv', index=False, encoding='utf-8-sig')

# 8. 확인 출력
print(df.head(20))

# 시각화
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import koreanize_matplotlib
from matplotlib.lines import Line2D

df = pd.read_csv('최종쿼리(1).csv')  # 네 파일명 유지

# ================================
# 2. 기준선
# ================================
avg_price = df['avg_land_price'].mean()
avg_shop = df['shop_count'].mean()

# ================================
# 3. 색상 매핑 (구/군)
# ================================
gu_list = df['gu_name'].unique()
colors = plt.cm.tab10.colors
color_map = dict(zip(gu_list, colors[:len(gu_list)]))

# ==========================================
# 4. 최적 후보 개수 (구/군별 집계)
# ==========================================
optimal_count = (
    df[df['quadrant'] == '저가·저밀 (최적 후보)']
    .groupby('gu_name')
    .size()
    .sort_values(ascending=False)
)

print("구/군별 최적 후보 동 개수")
print(optimal_count)

# ================================
# 4. 시각화
# ================================
plt.figure(figsize=(16, 10))

for gu in gu_list:
    sub = df[df['gu_name'] == gu]
    plt.scatter(
        sub['avg_land_price'],
        sub['shop_count'],
        s=sub['population'] / 40,   # 점 크기 = 인구
        alpha=0.6,
        color=color_map[gu],
        edgecolors='black',
        linewidth=0.3
    )

# 기준선
plt.axvline(avg_price, color='red', linestyle='--', linewidth=1)
plt.axhline(avg_shop, color='red', linestyle='--', linewidth=1)

plt.xscale('log')

# ================================
# 5. 4분면 텍스트
# ================================
# -----------------------------
# 사분면 설명 텍스트 (모서리 배치)
# -----------------------------
text_kwargs = dict(
    fontsize=13,
    fontweight='bold',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.85),
    ha='center',
    va='center'
)

# 축 범위 가져오기
xmin, xmax = plt.xlim()
ymin, ymax = plt.ylim()

# ① 공시지가 낮음 + 고깃집 많음
plt.text(
    xmax * 0.0008, ymax * 0.95,
    "① 공시지가 낮음\n고깃집 많음\n(저가 경쟁)",
    **text_kwargs
)

# ② 공시지가 높음 + 고깃집 많음
plt.text(
    xmax * 0.6, ymax * 0.95,
    "② 공시지가 높음\n고깃집 많음\n(포화-비추천)",
    **text_kwargs
)

# ③ 공시지가 낮음 + 고깃집 적음
plt.text(
    xmax * 0.0008, ymax * 0.001,
    "③ 공시지가 낮음\n고깃집 적음\n(최적 후보)",
    **text_kwargs
)

# ④ 공시지가 높음 + 고깃집 적음
plt.text(
    xmax * 0.6, ymax * 0.001,
    "④ 공시지가 높음\n고깃집 적음\n(자본형)",
    **text_kwargs
)


# ================================
# 6. 🔥 범례 정리 (핵심)
# ================================

# (1) 구/군 색상 범례
color_legend = [
    Line2D([0], [0], marker='o', color='w',
           label=gu,
           markerfacecolor=color_map[gu],
           markersize=8)
    for gu in gu_list
]

legend1 = plt.legend(
    handles=color_legend,
    title='구/군',
    bbox_to_anchor=(1.02, 1),
    loc='upper left'
)

# (2) 인구 크기 범례
size_values = [30000, 60000, 100000]

# 범례에서는 크기를 과장해서 단계적으로 벌림
legend_sizes = [300, 800, 1400]   # ← 핵심: 직접 간격 조절

size_legend = [
    plt.scatter(
        [], [],
        s=s,
        facecolors='none',
        edgecolors='gray',
        linewidths=2,
        label=f'인구 {v:,}명'
    )
    for v, s in zip(size_values, legend_sizes)
]

legend2 = plt.legend(
    handles=size_legend,
    title='동별 인구 규모',
    bbox_to_anchor=(1.02, 0.55),
    loc='upper left',
    labelspacing=3,   # 텍스트 간격도 추가
    frameon=True
)



plt.gca().add_artist(legend1)

# ================================
# 7. 마무리
# ================================
plt.title('대구 동별 고깃집 창업 4분면 분석', fontsize=16)
plt.xlabel('동별 평균 공시지가')
plt.ylabel('고깃집 수')

plt.tight_layout()
plt.show()

