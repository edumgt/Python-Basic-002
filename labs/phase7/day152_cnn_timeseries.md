# Day 152 – CNN 기반 시계열 패턴 분류

> **소요시간**: 8시간 | **Phase**: 7 확장 – 딥러닝 보강

---

## 🎯 학습 목표

- 1D CNN으로 시계열 패턴 특징 추출
- LSTM 대비 CNN의 장단점 이해
- 윈도우 데이터셋 생성 및 학습 파이프라인 구성
- 예측 성능과 학습 속도 비교

---

## 📖 이론 (08:00 – 10:00)

### 1. CNN을 시계열에 쓰는 이유
- 국소 패턴(급등·급락·반전) 추출에 강함
- 병렬 계산에 유리하여 학습 속도 빠름
- 긴 의존성은 LSTM/Transformer 대비 약할 수 있음

### 2. 입력 텐서
- 형태: `(batch, timesteps, features)`
- 예: 30일 × 6특성 윈도우

---

## 🧪 LAB 1 – 1D CNN 모델 구현 (10:00 – 12:00)

```python
from tensorflow import keras
from keras import layers

model = keras.Sequential([
    layers.Conv1D(32, 3, activation="relu", input_shape=(30, 6)),
    layers.Conv1D(64, 3, activation="relu"),
    layers.GlobalMaxPooling1D(),
    layers.Dense(32, activation="relu"),
    layers.Dropout(0.2),
    layers.Dense(1, activation="sigmoid"),
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
```

---

## 🧪 LAB 2 – CNN vs LSTM 비교 실험 (13:00 – 15:00)

- 동일 데이터/동일 피처셋으로 CNN, LSTM 성능 비교
- 비교 지표: Accuracy, AUC, 학습 시간, 추론 시간
- 데이터 누수 방지를 위해 시간 순서 고정 분할

---

## 🧪 LAB 3 – 오류 사례 해석 (15:00 – 17:00)

- CNN 오분류 구간의 캔들/지표 시각화
- 횡보장/급변장 성능 차이 분석
- 모델 개선 아이디어 도출(윈도우 길이, 특성 확장)

---

## ✅ 체크리스트

- [ ] 1D CNN 학습 파이프라인 구현 완료
- [ ] LSTM 대비 성능·속도 비교표 작성
- [ ] 오분류 구간 분석 리포트 작성
