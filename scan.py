import cv2
import numpy as np

# 카메라 캡처 설정
cap = cv2.VideoCapture(1)

def calculate_distance_to_object(frame):
    frame_center = (frame.shape[1] // 2, frame.shape[0] // 2)
    box_size = 200
    box_top_left = (frame_center[0] - box_size // 2, frame_center[1] - box_size // 2)
    box_bottom_right = (frame_center[0] + box_size // 2, frame_center[1] + box_size // 2)
    
    # 중앙 박스 그리기
    cv2.rectangle(frame, box_top_left, box_bottom_right, (255, 0, 0), 2)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        # 카드의 넓이와 높이 비율로 카드 여부 판단 (예: 신용카드 비율 약 1.6:1)
        aspect_ratio = w / float(h)
        if 1.5 < aspect_ratio < 1.7 and w * h > 5000:
            object_center = (x + w // 2, y + h // 2)
            if (box_top_left[0] < object_center[0] < box_bottom_right[0] and 
                box_top_left[1] < object_center[1] < box_bottom_right[1]):
                cv2.putText(frame, "인식됨", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                print("True")
                return frame
    print("False")
    return frame

while True:
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = calculate_distance_to_object(frame)

    cv2.imshow('Object Distance', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
