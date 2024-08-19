def calculate_distance(bbox1, bbox2):
    """두 바운딩 박스 간의 중심점 거리 계산"""
    x1_center = (bbox1[0] + bbox1[2]) / 2
    y1_center = (bbox1[1] + bbox1[3]) / 2
    x2_center = (bbox2[0] + bbox2[2]) / 2
    y2_center = (bbox2[1] + bbox2[3]) / 2
    distance = np.sqrt((x2_center - x1_center) ** 2 + (y2_center - y1_center) ** 2)
    return distance


def find_closest_object(target_bbox, objects):
    """대상 객체에 가장 가까운 물체를 찾습니다."""
    min_distance = float('inf')
    closest_object = None

    for obj in objects:
        if obj['bbox'] == target_bbox:
            continue  # 동일한 객체는 건너뜁니다.

        distance = calculate_distance(target_bbox, obj['bbox'])
        if distance < min_distance:
            min_distance = distance
            closest_object = obj

    return closest_object


def compare_objects(stored_objects, current_objects):
    """미리 저장된 객체와 현재 객체를 비교하여 일치 여부를 반환합니다."""
    matching_objects = []
    for stored_obj in stored_objects:
        stored_id = stored_obj['class_id']
        stored_bbox = stored_obj['bbox']

        for current_obj in current_objects:
            current_id = current_obj['class_id']
            current_bbox = current_obj['bbox']

            if stored_id == current_id:
                # 위치가 동일한지 비교 (여기서는 BBox 좌표가 정확히 일치하는지 확인)
                if np.array_equal(stored_bbox, current_bbox):
                    matching_objects.append({
                        'id': current_id,
                        'bbox': current_bbox,
                        'status': 'Same position'
                    })
                else:
                    # 가장 가까운 물체를 찾기
                    closest_obj = find_closest_object(current_bbox, current_objects)
                    if closest_obj:
                        closest_obj_name = closest_obj['class_name']
                        matching_objects.append({
                            'id': current_id,
                            'bbox': current_bbox,
                            'status': "New position", 
                            'current_bbox': f"{current_bbox}",
                            'closest to' : f"{closest_obj_name}"
                        })
                    else:
                        matching_objects.append({
                            'id': current_id,
                            'bbox': current_bbox,
                            'status': "New position",
                            'current_bbox' : f"{current_bbox}",
                            'closest to' : "but no other objects detected"
                        })
                break
        else:
            # ID가 없는 경우
            matching_objects.append({
                'id': stored_id,
                'bbox': None,
                'status': 'Not detected'
            })

    return matching_objects

# #테스트
# def main(image_path, stored_objects):
#     # 이미지 로드
#     image = cv2.imread(image_path)

#     # 이미지가 제대로 로드되었는지 확인
#     if image is None:
#         raise ValueError(f"Error: Unable to load image at {image_path}")

#     # 현재 이미지에서 객체 탐지
#     current_objects = detect_objects(image)

#     # 객체 비교
#     result = compare_objects(stored_objects, current_objects)

#     return result


# # 테스트용 미리 저장된 객체 (예시)
# stored_objects = [
#     {'bbox': (905, 3, 1345, 581), 'confidence': 0.36, 'class_id': 62, 'class_name': 'tv',
#      'unique_id': '9cfeb348-65ec-4cec-8b1a-a5898e71df26'},
#     {'bbox': (300, 400, 350, 450), 'confidence': 0.8, 'class_id': 1, 'class_name': 'laptop',
#      'unique_id': 'example-uuid-2'}
# ]

# # 테스트 이미지 경로
# image_path = '/Users/haneul/Downloads/사물이미지.jpg'

# # 메인 함수 호출 및 결과 출력
# try:
#     results = main(image_path, stored_objects)
#     for obj in results:
#         print(f"ID: {obj['id']}, BBox: {obj['bbox']}, Status: {obj['status']}")
# except ValueError as e:
#     print(e)
