# 매칭점 원근 변환으로 영역 찾기 (match_homography.py)
import os
import cv2
import numpy as np

# 한글/윈도우 경로 안전 로더
def imread_unicode(path, flags=cv2.IMREAD_COLOR):
    arr = np.fromfile(path, dtype=np.uint8)
    if arr.size == 0:
        return None
    return cv2.imdecode(arr, flags)

def test(url1_filename, A, B):

    base_path = r"C:/opencv/img/"

    # 실제 경로 조립
    url1 = os.path.join(base_path, url1_filename)
    url2 = os.path.join(base_path, f"{['A','B','C','D'][A]}{B}.jpg")

    # 이미지 로드
    img1 = imread_unicode(url1, cv2.IMREAD_COLOR)
    img2 = imread_unicode(url2, cv2.IMREAD_COLOR)

    if img1 is None:
        print(f"{url2}\tX\t(기준 이미지 없음: {url1})")
        return
    if img2 is None:
        print(f"{url2}\tX\t(비교 이미지 없음)")
        return

    # 리사이즈(연산량 감소)
    img1 = cv2.resize(img1, (0, 0), fx=0.5, fy=0.5)
    img2 = cv2.resize(img2, (0, 0), fx=0.5, fy=0.5)

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # ----- 전처리: B 기준으로 조명/노이즈 조건 분기 -----
    def preprocess(gray, A, B):
        if B >= 5:
            # 배경 노이즈 적고 조명 균일: 단순 이진화 + 침식
            _, th = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
            th = cv2.erode(th, np.ones((3, 3), np.uint8), iterations=2)
        else:
            # 배경 노이즈 많고 밝은 영역 존재: Otsu
            otsu_thr, _ = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            if A == 0:
                _, th = cv2.threshold(gray, otsu_thr, 255, cv2.THRESH_BINARY_INV)
            else:
                _, th = cv2.threshold(gray, otsu_thr, 255, cv2.THRESH_BINARY)
            th = cv2.erode(th, np.ones((2, 2), np.uint8), iterations=3)
        return th

    bin1 = preprocess(gray1, A, B)
    bin2 = preprocess(gray2, A, B)

    # ----- ORB 특징 추출 -----
    orb = cv2.ORB_create(nfeatures=1000)
    kp1, desc1 = orb.detectAndCompute(bin1, None)
    kp2, desc2 = orb.detectAndCompute(bin2, None)

    # 디스크립터/키포인트 가드
    if desc1 is None or desc2 is None or len(kp1) < 4 or len(kp2) < 4:
        print(f"{url2}\tX\t(특징 부족)")
        return

    # ----- 매칭 (KNN + ratio test) -----
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)  # ORB는 해밍 사용
    matches = matcher.knnMatch(desc1, desc2, k=2)

    ratio = 0.75
    good = []
    for m in matches:
        if len(m) < 2:
            continue
        m1, m2 = m
        if m1.distance < ratio * m2.distance:
            good.append(m1)

    # 임계값(경험치): 30개 초과면 매칭 인정
    if len(good) > 30:
        print(f"{url2}\tO", end="\t")
    else:
        print(f"{url2}\tX", end="\t")

    # 매칭 시각화가 필요하면 저장
    res = cv2.drawMatches(img1, kp1, img2, kp2, good, None,
                          flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
    cv2.imwrite(os.path.join(base_path, "last_match.jpg"), res)

if __name__ == "__main__":

    lists = ["A5.jpg", "B5.jpg", "C5.jpg", "D5.jpg"]

    for i in range(4):
        print()
        print("표본 : " + lists[i])
        for j in range(10):
            test(lists[i], 0, j)  # A0~A9
            test(lists[i], 1, j)  # B0~B9
            test(lists[i], 2, j)  # C0~C9
            test(lists[i], 3, j)  # D0~D9
            print()
