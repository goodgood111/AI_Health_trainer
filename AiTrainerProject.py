import cv2
import time
import ExerciseCondition as EC

Exercise_type = {1: 'pushup', 2: 'barbellCurl', 3: 'squat'}
Routine_type = {'Legs': [3, 1, 2], 'Arms': [1, 3, 2]}
Routine = 'Legs'

# 'pose/squat.mp4' pose/Boy1920x1080.mp4 pose/pushup.mp4 pose/pushupvideo.mp4 pose/barbellcurl2.mp4
# pose/SquatsideView.mp4 pose/squat2
# openCV 영상크기 정해주기.(bar를 그리기 위해서).
cap = cv2.VideoCapture(0)
fps = round(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

delay = round(1000 / fps)

#녹화
# codec = cv2.VideoWriter_fourcc(*"MJPG")
# writer = cv2.VideoWriter('pose/webcam_output.avi', codec, fps, (width, height))

detector = EC.ExerciseType(width,height,fps)

time.sleep(2)
# 2초정도 준비시간 부여.
start = time.time()
idx = 0

while True:
    success, img = cap.read()
    # img = cv2.resize(img, (width*2, height*2))
    # img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
    # img = cv2.flip(img, 0)
    # img = cv2.flip(img, 1)

    Exercise = Routine_type[Routine]

    img = detector.findPose(img, draw=False)
    lmList = detector.findPosition(img, draw=False)
    #정의해놓은 landmarks 찾기.

    if len(lmList) != 0:
        current = time.time()-start
        #걸린시간 계산 시작
        count = detector.SelectExerciseMode(img, Exercise_type[Exercise[idx]])
        if (int(current) == 25) | (count == 10):
        #시간이 넘거나 계수가 만족되면 다음운동.
            idx += 1
            start = time.time()

    cv2.rectangle(img, (0, height - 200), (150, height),
                  (0, 255, 0), cv2.FILLED)
    cv2.putText(img, '{:.1f}'.format(current), (15, height-75), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)
    cv2.putText(img, Exercise_type[Exercise[idx]], (15+150, height-50), cv2.FONT_HERSHEY_PLAIN, 5,
                (0, 0, 255), 5)
    #하고있는 운동, 초 등등 보여주기
    cv2.imshow('image', img)
    if cv2.waitKey(2) == 27:
    # ESC누르면 꺼짐.
        break
    #녹화
    # detector.VideoSave(writer, img) 

#녹화
# writer.release()
cap.release()
cv2.destroyAllWindows()
#비디오 닫기
#모든창을 닫기
