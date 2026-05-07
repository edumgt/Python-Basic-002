# Day 153 – Transformer 기반 시계열 예측

> **소요시간**: 8시간 | **Phase**: 7 확장 – 최신 시계열 모델

---

## 🎯 학습 목표

- Self-Attention 기반 시계열 예측 구조 이해
- Positional Encoding을 활용한 시계열 입력 설계
- 간단한 Transformer Encoder 모델 구현
- LSTM/CNN 대비 성능과 해석 가능성 비교

---

## 📖 이론 (08:00 – 10:00)

### 1. Transformer 핵심
- Attention으로 시점 간 중요도를 직접 학습
- 병렬 처리에 강하고 긴 의존성 표현에 유리
- 데이터가 적으면 과적합 리스크 증가

### 2. 금융 시계열 적용 포인트
- 윈도우 기반 인코더 입력
- 멀티헤드 수·차원·드롭아웃 조정 필수
- 조기종료·정규화 적용 권장

---

## 🧪 LAB 1 – Transformer Encoder 구현 (10:00 – 12:00)

```python
from tensorflow import keras
from keras import layers

inputs = keras.Input(shape=(40, 8))
x = layers.LayerNormalization()(inputs)
attn = layers.MultiHeadAttention(num_heads=4, key_dim=16)(x, x)
x = layers.Add()([x, attn])
x = layers.LayerNormalization()(x)
ffn = layers.Dense(64, activation="relu")(x)
ffn = layers.Dense(32)(ffn)
x = layers.Add()([x, ffn])
x = layers.GlobalAveragePooling1D()(x)
outputs = layers.Dense(1, activation="sigmoid")(x)

model = keras.Model(inputs, outputs)
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
```

---

## 🧪 LAB 2 – Attention 기반 해석 (13:00 – 15:00)

- 특정 예측에서 어떤 시점이 중요했는지 Attention weight 확인
- 급락 직전 패턴, 거래량 급증 구간의 중요도 변화 분석

---

## 🧪 LAB 3 – 모델 비교 평가 (15:00 – 17:00)

- 비교 모델: RandomForest, LSTM, Transformer
- 지표: Accuracy, AUC, MDD 개선 여부, 신호 안정성

---

## ✅ 체크리스트

- [ ] Transformer Encoder 모델 구현 완료
- [ ] Attention 시각화 결과 확보
- [ ] 기존 모델 대비 비교표 작성 완료
