# Day 154 – 종목 클러스터링 (KMeans/DBSCAN)

> **소요시간**: 8시간 | **Phase**: 7 확장 – 군집화/해석

---

## 🎯 학습 목표

- 종목 특성 기반 비지도 군집화 수행
- KMeans와 DBSCAN 차이점 이해
- 군집별 투자 의미(성장/가치/고변동성) 해석
- 군집 결과를 스크리닝에 연결

---

## 📖 이론 (08:00 – 10:00)

- KMeans: 군집 수 사전 지정, 빠르고 직관적
- DBSCAN: 밀도 기반, 이상치 탐지에 유리
- 대표 특성: 변동성, 모멘텀, 거래대금, 밸류에이션 지표

---

## 🧪 LAB 1 – KMeans 군집화 (10:00 – 12:00)

```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

X_scaled = StandardScaler().fit_transform(features_df)
km = KMeans(n_clusters=4, random_state=42, n_init=20)
labels = km.fit_predict(X_scaled)
features_df["cluster"] = labels
```

---

## 🧪 LAB 2 – DBSCAN 및 이상치 탐지 (13:00 – 15:00)

- `eps`, `min_samples` 조정에 따른 군집 수 변화 관찰
- 노이즈(-1) 종목을 고위험 감시 리스트로 분류

---

## 🧪 LAB 3 – 군집 의미 해석 (15:00 – 17:00)

- 군집별 평균 지표 요약표 작성
- 군집별 대표 종목 선정 및 투자 아이디어 정리

---

## ✅ 체크리스트

- [ ] KMeans/DBSCAN 모두 실행 완료
- [ ] 군집별 특성 해석 리포트 작성
- [ ] 군집 기반 스크리닝 규칙 정의 완료
