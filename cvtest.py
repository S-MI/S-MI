import cv2
import time

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)    
    while True:
        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_180)        
        cv2.imshow("img", frame)
        if cv2.waitKey(100) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

