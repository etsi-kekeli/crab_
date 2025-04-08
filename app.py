from ultralytics import YOLO
import cv2
import sqlite3
from datetime import datetime

model_path = './runs/detect/train/weights/last.pt'
# test_img = './data/images/train/0b7bfc590045b08c.jpg'

# img = cv2.imread(test_img)
# H, W, _ = img.shape
# print(W, H)
# model = YOLO(model_path)
# res = model(test_img)[0]

# for result in res.boxes.data.tolist():
#     x1, y1, x2, y2, score, class_id = result
    
#     if score > threshold:
#         cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
#         cv2.putText(img, res.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 1, cv2.LINE_AA)

# cv2.imshow('Window', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

def init_db():
    """Creates a table to record the number of crabs if the table doesn't exist."""

    con = sqlite3.connect("crabs.db")
    cursor = con.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS crabs(
                   id INTEGER PRIMARY KEY,
                   date TIMESTAMP,
                   number INTEGER CHECK(number >= 0))""")
    con.commit()
    con.close()

def count_crab(threshold : int = 0.5) -> int:
    """Read a frame from the camera and count the number of crab in the frame
    
    Args:
        threshold (int) : Confidence level to pass for a detection to be consider valid
    
    Returns:
        num (int) : The number of validated crab detections
    """
    model = YOLO(model_path)

    cap = cv2.VideoCapture(0)
    num = 0
    ret, frame = cap.read()
    if ret:
        results = model(frame)[0]
        for result in results.boxes.data.tolist():
            _, _, _, _, score, _ = result

            if score > threshold:
                num += 1
    
    return num

def record(number: int) -> None:
    """Add the number of crab to crabs table
    
    Args :
        number (int) : the number of crab detected
    """

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con = sqlite3.connect("crabs.db")
    cursor = con.cursor()
    cursor.execute("INSERT INTO crabs(date, number) VALUES (?, ?)", (now, number))
    con.commit()
    con.close()

if __name__ == "__main__" :
    init_db()
    num = count_crab()
    record(num)
