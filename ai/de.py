import cv2
import torch
import uuid

# YOLO 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')


def generate_unique_id():
    """고유한 UUID를 생성합니다."""
    return str(uuid.uuid4())


def detect_objects(image):
    """이미지에서 객체를 탐지하고 정보를 반환합니다."""
    results = model(image)

    detected_objects = []
    for det in results.xyxy[0]:
        x1, y1, x2, y2 = map(int, det[:4])
        conf = float(det[4])
        class_id = int(det[5])
        unique_id = generate_unique_id()
        bbox = (x1, y1, x2, y2)

        detected_objects.append({
            'bbox': bbox,
            'confidence': conf,
            'class_id': class_id,
            'class_name': model.names[class_id],
            'unique_id': unique_id
        })

    return detected_objects


def describe_relative_position(selected_object, all_objects):
    """선택된 물건의 위치를 주변 물건에 기반하여 설명합니다."""
    x1_sel, y1_sel, x2_sel, y2_sel = selected_object['bbox']
    description = []

    for obj in all_objects:
        if obj['unique_id'] == selected_object['unique_id']:
            continue  # 자기 자신은 비교 대상에서 제외

        x1, y1, x2, y2 = obj['bbox']
        object_name = obj['class_name']

        # 위치 관계 설명
        if y2_sel < y1:  # 선택된 물건이 위쪽에 있는 경우
            description.append(f"{object_name} 아래에 있습니다.")
        elif y1_sel > y2:  # 선택된 물건이 아래쪽에 있는 경우
            description.append(f"{object_name} 위에 있습니다.")
        elif x2_sel < x1:  # 선택된 물건이 왼쪽에 있는 경우
            description.append(f"{object_name} 오른쪽에 있습니다.")
        elif x1_sel > x2:  # 선택된 물건이 오른쪽에 있는 경우
            description.append(f"{object_name} 왼쪽에 있습니다.")
        else:
            description.append(f"{object_name}과(와) 근접해 있습니다.")

    return ', '.join(description)


def find_and_describe_object(image_path, selected_item_name):
    """이미지에서 객체를 탐지하고 선택된 물건의 위치를 설명합니다."""
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return None

    # 객체 탐지
    detected_objects = detect_objects(image)

    # 선택된 물건 찾기
    selected_object = None
    for obj in detected_objects:
        if obj['class_name'] == selected_item_name:
            selected_object = obj
            break

    if selected_object is None:
        print(f"Error: Selected item '{selected_item_name}' not found in the image.")
        return None

    # 선택된 물건의 위치 설명
    position_description = describe_relative_position(selected_object, detected_objects)

    print(f"'{selected_item_name}'의 위치 설명: {position_description}")
    return position_description


# 이미지 파일 경로와 선택된 물건 이름 설정
image_path = '/Users/haneul/Downloads/사물이미지.jpg'  # 실제 이미지 경로로 수정
selected_item_name = 'cell'  # 예: 'bottle'

# 위치 설명 함수 실행
find_and_describe_object(image_path, selected_item_name)
