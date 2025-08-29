# 금속 부품 이미지 판별

조명/각도/배경이 달라진 금속 부품 이미지를 **OpenCV ORB 특징 매칭**으로 비교해 같은 부품인지 판별한 전통 컴퓨터 비전 프로젝트입니다.

<p align="center">
  <img src="docs/images/success_sample.jpg" alt="same-match" width="45%">
  <img src="docs/images/failure_sample.jpg" alt="diff-match" width="45%">
</p>

## 데이터
- 위치(로컬): `C:\opencv\img`
- 파일명 규칙: `A0.jpg ~ D9.jpg` (예: A5.jpg)

## 실행 방법
```bash
# 가상환경/패키지 설치 후
pip install -r requirements.txt

# 스크립트 실행 
python Opencv.py
