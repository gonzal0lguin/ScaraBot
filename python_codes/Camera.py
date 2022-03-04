import cv2 as cv
from python_codes.defaults import *

class Camera(object):
    def __init__(self, deb_true=False):
        self.img = None
        self.prev = None
        self.curr = None
        self.calibration_img = None #cv.imread(m1)[200:-1, 400:2400] #None
        self.debug = deb_true
        self.green = (0, 255, 0)
        self.user_moves = []
        self.last_user_move = None
        self.pts1 = None

    def initial_transform(self, img):
        """
        :param img: image array
        :return: transformed image array
        """

        w, h = RESOLUTION

        pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
        mat = cv.getPerspectiveTransform(self.pts1, pts2)
        res = cv.warpPerspective(img, mat, RESOLUTION)

        gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (7, 7), 0)
        return blur

    def capture(self, img, calibration=False):  # IMG ES SOLO PARA TESTEAR EN REALIDAD IMG ES LA FOTO QUE SE SACA
        """
        Takes a new photo and updates the previous and current images. It
        aplies the blur and graysacle inmediately
        """

        # pic = picam capture
        # img = cv.imread(pic)
        if not calibration:
            self.img = img  # SOLO PARA PROBAR
            self.prev = self.curr
            self.curr = self.initial_transform(img)
        else:
            self.calibration_img = img
            self.get_calibration_corners(self.calibration_img)

    def compare(self):
        """
        Compare self.prev with self.curr and detect if new user move is
        present. If so, return its coordinates.
        :return: TODO: return in array or pixel format?
        """

        pass

    def detect_user_circles(self, img):
        # convertirla a gray si esq no esta en gray y blurrearla
        circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT,
                                  ACUMM_RES, CIRCLES_DIST, param1=50,
                                  param2=30, minRadius=20, maxRadius=80)

        det_circles = np.uint16(np.around(circles))

        if self.debug:
            for (x, y, r) in det_circles[0, :]:
                cv.circle(img, (x, y), r, (0, 255, 0), 4)
                cv.circle(img, (x, y), 4, (0, 255, 255), 3)

            self.draw_grid()

        return det_circles[0, :]

    def get_user_coords(self):
        try:
            circles = self.detect_user_circles(self.curr)
            circles //= BOX_L

            for (x, y, r) in circles:
                if (x, y) not in self.user_moves:
                    self.user_moves.append((x, y))
                    self.last_user_move = (x, y)
                else:
                    continue
            # print(self.user_moves)
        except:
            pass

    def draw_grid(self, moves=True):
        dx, dy = RESOLUTION[0] // 3, RESOLUTION[1] // 3

        for i in range(2):  # vecrtical -> y // 3
            x1, x2 = 0, 3 * dx
            y1, y2 = dy * (i + 1), dy * (i + 1)
            cv.line(self.curr, (x1, y1), (x2, y2), self.green, LINE_THICKNESS)

        for i in range(2):  # vecrtical -> y // 3
            x1, x2 = dx * (i + 1), dx * (i + 1)
            y1, y2 = 0, 3 * dy
            cv.line(self.curr, (x1, y1), (x2, y2), self.green, LINE_THICKNESS)

        if moves:
            for (x, y) in self.user_moves:
                cv.circle(self.curr, (BOX_L // 2 + x * BOX_L, BOX_L // 2 + y * BOX_L), 50, (255, 0, 0), 3)

    def get_calibration_corners(self, img):
        try:
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            blur = cv.GaussianBlur(gray, (7, 7), 0)
            canny = cv.Canny(blur, 50, 100)

            corners = cv.goodFeaturesToTrack(canny, N_CORNERS, MIN_QUALTY, MIN_CORNER_DIST)
            corners = np.int0(corners)
            if self.debug:
                for corner in corners:
                    x, y = corner.ravel()
                    cv.circle(img, (x, y), 30, (0, 255, 0), 5)
                print(corners)

            self.pts1 = np.float32(self.order_corners(corners[:, 0]))
        except:
            self.pts1 = np.float32(CORNERS)
            print('Using defaults to calibrate...')

    @staticmethod
    def order_corners(corners):
        ord = [None] * 4
        dists = {0: 0, 1: 0, 2: 0, 3: 0}
        i = 0
        for (x, y) in corners:
            dists[i] = np.linalg.norm([x, y])
            i += 1

        sortedv = dict(sorted(dists.items(), key=lambda item: item[1]))
        key_list = list(sortedv.keys())

        for i in range(len(ord)):
            ord[i] = corners[key_list[i]]

        return ord

    def clean(self):
        self.__init__()



if __name__ == "__main__":

    cal = cv.imread(m1)[200:-1, 400:2400] # y, x
    img = cv.imread(circles)[200:-1, 400:2400] # y, x
    cam = Camera(True)
    cam.capture(cal, calibration=True)
    cam.capture(img)
    cam.get_user_coords()
    cam.draw_grid()

    cv.imshow('img', cam.calibration_img)
    cv.imshow('processed', cam.curr)
    cv.waitKey(0)
    cv.destroyAllWindows()
