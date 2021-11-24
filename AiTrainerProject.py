import cv2
import time
import ExerciseCondition as EC

Exercise_type = {1: 'pushup', 2: 'barbellCurl', 3: 'squat'}
Routine_type = {'Legs': [3, 1, 2], 'Arms': [1, 3, 2]}
Routine = 'Legs'

# Decide the size of the openCV video.(For drawing bar as well)
cap = cv2.VideoCapture(0)
fps = round(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

delay = round(1000 / fps)
tput.avi', codec, fps, (width, height))

detector = EC.ExerciseType(width,height,fps)

time.sleep(2)
# give 2 seconds to get ready.
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
    # Finding landmarks.

    if len(lmList) != 0:
        current = time.time()-start
        # Counting time
        count = detector.SelectExerciseMode(img, Exercise_type[Exercise[idx]])
        if (int(current) == 25) | (count == 10):
        # Conditions for moving on to the next exercise.
            idx += 1
            start = time.time()

    cv2.rectangle(img, (0, height - 200), (150, height),
                  (0, 255, 0), cv2.FILLED)
    cv2.putText(img, '{:.1f}'.format(current), (15, height-75), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)
    cv2.putText(img, Exercise_type[Exercise[idx]], (15+150, height-50), cv2.FONT_HERSHEY_PLAIN, 5,
                (0, 0, 255), 5)
    # Showing the kind of exercise and time.
    cv2.imshow('image', img)
    if cv2.waitKey(2) == 27:
        break

cap.release()
cv2.destroyAllWindows()
