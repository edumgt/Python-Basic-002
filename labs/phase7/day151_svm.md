# Day 151 – SVM 기반 주가 방향 분류

> **소요시간**: 8시간 | **Phase**: 7 확장 – 머신러닝 보강

---

## 🎯 학습 목표

- SVM(Linear/RBF)으로 상승·하락 분류 모델 구현
- 시계열 데이터에서 `TimeSeriesSplit` 기반 검증 수행
- 커널/정규화/C·gamma 하이퍼파라미터 영향 이해
- 분류 성능(Accuracy·F1·AUC)과 신호 품질 비교

---

## 📖 이론 (08:00 – 10:00)

### 1. SVM 핵심 개념
- 마진 최대화로 일반화 성능 확보
- 커널 트릭으로 비선형 경계 분리
- 금융 데이터에서는 과적합 방지를 위해 파라미터 범위 제한이 중요

### 2. 실무 권장 설정
- 입력 정규화(`StandardScaler`) 필수
- `class_weight='balanced'`로 불균형 대응
- 시계열 순서 보존 검증(`TimeSeriesSplit`) 사용

---

## 🧪 LAB 1 – SVM 분류기 구현 (10:00 – 12:00)

```python
import yfinance as yf
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# 데이터 준비
close = yf.download("AAPL", period="5y", auto_adjust=True)["Close"].dropna()
df = pd.DataFrame(index=close.index)
df["ret_1"] = close.pct_change(1)
df["ret_5"] = close.pct_change(5)
df["ma_ratio"] = close / close.rolling(20).mean() - 1
df["target"] = (close.shift(-1) > close).astype(int)
df = df.dropna()

X = df[["ret_1", "ret_5", "ma_ratio"]]
y = df["target"]

model = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(kernel="rbf", C=5.0, gamma="scale", probability=True, class_weight="balanced")),
])
model.fit(X, y)
```

---

## 🧪 LAB 2 – 시계열 교차검증 & 튜닝 (13:00 – 15:00)

- `TimeSeriesSplit` 5-fold로 AUC 평균 비교
- 후보 파라미터: `kernel={linear, rbf}`, `C={0.1,1,5,10}`, `gamma={scale,0.1,0.01}`
- 최종 모델의 혼동행렬/정밀도/재현율 비교

---

## 🧪 LAB 3 – 신호 품질 분석 (15:00 – 17:00)

- SVM 확률 출력으로 임계값별 매수 신호 수 변화 확인
- 임계값 0.5/0.6/0.7 비교 백테스트
- 오탐(False Positive) 비중이 높은 구간 해석

---

## ✅ 체크리스트

- [ ] SVM 파이프라인 구현 완료
- [ ] 시계열 교차검증 결과 표 작성
- [ ] 커널/하이퍼파라미터별 성능 비교 완료
- [ ] 임계값 기반 전략 신호 변화 분석 완료
