import io
import math
import multiprocessing
import threading

import cv2
import imutils
import requests
import  numpy as np
import Detect_border_not_Circle as Al
# import  tensorflow as tf
# from  tensorflow import  keras
# import  detect_curve as detect_curve
import  Meshing
import visvis as vv



import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rc('axes', labelsize=14)
mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)

class Detect_Shape_C :
    path = ""
    list_circle =[]
    corner_list = []
    list_point = None
    LIST_POint = []


    def __int__(self,path):
        self.path =  path
        self.response_json   = None
        self.list_circle = None
        self.corner_list = []
        self.list_point  = None
        self. LIST_POint = []

    def setPath(self , path):
        self.path =   path

    def get_LIST_POINT(self):
        return self.LIST_POint
    def getlist_point(self):
        return self.list_point
    def get_corner_list(self):
        return self.corner_list

    def getcoordinate_from_API(self):


        img = cv2.imread(self.path)

        image = cv2.cvtColor(img, cv2.cv2.COLOR_BGR2RGB)
        pilImage = Image.fromarray(image)

        buffered = io.BytesIO()
        pilImage.save(buffered, quality=100, format="JPEG")

        m = MultipartEncoder(fields={'file': ("imageToUpload", buffered.getvalue(), "image/jpeg")})

        response = requests.post("https://detect.roboflow.com/steel_shape_c/1?api_key=5CTrdY2PU4A5uX2kn35g", data=m,
                                 headers={'Content-Type': m.content_type})

        # print(response)
        # print(response.json())
        self.response_json =  response.json()

    def Draw_rectangel_in_image(self):
        img = cv2.imread(self.path)

        x = self.response_json["predictions"][0]["x"]
        y =  self.response_json["predictions"][0]["y"]

        width =  self.response_json["predictions"][0]["width"]

        height =  self.response_json["predictions"][0]["height"]

        x1 = x - (width / 2)
        y1 = y - (height / 2)
        x2 = x + (width / 2)
        y2 = y + (height / 2)

        Start_Point = (int(x1), int(y1))
        End_point = (int(x2), int(y2))
        print(Start_Point, End_point)

        color = (156, 45, 56)

        thickness = 2

        image = cv2.rectangle(img, Start_Point, End_point, color, thickness, None)

        return
    def Remove_bg(self):

        # response = requests.post(
        #     'https://api.remove.bg/v1.0/removebg',
        #     files={'image_file': open(self.path, 'rb')},
        #     data={'size': 'auto'},
        #     headers={'X-Api-Key': 'ubbV2ozhWwBEg8FpHqp5T6sw'},
        # )
        # if response.status_code == requests.codes.ok:
        #     with open('no-bg.png', 'wb') as out:
        #         out.write(response.content)
        # else:
        #     print("Error:", response.status_code, response.text)
        return

    def detect_bordder_of_object(self):

        image =  cv2.imread("no-bg.png")
        image =  cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        # cv2.imshow("test" , image)
        # cv2.waitKey(0)

        lap = cv2.Laplacian(image, cv2.CV_64F)
        lap = np.uint8(np.absolute(lap))

        sobelX = cv2.Sobel(image, cv2.CV_64F, 1, 0)
        sobelY = cv2.Sobel(image, cv2.CV_64F, 0, 1)
        sobelX = np.uint8(np.absolute(sobelX))
        sobelY = np.uint8(np.absolute(sobelY))
        sobelCombined = cv2.bitwise_or(sobelX, sobelY)

        titles = ['Original Image', 'Combined',
                  'Sobel X', 'Sobel Y']
        images = [image, sobelCombined, sobelX, sobelY]

        return

    def Canny_Edge(self ,  src):
        # image = cv2.imread("image/steelshapeC3.png")
        # image = cv2.imread("C:/Users/pc/PycharmProjects/Thesis/Detect_with_yolo/nobackground/no-bg_1.png")
        image =  cv2.imread(src)
        image = cv2.imread("308129922_2243671462458093_8150599188767817903_n-removebg-preview.png")


        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # cv2.imshow("test" ,  image)
        lap = cv2.Laplacian(image, cv2.CV_64F)
        canny = cv2.Canny(blurred, 30, 300)
        plt.imshow(self.fixColor(canny))
        plt.show()

        lines = cv2.HoughLines(canny, 1, np.pi / 180, 150, None, 0, 0)


        (cnts, hierarchy ) = cv2.findContours(canny.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        coins = image.copy()
        thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        self.list_point =  cnts[0]
        self.detach_contours(thresh)

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_NONE)

        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        cv2.boundingRect(cnts[0])

        # object.detect_Circle(image)


        plt.imshow(self.fixColor(canny))

        plt.imshow(self.fixColor(coins))

        self.draw_Point(cnts)
        plt.show()
    def haris(self  , img):
        blob = img
        cv2.circle(blob, (380, 120), 25, 0, cv2.FILLED)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        corners = cv2.goodFeaturesToTrack(gray, 300, 0.07, 20)

        for corner in corners:

            x, y = corner[0]
            x = int(x)
            y = int(y)
            cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (200, 150, 200), -1)
            self.corner_list.append([x,y])

        cv2.imshow("goodFeaturesToTrack Corner Detection", img)
        cv2.waitKey()
        cv2.destroyAllWindows()


    def detect_Circle(self , image):
        src_img = image

        output = image.copy()
        list = []

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        max_radius = 30

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                                      param1=50, param2=30, minRadius=0, maxRadius=30)
        if circles is not None:

            circles = np.round(circles[0, :]).astype("int")

            for (x, y, r) in circles:

                if(r <= max_radius ) :
                    self.list_circle.append([x,y,r])
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            cv2.imshow("output", np.hstack([image, output]))

            cv2.waitKey(0)
            return circles
    def detach_contours(self , image):
        blob =image
        cv2.circle(blob, (380, 120), 25, 0, cv2.FILLED)
        contours, hier = cv2.findContours(blob, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        colors = [(255, 255, 0), (0, 255, 255), (255, 0, 255)]

        blob_idx = np.squeeze(np.where(hier[0, :, 3] == -1))

        blob_imgs = []

        k = 0
        for b_idx in np.nditer(blob_idx):
            blob_cnts = [contours[b_idx]]
            cnt_idx = np.squeeze(np.where(hier[0, :, 3] == b_idx))
            if (cnt_idx.size > 0):
                blob_cnts.extend([contours[c_idx] for c_idx in np.nditer(cnt_idx)])

            img = np.zeros((blob.shape[0], blob.shape[1], 3), np.uint8)
            cv2.drawContours(img, blob_cnts, -1, colors[k], 2)
            blob_imgs.append(img)
            k += 1
        k = 0
        for img in blob_imgs:
            cv2.imshow(str(k), img)

            self.haris(img)

            cv2.imshow("detectedLines", image)
            cv2.waitKey(0)

            k += 1
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def fixColor(self, image):
         return(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    def draw_Point(self, list_point):
        list_x = []
        list_y = []
        list_point_1 = []
        list_point_1_4 = []
        for  i in list_point[0] :
            list_temp = [ i[0][0], i[0][1]]
            list_point_1.append(list_temp)

        x_list = [x for [x, y] in list_point_1]
        y_list = [y for [x, y] in list_point_1]
        self.LIST_POint =  list_point_1


if __name__ == '__main__':
   src = " "
   Detect_not_circle =  Al.Algro()
   object = Detect_Shape_C()

   object.setPath("D:\Shape_Steel_C_3.png")
   # object.getcoordinate_from_API()
   # object.Draw_rectangel_in_image()
   object.Remove_bg()

   object.Canny_Edge(src)

   Detect_not_circle.set_List_Point(object.get_LIST_POINT())
   Detect_not_circle.Set_circle_list(object.list_circle)
   Detect_not_circle.using_corner(object.get_corner_list(), object.getlist_point())

   Detect_not_circle.border_only()
   mesing_class = Meshing.Meshing()
   mesing_class.Set_Hastable_Segment(Detect_not_circle.get_Hash())
   mesing_class.processing_point()
   # mesing_class.scale(0,600)
   # mesing_class.scale_process(0 ,600  , mesing_class.get_point_scale())
   # mesing_class.draw_model()

   # mesing_class.scale_process()


   # print(threading.Thread.name)
   #
   # x = threading.Thread(target=mesing_class.input)
   # x.start()

   # print(threading.Thread.getName(x))
   mesing_class.Draw_model()
   mesing_class.Messing_2()



   # mesing_class.input()

   # mesing_class.Cal_displayment.Preprocessing()
   #
   # mesing_class.Cal_displayment.Cal_Displace()









