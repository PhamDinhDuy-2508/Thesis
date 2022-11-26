import copy
import math
from collections import defaultdict

import numpy as np
from mpmath import arange
from scipy.optimize import curve_fit
from sympy.abc import x, y, z, a, b
from sympy import solve, Poly, Eq, Function, exp, symbols
from sympy import *
from sympy.physics.quantum.circuitplot import pyplot


class Filter :

    def __init__(self ,  list_point_real , list_point_filter , key_point):
        self.line_area = None
        self.list_point_real = list_point_real
        self.list_point_filter = list_point_filter
        self.result = []
        self.key_point =  key_point
        self.step_stack = []
        self.line_key_value ={}
        self.step_position_change=[]
        self.step_stack_curve= defaultdict(lambda : set())
        self.curve_list =[]
        self.key_filter ={}
        self.x_curve=[]
        self.y_curve =[]
        self.list_curve_x = []
        self.list_curve_y = []
        self.max_list_point = []
        self.list_key = []
        self.step_stack_end_Curve=[]
        self.Curve_List =[]
        self.Curve_Area = []

    def get_result(self):
        return self.result
    def get_curve_list(self):
        pass

    def get_curve(self):
        return self.curve_list


    def Smooth_Line(self):
        # print("smooth" , self.list_point_filter)
        for i in range(1 , self.list_point_filter.__len__()):
            if(abs(self.list_point_filter[i][0] - self.list_point_filter[i-1][0]) <4 ) :
                self.list_point_filter[i][0]  = self.list_point_filter[i - 1][0]
            elif (abs(self.list_point_filter[i][1] - self.list_point_filter[i - 1][1]) < 4):
                    self.list_point_filter[i][1] = self.list_point_filter[i - 1][1]
        self.result = self.list_point_filter
        self.list_key =  list(self.key_point.keys())
        list_point = []

        for k  in  range( 1 , self.list_key .__len__()) :
            key1 =   self.list_key [k-1]
            key2 =   self.list_key [k]

            # print(key1 , key2)
            for j in range(self.key_point.get(key1), self.key_point.get(key2) + 1):
                x = self.list_point_real[j][0]
                y = self.list_point_real[j][1]

                list_point.append(self.list_point_real[j])
                # list_distance_arr.append(abs(np.cross(P2 - P1, P3 - P1) / np.linalg.norm(P2 - P1)))
            if(list_point.__len__() != 0) :
                if(self.Line_Fitting(list_point) == True) :
                    # print(key1 , key2 ,  "Line")
                    pass
                else :
                    pass
                self.Curve_List.append(list_point)
                # self.curve_detect(list_point , back_point)

            list_point = []
        self.Curve_detect_2(self.list_point_filter)

        # print("list key" ,   self.list_key )

        # if(self.curve_list.__len__() != 0 ) :
        #     self.Connect_curve(self.curve_list)
    def get_Curve(self):
        return self.curve_list


    def Curve_detect_2(self ,  _list):
        print("FILTER " , _list)
        stack = []
        point = []
        i = 0
        step_Angle = []


        while i < _list.__len__()-1 :

            point = [_list[i-1] , _list[i] , _list[i+1]]
            vector1 = [abs(point[0][0] - point[1][0]), abs(point[0][1] - point[1][1])]
            vector2 = [abs(point[1][0] - point[2][0]), abs(point[1][1] - point[2][1])]

            angle3 = (vector1[0] * vector2[0] + vector1[1] * vector2[1]) / (
                        math.sqrt(math.pow(vector1[0], 2) + math.pow(vector1[1], 2)) * math.sqrt(
                    math.pow(vector2[0], 2) + math.pow(vector2[1], 2)))
            print(point , math.degrees(math.acos(angle3)))
            if(angle3 > 1) :
                angle3 = 1
            if(math.degrees(math.acos(angle3)) < 50) :

                    if(math.degrees(math.acos(angle3)) >50 ) :
                        if(stack.__len__()!=0) :
                            if(stack[stack.__len__()-1][0] == "Curve" and stack.__len__() != 0 ) :
                                stack.append(["Curve", stack[stack.__len__() - 1][2], point[1]])

                        stack.append(['Line' , point[0], point[1]])
                    elif( math.degrees(math.acos(angle3)) > 2 and abs( point[0][0] -point[1][0] ) < 60 and abs( point[0][1] -point[1][1] ) < 60 ):
                        if (stack.__len__() != 0):
                            if (stack[stack.__len__() - 1][0] == "Curve" and stack.__len__() != 0):
                                stack.append(["Curve", stack[stack.__len__() - 1][2], point[1]])

                        if(step_Angle.__len__()!=0) :
                            if (step_Angle[step_Angle.__len__() - 1] > 50):
                                stack.append(["Line", point[0], point[1]])
                            else:
                                if(abs( point[0][0] -point[1][0] ) < 60 and abs( point[0][1] -point[1][1] ) < 60) :

                                    stack.append(["Curve", point[0], point[1]])
                                else :
                                    stack.append(["Line", point[0], point[1]])
                    else :
                        stack.append(["Line", point[0], point[1]])

                    i=i+1


            else :
                if (stack.__len__() != 0):
                    if (stack[stack.__len__() - 1][0] == "Curve" ):
                        if (abs(point[0][0] - point[1][0]) < 60 and abs(point[0][1] - point[1][1]) < 60):
                            stack.append(["Curve", point[0], point[1]])

                stack.append(['Line' ,point[0], point[1]])
                i=i+1
            step_Angle.append(math.degrees(math.acos(angle3)))
        print(stack)

        self.Connect_Curve_2(stack)



        pass
    def get_angle_3_point(self , point):
        vector1 = [abs(point[0][0] - point[1][0]), abs(point[0][1] - point[1][1])]
        vector2 = [abs(point[1][0] - point[2][0]), abs(point[1][1] - point[2][1])]
        angle3 = (vector1[0] * vector2[0] + vector1[1] * vector2[1]) / (math.sqrt(math.pow(vector1[0], 2) + math.pow(vector1[1], 2)) * math.sqrt(
            math.pow(vector2[0], 2) + math.pow(vector2[1], 2)))
        if(angle3 >1 ) :
            angle3 =1
        return  math.degrees(math.acos(angle3))

    def get_angle_3_point_NONE_ABS(self, point):
        vector1 = [(point[0][0] - point[1][0]), (point[0][1] - point[1][1])]
        vector2 = [(point[1][0] - point[2][0]), (point[1][1] - point[2][1])]
        angle3 = (vector1[0] * vector2[0] + vector1[1] * vector2[1]) / (
                    math.sqrt(math.pow(vector1[0], 2) + math.pow(vector1[1], 2)) * math.sqrt(
                math.pow(vector2[0], 2) + math.pow(vector2[1], 2)))
        if (angle3 > 1):
            angle3 = 1
        if (angle3 <- 1):
            angle3 = -1
        return math.degrees(math.acos(angle3))

    def Connect_Curve_2(self , stack):
        temp_stack = []
        i = 0
        result = list()
        Curvelist = []
        start_Curve = []

        temp_back = []
        temp_back_Point = []
        while (stack.__len__() != 0):
            if (start_Curve.__len__() != 0):
                back_point = start_Curve[start_Curve.__len__() - 1]

                x_width1 = back_point[0][0] - back_point[1][0]
                y_width1 = back_point[0][1] - back_point[1][1]
                x_width = back_point[1][0] - stack[0][2][0]
                y_width = back_point[1][1] - stack[0][2][1]
                # print(back_point, x_width1, y_width1, x_width, y_width)
            if (stack.__len__() == 1):
                    print("Final")

                    break

            if (stack[0][0] == "Line"):
                if(stack.__len__() > 2) :
                    if (stack[0][2][0] == stack[1][1][0] and stack[0][2][1] == stack[1][1][1]):
                        point = [stack[0][1], stack[0][2], stack[1][2]]
                    else:
                        point = [stack[0][1], stack[0][2], stack[1][1]]
                else :

                    break
                if(temp_back.__len__()!= 0 ) :
                    # print(temp_back[temp_stack.__len__() - 1], stack[0][0] , stack[1][0], stack[0])

                    if(temp_back[temp_back.__len__()-1] == "Curve" and stack[1][0] == "Curve") :
                        if (abs(stack[0][1][0] - stack[0][2][0]) < 80 and abs(stack[0][1][1] - stack[0][2][1]) < 80):

                            start_Curve.append([stack[0][1], stack[0][2]])
                        else :
                            temp_back.append(stack[0][0])
                            temp_back_Point.append([stack[0][1], stack[0][2]])
                            stack.pop(0)
                            continue

                    elif(temp_back[temp_back.__len__()-1] == "Curve" and stack[1][0] == "Line"):
                        if(stack[1][0] == "Line") :
                            angle  = self.get_angle_3_point(point)

                            if(angle < 48) :

                                if(abs(stack[0][1][0]-stack[0][2][0]) < 80 and abs(stack[0][1][1]-stack[0][2][1]) < 80 ) :

                                    stack[0][0] = "Curve"

                                    start_Curve.append([stack[0][1], stack[0][2]])
                        else :
                            point = [stack[0][1], stack[0][2], stack[1][2]]
                    elif (temp_back[temp_back.__len__() - 1] == "Line" and stack[1][0] == "Curve"):
                        if (stack[0][0] == "Line"):
                            angle = self.get_angle_3_point(point)

                            if (angle < 48):

                                if (abs(stack[0][1][0] - stack[0][2][0]) < 80 and abs(
                                        stack[0][1][1] - stack[0][2][1]) < 80):
                                    stack[0][0] = "Curve"

                                    start_Curve.append([stack[0][1], stack[0][2]])
                        else:
                            point = [stack[0][1], stack[0][2], stack[1][2]]


                    else :
                        if (abs(stack[0][1][0] - stack[0][2][0]) < 80 and abs(stack[0][1][1] - stack[0][2][1]) < 80):
                            if (start_Curve.__len__() != 0):
                                if(start_Curve.__len__() < 3 ) :
                                    result.append(["curve", start_Curve[0], start_Curve[0]])
                                    result.append(["curve", start_Curve[start_Curve.__len__() - 1],  start_Curve[start_Curve.__len__() - 1]])

                                else :
                                    result.append(["curve", start_Curve[0], start_Curve[start_Curve.__len__() - 1]])
                                start_Curve = []



            else:
                print("Line_Between", stack[0], abs(stack[0][1][0] - stack[0][2][0]),
                      abs(stack[0][1][1] - stack[0][2][1]))

                start_Curve.append([stack[0][1], stack[0][2]])

            temp_back.append(stack[0][0])
            temp_back_Point.append([stack[0][1] ,  stack[0][2]])
            stack.pop(0)

        print("Stack" , start_Curve)

        if(stack.__len__() == 2) :
             stack.pop(0)
        if (temp_back[temp_back.__len__() - 1] == "Curve"):

            if (start_Curve.__len__() == 0):
                p1 = result[result.__len__() - 1][2][0]
                p2 = result[result.__len__() - 1][2][1]
                p3 = stack[0][2]
                point = [p1, p2, p3]
                if (self.get_angle_3_point(point) < 50 and self.get_angle_3_point(point) > 3 ):
                    if (abs(p2[0] - stack[0][2][0]) < 60 and abs(p2[1] - stack[0][2][1]) < 60):
                        result[result.__len__() - 1][2] = [stack[0][1], stack[0][2]]
            else:
                p1 = start_Curve[start_Curve.__len__() - 1][0]
                p2 = start_Curve[start_Curve.__len__() - 1][1]
                p3 = stack[0][2]
                point = [p1, p2, p3]
                if (self.get_angle_3_point(point) < 50  ):
                    if (abs(p2[0] - stack[0][2][0]) < 60 and abs(p2[1] - stack[0][2][1]) < 60):
                        start_Curve[start_Curve.__len__() - 1] = [stack[0][1], stack[0][2]]
                result.append(["curve" , start_Curve[0], start_Curve[start_Curve.__len__() - 1]])
        if (start_Curve.__len__() != 0):

                result.append(["curve", start_Curve[0], start_Curve[start_Curve.__len__() - 1]])



        curve_list = []
        listkey = list( self.key_point.keys() )




        for j in range(result.__len__()):
            test = result[j][1][0]
            test2 =  result[j][2][1]


            if(self.key_point.get(tuple(test)) == None ) :
                for k in range (listkey.__len__()) :

                    if(abs(test[0] - listkey[k][0]) <= 4 and  abs(test[1] - listkey[k][1]) <= 4) :
                        test =  listkey[k]
                        break
            if (self.key_point.get(tuple(test2)) == None):
                    for k in range(listkey.__len__()):

                        if (abs(test2[0] - listkey[k][0]) <= 4 and abs(test2[1] - listkey[k][1]) <= 4):
                            test2 = listkey[k]
                            break
            curve_list.append(test)
            curve_list.append(test2)



        self.curve_list = self.check_Curve_Out_Curve_In(curve_list)
        self.Curve_Area =  self.check_Curve_Out_Curve_In(curve_list)

        # print("result", result)
    def get_Curve_Area(self):
        return self.Curve_Area
    def check_Curve_Out_Curve_In(self , result):
        res = []
        for j in range( 1, result.__len__(),2):
            hastable =  defaultdict(lambda :list())
            for i in range(self.key_point.get(tuple(result[j-1])), (self.key_point.get(tuple(result[j]))) + 1):
                point = self.list_point_real[i]
                hastable[self.distance_Point_line( result[j-1] ,result[j] , point )] = tuple( self.list_point_real[i] )
            liskey = list( hastable.keys() )
            max_distance =   hastable[max(liskey)]
            if(res.__len__()!=0) :
                if(res[res.__len__()-1][0][0] !=result[j-1][0] and  res[res.__len__()-1][0][1] !=result[j-1][1] ) :
                    res.append([result[j-1], max_distance , result[j] ])
            else :
                res.append([result[j - 1], max_distance, result[j]])

        point = [ self.list_point_filter[1] , self.list_point_filter[self.list_point_filter.__len__() - 1] , self.list_point_filter[self.list_point_filter.__len__() - 2]  ]
        if (res[0][0][0] == self.list_point_filter[0][0 ]and res[0][0][1] == self.list_point_filter[0][1]) :
            p = [self.list_point_filter[self.list_point_filter.__len__() - 2], self.list_point_filter[0] , self.list_point_filter[1]]
            print("Connect",p , self.get_angle_3_point(p))
            if(self.get_angle_3_point(p) < 15) :
                res[0][0] =self.list_point_filter[self.list_point_filter.__len__() - 2]

        print(res)
        self.Curve_fitting_2(res)


        return res
    def distance(self , a,c , x , y):
        return abs(a*x + -1*y +c) /math.sqrt(math.pow(a,2) + math.pow(-1 , 2))
    def distance_Point_line(self , Point1 , Point2 , Point3):
        P2 = np.array([Point2[0] , Point2[1]])
        P1 = np.array([Point1[0] , Point1[1]])
        P3 = np.array([Point3[0], Point3[1]])

        return abs(np.cross(P2 - P1, P3 - P1) / np.linalg.norm(P2 - P1))
    def get_xy_curve(self):

        return [self.x_curve , self.y_curve]
    def distance_2Point(self , Point1 , Point2):
        return math.dist(Point2 , Point1)

    def objective(self , x, a, b, c, d, e, f):
        return (a * x) + (b * x ** 2) + (c * x ** 3) + (d * x ** 4) + (e * x ** 5) + f

    def Curve_fitting_2(self , list):
        result_x = []
        result_y = []
        signal = True
        start = []
        end = []



        for j in range(list.__len__()) :
            y_res = []
            x1 = []
            y1 = []
            start.append(list[j][0])
            end.append(list[j][2])

            if(self.key_point.get(tuple(list[j][0]))  > self.key_point.get(tuple(list[j][2]))+1) :
                for i in range(-1, self.key_point.get(tuple(list[j][2])) + 1):
                    x1.append(self.list_point_real[i][0])
                    y1.append(self.list_point_real[i][1])
            else :
                for i in range(self.key_point.get(tuple(list[j][0])) ,self.key_point.get(tuple(list[j][2]))+1) :
                    x1.append(self.list_point_real[i][0])
                    y1.append(self.list_point_real[i][1])

            #
            if(  list[j][0][0] > list[j][1][0] and list[j][1][0]  < list[j][2][0]) :
                    temp = y1
                    y1 =  x1
                    x1 =  temp

                    signal =  False
            popt, _ = curve_fit(self.objective, x1, y1)
            #
            a, b, c, d, e, f = popt

            # y_res = []
            for k in range(x1.__len__()):
                    x1_ = x1[k]
                    t = float (e*math.pow(x1_ , 5))
                    t4 = float(d* math.pow(x1_, 4))
                    test = (a * x1_) + (b * x1_ ** 2) + (c * x1_ ** 3) + t4 + t + f

                    y_res.append(test)

            if(signal ==  False) :
                    y_res.insert(0, list[j][0][0])
                    x1.insert(0 , list[j][0][1])
                    y_res.append( list[j][2][0])
                    x1.append( list[j][2][1])
                    result_x.append(y_res)
                    result_y.append(x1)


                    signal =  True
            else :
                    y_res.insert(0, list[j][0][1])
                    x1.insert(0, list[j][0][0])
                    y_res.append(list[j][2][1])
                    x1.append(list[j][2][0])
                    result_x.append(x1)
                    result_y.append(y_res)


        self.x_curve  =  result_x
        self.y_curve =  result_y


        self.Filter(  result_x , result_y)
    def get_x_curve(self):
        return self.x_curve
    def get_y_curve(self):
        return self.y_curve
    def Filter2(self, start , end , resultx , reslty):
        Hashtable = defaultdict(lambda  : list())
        i  =1
        while i  < self.result.__len__() :
            if(self.result[i-1][1] == start[i-1][1] and  self.result[i-1][0] == start[i-1][0]) :
                Hashtable["Curve"]  = [resultx ,  reslty]

    def Objective_line(self , x ,  a,b):
        return  a*x + b



    def shortest_distance(x1, y1, a, b, c):

        d = abs((a * x1 + b * y1 + c)) / (math.sqrt(a * a + b * b))
        print("Perpendicular distance is", d)
    def Line_Fitting(self ,List):
        x = []
        y = []
        for i in range(List.__len__()) :
            x.append(List[i][0])
            y.append(List[i][1])

        popt, _ = curve_fit(self.Objective_line, x, y)

        print(x)
        print(y)
        # summarize the parameter values
        a, b = popt
        # print('y = %.5f * x + %.5f' % (a, b))
        # plot input vs output
        # define a sequence of inputs between the smallest and largest known inputs


        Point_In_Line = []
        P1 = np.array([x[0], y[0]])
        P2 = np.array([x[x.__len__() - 1], y[x.__len__() - 1]])
        for i in range(1, x.__len__() - 1):
            x_Corr = x[i]
            y_Corr = y[i]
            P3 = np.array([x_Corr, y_Corr])
            # d = shortest_distance(x_Corr, y_Corr, a, -1, b)
            d = abs(np.cross(P2 - P1, P3 - P1) / np.linalg.norm(P2 - P1))

            if (d <= 1):
                Point_In_Line.append([x_Corr, y_Corr])
        if (Point_In_Line.__len__() > 0.5 * x.__len__()):
            return True
        else:
            return False


    def  Filter(self , curve_x  , curve_y):

        lis_segment =  copy.deepcopy(self.result)
        lis_segment_temp =  copy.deepcopy(self.result)

        list_curve_x =  copy.deepcopy(curve_x)
        lis_curve_y  =  copy.deepcopy(curve_y)
        result_position = []
        stack = []
        count = 0
        curve_pos = []
        Line_result =[]

        Hashtable = defaultdict(lambda : list())
        for i in range(list_curve_x.__len__()) :

                curve_pos_start = [list_curve_x[i][0] , lis_curve_y[i][0]]
                curve_pos_end =  [list_curve_x[i][list_curve_x[i].__len__()-1] , lis_curve_y[i][lis_curve_y[i].__len__()-1]]
                count = self.delete_line_in_curve(count , curve_pos_start  ,lis_segment)
                result_position.append(count)
                count = self.delete_line_in_curve(count , curve_pos_end ,  lis_segment)
                result_position.append(count)
        i = 1
        while (i < lis_segment_temp.__len__()) :


            if(result_position.__len__() == 0 ) :
                Hashtable[tuple(lis_segment_temp[i-1])] = ["Line" ,  tuple(lis_segment_temp[i-1]) ,tuple (lis_segment_temp[i])]
                i+=1
            elif (i-1 != result_position[0] and result_position.__len__() != 0):
                Hashtable[tuple(lis_segment_temp[i - 1])] = ["Line", lis_segment_temp[i - 1],
                                                             lis_segment_temp[i]]
                i+=1

            else :

                lis_segment_temp[i-1][0] =      list_curve_x[0][0]
                lis_segment_temp[i - 1][1] =  lis_curve_y[0][0]

                Hashtable[tuple(lis_segment_temp[i-1])] =  ["Curve" , list_curve_x[0] , lis_curve_y[0]]
                if(result_position[1] == None) :
                    i = i+1
                else :
                    i =  result_position[1] +1
                # list_curve_x[0][list_curve_x.__len__()-1] = lis_segment_temp[i ][0]
                # lis_curve_y[0][lis_curve_y.__len__()-1] = lis_segment_temp[i][1]
                list_curve_x.pop(0)
                lis_curve_y.pop(0)
                result_position.pop(0)
                result_position.pop(0)

        self.line_area =  Hashtable
        # print(Hashtable)
        # print(Hashtable)
    def Curve_fiter(self):
        list_key =  list( self.line_area.keys() )
        curve_Area = []

        for i in range(1 , list_key.__len__())  :
            if(self.line_area.get(list_key[i])[0] == "Curve" or self.line_area.get(list_key[i])[0] == "curve" ) :

                temp = [self.line_area.get(list_key[i-2]) , self.line_area.get(list_key[i-1]) , self.line_area.get(list_key[i])]
                print(self.line_area.get(list_key[i-2])[1] , self.line_area.get(list_key[i-1])[2])
                curve_Area.append(temp)

                point_0 = self.line_area.get(list_key[i-2])[1]
                point_1 = self.line_area.get(list_key[i-2])[2]
                point_2 = self.line_area.get(list_key[i])[1]
                point_3  =self.line_area.get(list_key[i])[2]
                point = [point_0 , point_1 ,  point_2]
                if (self.get_angle_3_point_NONE_ABS(point) <= 87    and self.get_angle_3_point_NONE_ABS(point) > 10 ) :
                    self.line_area.get(list_key[i + 1])[1] = self.find_perpendicular("L" , point_1 , point_2 , point_3)
                    point_2 = self.line_area.get(list_key[i + 1])[1]
                    self.line_area.get(list_key[i])[1].append(point_2[0])
                    self.line_area.get(list_key[i])[2].append(point_2[1])
                elif(self.get_angle_3_point_NONE_ABS(point) >= 93     and self.get_angle_3_point_NONE_ABS(point) <170  ) :
                    print("L" , point_1 , point_2 ,  point_3)

                    self.line_area.get(list_key[i + 1])[1] = self.find_perpendicular("R", point_1,point_2 ,  point_3)
                    point_2 =  self.line_area.get(list_key[i + 1])[1]
                    self.line_area.get(list_key[i])[1].append(point_2[0])
                    self.line_area.get(list_key[i])[2].append(point_2[1])


                elif(abs(self.get_angle_3_point_NONE_ABS(point) - 0) < 10 or abs(self.get_angle_3_point_NONE_ABS(point) - 180) <10  ) :
                    pass
                else :
                    pass

    def find_perpendicular(self ,  signal ,  point1 ,  midpoint,  point2) :
        Hastable = defaultdict(lambda : list())
        start_position = 0
        listkey = list( self.key_point.keys() )
        start_position = self.key_point.get(tuple(midpoint))

        if (self.key_point.get(tuple(midpoint)) == None):
            for k in range(listkey.__len__()):
                if (abs(midpoint[0] - listkey[k][0]) <= 4 and abs(midpoint[1] - listkey[k][1]) <= 4):
                    point2 = listkey[k]
                    start_position = self.key_point.get(listkey[k])
                    break
        if(signal == "L") :
            p = [point1 , self.list_point_real[start_position] , point2]

            angle  = self.get_angle_3_point(p)

            while( abs(angle -  90) < 30) :
                p = [point1, self.list_point_real[start_position], point2]
                angle = self.get_angle_3_point(p)
                minus =  abs(angle -  90)
                Hastable[minus] = p

                start_position +=1
        elif (signal == "R"):
                p = [point1, self.list_point_real[start_position], point2]

                angle = self.get_angle_3_point(p)
                while (abs(angle - 90) < 30):
                    p = [point1, self.list_point_real[start_position], point2]
                    angle = self.get_angle_3_point(p)
                    minus = abs(angle - 90)

                    Hastable[minus] = p
                    start_position -= 1
        if(start_position == 0 ) :
            print("Something was wrong")

        lst = list(Hastable.keys())


        # print(min(lst) )
        # min_ = min(list(Hastable.keys()))
        p = Hastable.get(min(lst , default=None))
        if(p==None) :
            return midpoint

        return p[1]

        # print("find_perpendicular", self.get_angle_3_point(p), [point1, self.list_point_real[start_position], point2])

    def get_line_Area(self):
        return self.line_area
    def delete_line_in_curve(self ,  count , start , list_segment):
        try :
            for j  in range (count  ,list_segment.__len__()) :
                if (abs(start[0] - list_segment[j][0]) <= 4 and abs(start[1] - list_segment[j][1]) <= 4):
                    return j
                else :
                    continue
        except :
            pass
