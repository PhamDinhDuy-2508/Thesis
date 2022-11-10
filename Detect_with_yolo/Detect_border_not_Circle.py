import math
import matplotlib
from collections import defaultdict
import  Meshing


import  numpy as np

from scipy.special import binom
import math
import  copy
import Filter_Point as filter_point

import operator

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


class Algro :


    list_point = []
    queue_line = []
    const_lint = 0

    circle_list = []
    result =None
    real_list_point=[]


    def __init__(self):

        self.response_json = None
        self.key_val = None

        self.const_lint = 0

        self.begin_point =  None

        self.circle_list = []
        self.result = None
        self.curve = []
        self.corner = []
        self.area_curve_x=[]
        self.area_curve_y=[]
        self.area_curve=[]
        self.list_curve = []
        self.Hash = None





    def Set_circle_list(self , list):

        self.circle_list =  list

    def set_List_Point(self , lispoint):
        self.list_point = lispoint
        self.real_list_point = lispoint

    def draw_line_base_array_end_start_point(self , a,b,r):
        listx = []
        listy = []

        for i in range(self.queue_line.__len__()) :
          for j in range (0,2) :
              listx.append(float(self.queue_line[i][j][1]))
              listy.append(float(self.queue_line[i][j][0]))

        for i in range(0,listx.__len__()-1) :
            if(abs(listx[i] -  listx[i+1]) <=5) :
                listx[i] = listx[i+1]
            elif(abs(listy[i] -  listy[i+1])) :
                    listy[i] = listy[i+1]

        if(listx[listx.__len__()-1] -listx[0]- listx[0] < listy[listy.__len__()-1]-listy[0] ) :
            listx[listx.__len__()-1] = listx[0]
            endpoint = [listx[0] , listx[0]]
            listx.append(listx[0])
            listy.append(listy[0])
        else :
            listy[listy.__len__() - 1] = listx[0]
            listx.append(listx[0])
            listy.append(listy[0])


        points = np.array([listx, listy]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        cm = dict(zip(range(-1, 2, 1), list("rbgcmykw")))
        colors = list(map(cm.get, np.sign(np.diff(listy))))

        lc = LineCollection(segments, colors=colors, linewidths=2)
        fig, ax = plt.subplots(1,1)

        ax.add_collection(lc)

        ax.autoscale()
        ax.margins(0.1)
        plt.show()

    def uniqueish_color(selfm ,  size):

        return plt.cm.gist_ncar(np.random.random(size))



    def border_only(self):

        self.draw_2(self.list_point)

        return

        # ax.scatter(b, a, r, 'r')
        # ax.scatter(b, a, r, 'r')




    def angle(self , A, B, C):
        Ax, Ay = (A[0] - B[0]), (A[1] - B[1])
        Cx, Cy = (A[0] - C[0]), (A[1] - C[1])
        res = (Ax*Cx + Ay*Cy) /(math.sqrt(math.pow(Ax ,  2)  + math.pow(Ay,2))*math.sqrt(math.pow(Cx ,  2)  + math.pow(Cy,2)))


        return math.degrees(math.acos(res))

    def get_angle(self , p1, p2):  # These can also be four parameters instead of two arrays
        if(abs(p2[0]-p1[0]) <= 4) :
            return 90
        elif(abs(p1[1]-p2[1]) <= 4) :
            return 0
        else :
            angle =  math.atan2(p1[1] - p2[1], p1[0] - p2[0])

            # Optional
            angle = math.degrees(angle)

            # OR

            return angle

    def check_line_or_curve(self , list):
        list_temp =  []
        list_temp.append(list[0])

        for i in range(1 ,  list.__len__()) :
            if(i < list.__len__())  :
                    if(list_temp[list_temp.__len__()-1][0]!=list[i][0] and list_temp[list_temp.__len__()-1][1]!=list[i][1] ) :
                        list_temp.append(list[i])
                    elif (list_temp[list_temp.__len__()-1][0]==list[i][0]) :
                        list_temp[list_temp.__len__()-1][0] =  list[i][0]
                        continue
                    elif(list_temp[list_temp.__len__()-1][1]==list[i][1]) :
                        list_temp[list_temp.__len__()-1][1] =  list[i][1]
                        continue

                    else:
                        continue
            else :
                break
        result = {}
        start_point = list_temp[0]
        for i in range(1, list_temp.__len__()-1) :
            res_xy =  self.angle(list_temp[0] , list_temp[list_temp.__len__()-1] , list_temp[i])
            res_curve = self.angle(start_point , list_temp[list_temp.__len__()-1] , list_temp[i])

            if(res_xy <4) :
                result.__setitem__("xy" ,[list_temp[0] ,  list_temp[i]] )
            if(res_curve >4) :
                result.__setitem__("curve" ,[start_point ,  list_temp[i]] )
        if(self.angle(list_temp[0] , list_temp[list_temp.__len__()-1] , list_temp[list_temp.__len__()-2]) <5 ) :
            result.__setitem__("xy", [list_temp[0], list_temp[list_temp.__len__()-1]])
        else:
            result.__setitem__("curve", [start_point , list_temp[list_temp.__len__()-1]])



        print(result)



    def filter_corner(self , list_point_res):
        i = 0
        filter_point = []
        filter_result = []

        while (i+1 < list_point_res.__len__()) :
            Start_point = list_point_res[i]
            if(list_point_res[i][0] == list_point_res[i+1][0] and list_point_res[i][0] != 'xy' ) :
                for j in range(i+1 , list_point_res.__len__()) :
                    if(list_point_res[j][0] == Start_point[0]) :
                        filter_point.append(Start_point[1][0]) ,
                        filter_point.append( list_point_res[j][1][1])

                    else :
                        i=j+1
                        break
            else :
                filter_point.append(Start_point[1][0])
                filter_point.append(Start_point[1][1])

            i =  i+1



        return filter_point




    def process_corner(self , list ):
        step = []
        step_y=[]
        len = self.list_point.__len__()
        key_value = {}
        real_list_pont =  copy.deepcopy(self.list_point)
        print(real_list_pont.__len__())



        k = 0
        for i in range (0 , list.__len__()) :
            for j in range(0 , 6) :
                if abs(list[i][0] -  self.list_point[0][0]) <=2  and abs(list[i][1] - self.list_point[0][1]) <= 2 :
                    step.append(list[i])
                    key_value.__setitem__(tuple(self.list_point[j]), j)
                    break
            else:

                continue
        r_list = copy.deepcopy(list)
        j = 0
        while(j <  self.list_point.__len__() or list.__len__()!= 0  ) :
            for i in range(0, list.__len__()):
                if abs(list[i][0] - self.list_point[j][0]) <= 4 and abs(list[i][1] - self.list_point[j][1]) <= 4:
                    step.append(list[i])
                    key_value.__setitem__(tuple (list[i]) , j)
                    list.remove(list[i])
                    break
            j+=1


        x_number_list = []

        y_number_list = []
        f = open('bienbandau.txt', "w")

        for i in range(0, self.list_point.__len__()):
            self.Write_file(f, self.list_point[i][0], self.list_point[i][1])
        f.close()
        self.key_val =  key_value
        self.using_angle_corner(step , key_value)
        # res = self.line_process(step)
        self.list_point =  real_list_pont



        # self.compare_real_list_point(res,  key_value)

        # self.filter_corner_methode(res ,  key_value , res)
        text = []
        for i in range(0, step.__len__()):
            x_number_list.append(step[i][0])
            y_number_list.append(step[i][1])
            text.append(i)



        plt.scatter(x_number_list, y_number_list, s=10)
        for i, txt in enumerate(text):
            plt.annotate(txt, (x_number_list[i], y_number_list[i]))

        # Set chart title.
        plt.title("Danh sach cac diem dat biet ")

        plt.xlabel("")
        plt.ylabel("Diem")
        plt.show()

        return step
    def Write_file(self  ,   f , x , y):
        # f = open("demofile2.txt", "a")
        string  = str(x) + '\t' +str(y) +'\n'
        f.write(string )
    def usibng_key_value(self , start , end , key_value):
        value_check_x = {}
        value_check_y = {}
        if(start >0) :
            max_x_change = self.list_point[start][0]
            max_y_change =self.list_point[start][1]
            value_check_x.__setitem__(self.list_point[start][0]-max_x_change, 1)
            value_check_y.__setitem__(self.list_point[start][1]-max_y_change, 1)



        else :
            max_x_change = 0


        for i in range (start+1   , end+1) :
            if(end+1 > self.list_point.__len__()) :
                break
            devide_x = abs(self.list_point[i][0] - self.list_point[start][0])
            devide_y =  abs(self.list_point[i][1] -  self.list_point[start][1])
            if(value_check_x.get(devide_x) == None) :

                value_check_x.__setitem__(devide_x , 1)
            else :
                count  = value_check_x.get(devide_x)
                count+=1
                value_check_x.pop(devide_x)
                value_check_x.__setitem__(devide_x, count)

            if (value_check_y.get(devide_y) == None):
                value_check_y.__setitem__(devide_y, 1)
            else:

                count = value_check_y.get(devide_y)

                count += 1
                value_check_y.pop(devide_y)

                value_check_y.__setitem__(devide_y, count)


        key_x = list(value_check_x.keys())
        key_y = list(value_check_y.keys())

        x = list(value_check_x.values())
        y = list(value_check_y.values())
        max_x = key_x[x.index(max(x))]
        max_y = key_y[y.index(max(y))]        


        return [max_x , max_y]

    def using_angle_corner(self , point_ ,  key_value):
        i = 0
        point =  copy.deepcopy(point_)
        point_result = []

        self.Corner_CompareaTo_real_point()
        point = self.Corner_CompareaTo_real_point()
        while(i  < point.__len__()-1) :
            start = i
            left = i + 1
            right =  i -1

            left_vector = [abs(point[start][0]  - point[left][0]) ,  abs( point[start][1]-point[left][1])]

            right_vector =  [abs(point[start][0]  - point[right][0]) ,  abs( point[start][1]-point[right][1])]
            vector1 =   [abs(point[right][0]  - point[start][0]) ,  abs( point[right][1]-point[start][1])]
            vector2 =   [abs(point[right][0]  - point[left][0]) ,  abs( point[right][1]-point[left][1])]



            start_point =  point[left]

            mid_point =  point[start]

            end_point =  point[right]

            angle2 = ( right_vector[0]*left_vector[0] +  right_vector[1]*left_vector[1]) / (math.sqrt(math.pow( right_vector[0], 2) + math.pow( right_vector[1], 2)) * math.sqrt(math.pow(left_vector[0], 2) + math.pow(left_vector[1], 2)))
            angle3 = ( vector1[0]*vector2[0] +  vector1[1]*vector2[1]) / (math.sqrt(math.pow( vector1[0], 2) + math.pow( vector1[1], 2)) * math.sqrt(math.pow(vector2[0], 2) + math.pow(vector2[1], 2)))
            if(angle3 > 1) :
                angle3 =  1

            # print(abs(math.degrees(math.acos(angle3))) ,vector1 , vector2 , start_point  , mid_point , end_point)
            angle2 = round(angle2,2)

            if (abs(math.degrees(math.acos(angle2))) ) > 1:
                point_result.append(mid_point)

            if (point_result.__len__() == 0):
                point_result.append(mid_point)

            i = i+1
        test_vec = [0, 1]
        test_vec2 = [1, 0]
        angle_test = (test_vec[0] * test_vec2[0] + test_vec[1] * test_vec2[1]) / (
                    math.sqrt(math.pow(test_vec[0], 2) + math.pow(test_vec[1], 2)) * math.sqrt(
                math.pow(test_vec2[0], 2) + math.pow(test_vec2[1], 2)))

        point_result.append( point[point.__len__()-1])


        start = point_result.__len__()-1
        left =  0
        right =point_result.__len__()-2


        start_point = point_result[left]

        mid_point = point_result[start]

        end_point = point_result[right]


        vector1 = [abs(end_point[0] -mid_point[0]), abs(end_point[1] - mid_point[1])]
        vector2 = [abs(end_point[0] - start_point[0]), abs(end_point[1] - start_point[1])]
        angle3 = (vector1[0] * vector2[0] + vector1[1] * vector2[1]) / (
                    math.sqrt(math.pow(vector1[0], 2) + math.pow(vector1[1], 2)) * math.sqrt(
                math.pow(vector2[0], 2) + math.pow(vector2[1], 2)))

        if (angle3 > 1):
            angle3 = 1
        angle2 = round(angle3 , 2)
        # print(angle2)


        if(math.degrees(math.acos(angle3)) <10) :
            point_result.remove(mid_point)
            point_result.append(start_point)
        else :
            point_result.append(start_point)


        tem_dict = {}

        for i in range( 1, point_result.__len__()) :
            try :
                start = 0
                end = 0
                if tuple(point_result[i-1]) in self.key_val:
                    start  = list(self.key_val).index(tuple(point_result[i-1]))
                if tuple(point_result[i]) in self.key_val :
                    end =  list(self.key_val).index(tuple(point_result[i]))
                range_ =  abs(start-end)
                tem_dict.__setitem__(tuple(point_result[i-1]) , self.key_val.get(tuple(point_result[i-1])))

            except :
                 pass


        f = open('bientho.txt', "w")

        for i in range(0, point_result.__len__()):
            self.Write_file(f, point_result[i][0], point_result[i][1])
        f.close()

        object =  filter_point.Filter(self.list_point ,point_result , tem_dict)
        object.Smooth_Line()
        self.list_curve =  object.get_Curve()


        list_curve_x = object.get_xy_curve() [0]
        list_curve_y = object.get_xy_curve() [1]

        for i in range (list_curve_x.__len__()) :

            self.area_curve.append(list_curve_x[i])
            self.area_curve.append(list_curve_y[i])
        # print(self.area_curve.__len__())


        res = object.get_result()
        # print("final_res" , res)
        self.draw(res)
        self.curve =  object.get_Curve()
        self.Hash = object.get_line_Area()
        print("Hash" , self.Hash)
        object.Curve_fiter()

        # mesing_class =  Meshing.Meshing()
        # mesing_class.Set_Hastable_Segment(self.Hash)
        # mesing_class.Messing_2()


        self.draw_3(self.Hash)

        f = open('bienhoanchinh.txt', "w")
        # mesing_class.Set_Lisegment(point_result)
        # mesing_class.Meshing_Process()
        self.draw(res)


        for i in range(0, res.__len__()):
            self.Write_file(f, res[i][0], res[i][1])
        f.close()


        # self.draw(point_result)

    def compare_real_list_point(self , point_res ,  key_value):

        for i in range(point_res.__len__()-1) :
            if(point_res[i][0] != point_res[i+1][0] and point_res[i][1] != point_res[i+1][1] ) :
                start = key_value.get(tuple(point_res[i]))
                end = key_value.get(tuple(point_res[i+1]))
                if(start >= end) :
                    continue
                # print(self.usibng_key_value(start , end , key_value))
        # for i in range(45 , 51):
            # print(self.list_point[i])
        return


    def line_process(self  , list):


        start_point = list[0]
        result = []
        point_res = []
        temp_res = []
        step_angle = []
        temp_res.append(start_point )
        temp_res.append(list[1])
        base_vector = [start_point[0] -  list[1][0] , start_point[1] -  list[1][1] ]

        for  i in range(1 ,list.__len__()) :

            x1 =  list[i][0]
            x2 =  start_point[0]
            y1 =  list[i][1]
            y2 =  start_point[1]
            pressent_vector = [abs(x2-x1) ,  abs(y2-y1)]

            angle = (x1*x2 + y1*y2) / (math.sqrt(math.pow(x1, 2) + math.pow(y1, 2)) * math.sqrt(math.pow(x2, 2) + math.pow(y2, 2)))
            angle1 = (pressent_vector[0]*base_vector[0] + pressent_vector[1]*base_vector[1]) / (math.sqrt(math.pow(pressent_vector[0], 2) + math.pow(pressent_vector[1], 2)) * math.sqrt(math.pow(base_vector[0], 2) + math.pow(base_vector[1], 2)))
            angle2 = (x2*base_vector[0] + y2*base_vector[1]) / (math.sqrt(math.pow(x2, 2) + math.pow(y2, 2)) * math.sqrt(math.pow(base_vector[0], 2) + math.pow(base_vector[1], 2)))
            angle2 = (x2*base_vector[0] + y2*base_vector[1]) / (math.sqrt(math.pow(x2, 2) + math.pow(y2, 2)) * math.sqrt(math.pow(base_vector[0], 2) + math.pow(base_vector[1], 2)))


            if(step_angle.__len__() ==0):
                step_angle.append(math.degrees(math.acos(angle1)))
                continue

            if(abs(math.degrees(math.acos(angle1))  - step_angle[step_angle.__len__()-1] )) <= 7:

                    temp_res.append(list[i])
                    start_point = list[i-1]

            else :
                if(temp_res.__len__() >1) :
                    start_point =list[i-1]
                else :
                    start_point =list[i-1]

                if(abs(temp_res[0][0] -temp_res[temp_res.__len__() - 1][0]) <=7and abs(temp_res[0][1] -temp_res[temp_res.__len__() - 1][1]) >7 ) :
                    result.append(['x' , [temp_res[0], temp_res[temp_res.__len__() - 1]]])
                elif (abs(temp_res[0][0] - temp_res[temp_res.__len__() - 1][0]) > 7 and abs(
                        temp_res[0][1] - temp_res[temp_res.__len__() - 1][1]) <= 7):
                    result.append(['y' , [temp_res[0], temp_res[temp_res.__len__() - 1]]])
                else :
                    result.append(['xy' , [temp_res[0], temp_res[temp_res.__len__() - 1]]])

                point_res.append(temp_res[0])
                point_res.append(temp_res[temp_res.__len__() - 1])
                base_vector = [abs(start_point[0] - list[i][0]), abs(start_point[1] - list[i][1])]
                temp_res.clear()
                temp_res.append(list[i - 1])
                temp_res.append(list[i])
                i = i+1
                if( i+1 > list.__len__()) :
                    break
                x1 = list[i][0]
                x2 = list[i-1][0]
                y1 = list[i][1]
                y2 = list[i-1][1]
                pressent_vector = [abs(x2 - x1), abs(y2 - y1)]


                angle1 = (pressent_vector[0] * base_vector[0] + pressent_vector[1] * base_vector[1]) / (
                            math.sqrt(math.pow(pressent_vector[0], 2) + math.pow(pressent_vector[1], 2)) * math.sqrt(
                        math.pow(base_vector[0], 2) + math.pow(base_vector[1], 2)))
                step_angle.append(math.degrees(math.acos(angle1)))

        if (abs(temp_res[0][0] - temp_res[temp_res.__len__() - 1][0]) <= 8 and abs(
                temp_res[0][1] - temp_res[temp_res.__len__() - 1][1]) > 8):
            result.append(['x', [temp_res[0], temp_res[temp_res.__len__() - 1]]])
        elif (abs(temp_res[0][0] - temp_res[temp_res.__len__() - 1][0]) > 8 and abs(
                temp_res[0][1] - temp_res[temp_res.__len__() - 1][1]) <= 8):
            result.append(['y', [temp_res[0], temp_res[temp_res.__len__() - 1]]])
        else:
            result.append(['xy', [temp_res[0], temp_res[temp_res.__len__() - 1]]])


        point_res.append(result[result.__len__()-1][1][1])
        point_res.append(temp_res[0])
        point_res.append(temp_res[temp_res.__len__()-1])
        point_res.append(list[0])

        temp_res = result[result.__len__()-1]
        # result.remove( result[result.__len__()-1])
        if(abs(temp_res[1][1][1] - list[0][1]) <=6 and abs(temp_res[1][0][1] - list[0][1]) <=6 ):
            temp_res[1][0] = result[result.__len__()-2][1][1]
            temp_res[1][0][1] = list[0][1]
            temp_res[1][1] = list[0]

        self.result = result

        self.draw(      point_res)
        return result

    def using_corner(self ,  corner , list_point):

        list_point = []
        self.corner = copy.deepcopy(corner)


        for i in range( 0 , self.list_point.__len__() ,  4)  :
            list_point.append(self.list_point[i])


        self.list_point =  list_point

        sort_by_x =  sorted(corner, key=lambda k: [k[0], k[1]])
        sort_by_y =  sorted(corner, key=lambda k: [k[1], k[0]])

        step = self.process_corner(corner)

        x_number_list = []

        # y axis value list.
        y_number_list = []
        text = []
        for i in range(0 , step.__len__()) :
            x_number_list.append(step[i][0])
            y_number_list.append(step[i][1])
            text .append(i)

        plt.scatter(x_number_list, y_number_list, s=10)
        for i, txt in enumerate(text):
            plt.annotate(txt, (x_number_list[i], y_number_list[i]))

        # Set chart title.
        plt.title("E ")
        plt.xlabel("")
        plt.ylabel("ExtraNumber")
        plt.show()
    def draw_3(self ,  hash):
        fig, ax = plt.subplots()

        try :
            keys =  list(hash.keys())
            for i in range(keys.__len__()) :

                temp  = hash.get( keys[i])
                if(temp[0] == "Line" ) :
                    x_val = [temp[1][0], temp[2][0]]
                    y_val = [temp[1][1], temp[2][1]]
                    # print(x_val , y_val)
                    plt.plot(x_val, y_val)
                    plt.scatter(x_val, y_val, s=10, color='black')


                else :
                    x_val = temp[1]
                    y_val = temp[2]
                    print(x_val , y_val)
                    plt.plot(x_val, y_val , linewidth = 2)
            plt.autoscale(True, 'x' , None)
            plt.axis('scaled')

            plt.show()

        except : pass

    def bezier(self , points, num):
        N = len(points)
        t = np.linspace(0, 1, num=num)
        curve = np.zeros((num, 2))
        bernstein = lambda n, k, t: binom(n, k) * t ** k * (1. - t) ** (n - k)

        for i in range(N):
            curve += np.outer(bernstein(N - 1, i, t), points[i])
        return curve
    def draw(self , list_x_y):
        list_x = []
        list_y = []

        x_curve = []
        y_curve = []

        if(list_x_y.__len__()>100) :
            self.draw_2(list_x_y)
        else :
            for i in range(0, list_x_y.__len__()):
                list_x.append(list_x_y[i][0])

                list_y.append(list_x_y[i][1])

            while self.area_curve.__len__()!=0 :
                x=  self.area_curve[0]
                y =  self.area_curve[1]
                plt.plot(x,y , linewidth = 4)
                self.area_curve.pop(0)
                self.area_curve.pop(0)





            for i in range(0 ,list_x.__len__()-1) :

                x_val = [list_x[i], list_x[i+1]]

                y_val = [list_y[i], list_y[i+1]]



                if(x_curve.__len__()>0) :
                        x_curve.pop(0)
                if(y_curve.__len__()>0) :
                        y_curve.pop(0)


                plt.plot(x_val, y_val)
                plt.scatter(list_x, list_y, s=10, color='hotpink')
        plt.axis('scaled')

        plt.show()

    def draw_2(self , list_x_y):
        list_x = []
        list_y = []


        for i in range(0, list_x_y.__len__()):
            list_x.append(list_x_y[i][0])

            list_y.append(list_x_y[i][1])

        list_x.append(list_x_y[0][0])
        list_y.append(list_x_y[0][1])
        x_curve = []
        y_curve = []



        points = np.array([list_x, list_y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)


        cm = dict(zip(range(-1, 2, 1), list("rbgcmykw")))
        colors = list(map(cm.get, np.sign(np.diff(list_y))))
        lc = LineCollection(segments, colors='g', linewidths=2)



        fig, ax = plt.subplots(1, 1)
        plt.scatter(list_x, list_y, s=20 ,color = 'hotpink')


        ax.add_collection(lc)

        ax.autoscale()
        ax.margins(0.1)
        plt.axis('scaled')

        plt.show()




    def distance_2(self, Point1, Point2):
        x1 = Point1[0]
        x2 = Point2[0]
        y1 = Point1[1]
        y2 = Point2[1]
        return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

    def Corner_CompareaTo_real_point(self):
        res = []
        list = copy.deepcopy(self.list_point)
        key_val = copy.deepcopy(self.key_val)
        has_table = defaultdict(lambda: list())
        key = (key_val.keys())
        key_new = {}
        temp = defaultdict(lambda: list())


        len = key.__len__()
        for keys in key_val.keys():
            x = keys[0]
            y = keys[1]
            Point1 = [x, y]
            value_of_key = key_val.get(keys)
            has_table.clear()
            temp.clear()
            if (value_of_key + 2 < list.__len__()):
                for j in range(value_of_key - 2, value_of_key + 2):
                    Point2 = list[j]
                    has_table[self.distance_2(Point1, list[j])] = list[j]
                    temp[self.distance_2(Point1, list[j])] =  [list[j] , j]
                closset = min(has_table.keys())
                key_new.__setitem__(tuple(temp[min(temp.keys())][0]) ,temp[min(temp.keys())][1] )
                res.append(has_table[closset])
        self.key_val.clear()
        self.key_val =  key_new
        return res
    def get_Hash(self):
        return self.Hash

if __name__ == '__main__':
    al =  Algro()






