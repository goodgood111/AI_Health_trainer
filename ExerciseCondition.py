import cv2
import numpy as np
import PoseModule as pm


class ExerciseType(pm.poseDetector):

    def __init__(self, width, height, fps):
        super().__init__()
        self.width = width
        self.height = height
        self.fps = fps

        self.count = 0
        self.color = (255, 0, 255)

        self.dir = 0
        self.Up = False
        self.Down = False

        self.check = False
        self.Landmarks = {'nose': 0, 'left_eye_inner': 1, 'left_eye': 2, 'left_eye_outer': 3,
                          'right_eye_inner': 4, 'right_eye': 5, 'right_eye_outer': 6, 'left_ear': 7,
                          'right_ear': 8, 'mouth_left': 9, 'mouth_right': 10, 'left_shoulder': 11,
                          'right_shoulder': 12, 'left_elbow': 13, 'right_elbow': 14, 'left_wrist': 15,
                          'right_wrist': 16, 'left_pinky': 17, 'right_pinky': 18, 'left_index': 19,
                          'right_index': 20, 'left_thumb': 21, 'right_thumb': 22, 'left_hip': 23,
                          'right_hip': 24, 'left_knee': 25, 'right_knee': 26, 'left_ankle': 27,
                          'right_ankle': 28, 'left_heel': 29, 'right_heel': 30, 'left_foot_index': 31,
                          'right_foot_index': 32}

    def SelectExerciseMode(self, img, Mode, draw=True):

        if Mode == 'barbellCurl':
            p1, p2, p3 = self.Landmarks['left_shoulder'], self.Landmarks['left_elbow'],\
                self.Landmarks['left_wrist']

            Angle = self.findAngle(img, p1, p2, p3, draw)
            ref_low = 225
            ref_high = 305
            per = np.interp(Angle, (ref_low, ref_high), (0, 100))
            bar = np.interp(Angle, (ref_low + 10, ref_high), (self.height-100, 100))

            if per >= 60:
                self.Up = True
                if per == 100:
                    self.color = (0, 255, 0)
                    if self.dir == 0:
                        self.count += .5
                        self.dir = 1
                        self.check = True
                if (int(per) > 80) & (int(per) < 100) & (self.check == False):
                    cv2.putText(img, 'UP! UP! UP!', (250, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                                (0, 0, 255), 3)

            if per == 0:
                self.color = (0, 255, 0)
                if self.dir == 1:
                    self.count += .5
                    self.dir = 0
                    self.Up = False
                    self.check = False
                elif (self.Up == True) & (self.dir == 0):
                    self.check = False
                    # cv2.putText(img, 'MORE Arm UP!!!', (250, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    #             (0, 0, 255), 3)

        elif Mode == 'pushup':
            p1, p2, p3 = self.Landmarks['left_shoulder'], self.Landmarks['left_elbow'],\
                self.Landmarks['left_wrist']
            p4, p5, p6 = self.Landmarks['right_shoulder'], self.Landmarks['right_elbow'],\
                self.Landmarks['right_wrist']
            p7, p8, p9 = self.Landmarks['left_shoulder'], self.Landmarks['left_hip'], \
                self.Landmarks['left_knee']
            p10, p11, p12 = self.Landmarks['left_hip'], self.Landmarks['left_knee'], \
                self.Landmarks['left_ankle']
            p13, p14, p15 = self.Landmarks['right_hip'], self.Landmarks['right_knee'], \
                self.Landmarks['right_ankle']

            Angle_arm_L = self.findAngle(img, p1, p2, p3, draw)
            Angle_arm_R = self.findAngle(img, p4, p5, p6, draw)

            ref_low = 225
            ref_high = 250

            per = np.interp(Angle_arm_L, (ref_low, ref_high), (0, 100))
            per_R = np.interp(Angle_arm_R, (ref_low, ref_high), (0, 100))
            bar = np.interp(Angle_arm_L, (ref_low + 10, ref_high), (self.height-100, 100))

            Angle_back = self.findAngle(img, p7, p8, p9, draw=False)
            Angle_leg_left = self.findAngle(img, p10, p11, p12, draw=True)
            Angle_leg_right = self.findAngle(img, p13, p14, p15, draw=True)

            if (int(Angle_leg_left) < 180) & (int(Angle_leg_left) > 160) &\
                    (int(Angle_leg_right) < 180) & (int(Angle_leg_right) > 160):

                if (per >= 70) & (per_R >= 70):
                    self.Up = True
                    if per == 100:
                        self.color = (0, 255, 0)
                        # & (int(Angle_back) < 210) & (int(Angle_back) > 170):
                        if (self.dir == 0):
                            self.count += .5
                            self.dir = 1
                            self.check = True
                    if (int(per) > 80) & (int(per) < 100) & (self.check == False):
                        cv2.putText(img, 'MORE! MORE! MORE!', (250, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                                    (0, 0, 255), 3)

                if (per == 0) & (per_R == 0):
                    self.color = (0, 255, 0)
                    
                    if (self.dir == 1):
                        self.count += .5
                        self.dir = 0
                        self.Up = False
                        self.check = False
                    elif (self.Up == True) & (self.dir == 0):
                        self.check = False
                        cv2.putText(img, 'BEND YOUR ARMS MORE !!!', (250, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                                    (0, 0, 255), 3)
            else:
                per = 0
                bar = self.height-100

            self.Draw(img, per, bar)

        elif Mode == 'squat':  # side
            p1, p2, p3 = self.Landmarks['left_hip'], self.Landmarks['left_knee'], \
                self.Landmarks['left_ankle']
            p4, p5, p6 = self.Landmarks['right_hip'], self.Landmarks['right_knee'], \
                self.Landmarks['right_ankle']
            p7, p8, p9 = self.Landmarks['left_ear'], self.Landmarks['left_shoulder'], \
                self.Landmarks['left_hip']

            Angle_leg_left = self.findAngle(img, p1, p2, p3, draw)
            Angle_leg_right = self.findAngle(img, p4, p5, p6, draw)
            Angle_left_side = self.findAngle(img, p7, p8, p9, draw)

            ref_low = 90
            ref_high = 150

            per = np.interp(Angle_leg_left, (ref_low, ref_high), (0, 100))
            bar = np.interp(Angle_leg_left, (ref_low + 10, ref_high), (100, self.height-100))

            if (int(Angle_left_side) < 220) & (int(Angle_left_side) > 170):

                if per <= 40:
                    self.Down = True
                    if per == 0:
                        self.color = (0, 255, 0)
                        if self.dir == 0:
                            self.count += .5
                            self.dir = 1
                            # self.check = True
                    if (int(per) < 30) & (int(per) > 0) & (self.check == False):  # 30 0
                        cv2.putText(img, 'DOWN! DOWN! DOWN!', (250, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                                    (0, 0, 255), 3)

                if per == 100:
                    self.color = (0, 255, 0)
                    if self.dir == 1:
                        self.count += .5
                        self.dir = 0
                        self.Down = False
                        self.check = False
                    elif (self.Down == True) & (self.dir == 0):
                        self.check = False
                        cv2.putText(img, 'MORE LEGS DOWN!!!', (250, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                                    (0, 0, 255), 3)
                #
                per = 100 - per
            else:
                per = 0
                bar = self.height-100

            self.Draw(img, per, bar)

    def Draw(self, img, per, bar):
        cv2.rectangle(img, (0, 0), (150, 200), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(self.count)), (20, 150), cv2.FONT_HERSHEY_PLAIN, 10,
                    (255, 0, 0), 10)

        cv2.rectangle(img, (self.width -100, 100), (self.width - 50, self.height-100),
                      self.color, 3)
        cv2.rectangle(img, (self.width -100, int(bar)), (self.width - 50, self.height-100),
                      self.color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 80), cv2.FONT_HERSHEY_PLAIN, 3,
                    self.color, 3)

        return self.count
