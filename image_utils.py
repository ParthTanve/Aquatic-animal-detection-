import cv2

def draw_neon_box(image, box, label, color=(0, 255, 255)):
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    cv2.putText(image, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return image

def get_crop(frame, box):
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    return cv2.cvtColor(frame[y1:y2, x1:x2], cv2.COLOR_BGR2RGB)