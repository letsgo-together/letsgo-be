import cv2
import torch
import uuid

# YOLO 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')


def generate_unique_id():
    """고유한 UUID를 생성합니다."""
    return str(uuid.uuid4())


def detect_objects(image):
    # 이미지에서 객체 탐지
    results = model(image)

    # 탐지된 객체 정보 및 위치 추출
    detected_objects = []
    for det in results.xyxy[0]:
        x1, y1, x2, y2 = map(int, det[:4])
        conf = float(det[4])
        class_id = int(det[5])
        unique_id = generate_unique_id()  # 객체에 고유 ID를 생성
        detected_objects.append({
            'bbox': (x1, y1, x2, y2),
            'confidence': conf,
            'class_id': class_id,
            'class_name': model.names[class_id],
            'unique_id': unique_id
        })

    return detected_objects


if __name__ == '__main__':
    # 이미지 로드
    image_path = '/Users/haneul/Downloads/사물이미지.jpg'  # 실제 이미지 경로로 수정
    image = cv2.imread(image_path)

    # 이미지가 제대로 로드되었는지 확인
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
    else:
        # 객체 탐지
        detected_objects = detect_objects(image)

        # 결과 출력
        for obj in detected_objects:
            print(
                f"Class: {obj['class_name']}, BBox: {obj['bbox']}, Confidence: {obj['confidence']:.2f}, Class ID: {obj['class_id']}, Unique ID: {obj['unique_id']}")
