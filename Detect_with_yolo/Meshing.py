import copy
import math

import calfem.geometry as cfg
import calfem.mesh as cfm
import calfem.vis as cfv
from  collections  import  defaultdict

import numpy as np
import  Calulator

class Meshing :

    def __init__(self) -> None:

        super().__init__()
        self.list_surface = []
        self.List_segment = []
        self.Result = []
        self.g = cfg.Geometry()
        self.Curve_area = []
        self.Hastable_Segment = defaultdict(lambda : list)
        self.Segment_Area = []
        self.g2 =  cfg.Geometry()
        self.list_point = []

        self.list_spline = []
        self.surface = []

        self.Cal_displayment = Calulator.Calculator()


    def rotate_matrix(self , x, y, angle, x_shift=0, y_shift=0, units="DEGREES"):
        x = x - x_shift
        y = y - y_shift

        # Convert degrees to radians
        if units == "DEGREES":
            angle = math.radians(angle)

        # Rotation matrix multiplication to get rotated x & y
        xr = (x * math.cos(angle)) - (y * math.sin(angle)) + x_shift
        yr = (x * math.sin(angle)) + (y * math.cos(angle)) + y_shift

        return [xr, yr]

    def Set_Hastable_Segment (self , hash) :
        self.Hastable_Segment =  hash
        list_key =  list( self.Hastable_Segment.keys()  )
        for i in range(list_key.__len__()) :
            self.Segment_Area.append(self.Hastable_Segment.get(list_key[i]))

    def check_radius(self , mid_point , start_point , center_point):

        hastable =  defaultdict(lambda :list())
        radius_p1 = self.rotate_matrix(start_point[0] , start_point[1] ,  -90 , mid_point[0] , mid_point[1])
        radius_p2 =  self.rotate_matrix(start_point[0] , start_point[1] ,  90 , mid_point[0] , mid_point[1])
        if(math.dist(radius_p1 ,center_point) < math.dist(radius_p2,center_point)) :
            return radius_p1
        else :
            return  radius_p2
    def processing_point(self):
        self.Cal_displayment.Set_Segment_area(self.Segment_Area)

        list_Surface = []
        list_Spline = []
        list_poit = []
        list_Center_cirle = []
        list_point_cirle = []
        for i in range(self.Segment_Area.__len__()):
            if self.Segment_Area[i][0] == 'Line':

                if (list_poit.__len__() == 0):

                    list_poit.append(list(self.Segment_Area[i][1]))
                    list_poit.append(list(self.Segment_Area[i][2]))

                else:

                    list_poit.append(list(self.Segment_Area[i][2]))

            else:

                len_Curve = list(self.Segment_Area[i][1]).__len__()
                start = list(self.Segment_Area[i - 1][2])
                end = list(self.Segment_Area[i + 1][1])
                Center_Point = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
                mid_point = [self.Segment_Area[i][1][int(len_Curve / 2)], self.Segment_Area[i][2][int(len_Curve / 2)]]
                radius_point = self.check_radius(Center_Point, start, mid_point)
                list_Center_cirle.append(Center_Point)

                if (list_poit.__len__() == 0):
                    #

                    list_poit.append(list(start))
                    list_poit.append(list(radius_point))
                    list_poit.append(list(end))
                    list_point_cirle.append([list(start), list(radius_point)])
                    list_point_cirle.append([list(radius_point), list(end)])


                else:
                    #
                    #
                    list_poit.append(list(radius_point))
                    list_poit.append(list(end))
                    list_point_cirle.append([list(start), list(radius_point)])
                    list_point_cirle.append([list(radius_point), list(end)])

        lis_pos = []
        if (list_poit[0][0] == list_poit[list_poit.__len__() - 1][0] and list_poit[0][1] ==
                list_poit[list_poit.__len__() - 1][1]):
            list_poit.pop((list_poit.__len__() - 1))
        for i in range(list_poit.__len__()):
            self.g.point(list_poit[i])

        for i in range(list_Center_cirle.__len__()):
            lis_pos.append(list_poit.__len__() + i)
            lis_pos.append(list_poit.__len__() + i)

            self.g.point(list_Center_cirle[i])
        for i in range(list_poit.__len__()):
            list_Surface.append(i)

        for i in range(list_poit.__len__() - 1):
            if (list_point_cirle.__len__() != 0):
                if (list_poit[i][0] == list_point_cirle[0][0][0] and list_poit[i][1] == list_point_cirle[0][0][1]):
                    if (lis_pos.__len__() != 0):
                        self.g.circle([i, lis_pos[0], i + 1])
                        list_point_cirle.pop(0)
                        continue

            self.g.spline([i, i + 1])
        self.list_surface =  list_Surface

        self.g.spline([list_poit.__len__() - 1, 0])

        self.g.surface(list_Surface)
    def Draw_model(self):

        # self.g.surface(  self.list_surface, marker=self.mark_E2)
        cfv.drawGeometry(self.g)
        cfv.showAndWait()

    def Messing_2(self):
        # pass
        # self.Cal_displayment.Set_Segment_area(self.Segment_Area)
        #
        # list_Surface = []
        # list_Spline = []
        # list_poit = []
        # list_Center_cirle = []
        # list_point_cirle = []
        # for i in range(self.Segment_Area.__len__()) :
        #     if  self.Segment_Area[i][0] == 'Line' :
        #
        #         if (list_poit.__len__() == 0):
        #
        #             list_poit.append(list(self.Segment_Area[i][1]))
        #             list_poit.append(list(self.Segment_Area[i][2]))
        #
        #         else :
        #
        #             list_poit.append(list(self.Segment_Area[i][2]))
        #
        #     else :
        #
        #         len_Curve = list(self.Segment_Area[i][1]).__len__()
        #         start = list (self.Segment_Area[i-1][2])
        #         end =  list (self.Segment_Area[i+1][1])
        #         Center_Point =     [(start[0]+end[0])/2  , (start[1]+end[1])/2]
        #         mid_point =  [self.Segment_Area[i][1][int(len_Curve/2)] , self.Segment_Area[i][2][int(len_Curve/2)] ]
        #         radius_point =  self.check_radius(Center_Point , start,mid_point)
        #         list_Center_cirle.append(Center_Point)
        #
        #         if (list_poit.__len__() == 0):
        #             #
        #
        #             list_poit.append(list(start))
        #             list_poit.append(list(radius_point))
        #             list_poit.append(list(end))
        #             list_point_cirle.append([list(start) , list(radius_point)])
        #             list_point_cirle.append([list(radius_point) , list(end)])
        #
        #
        #         else :
        #             #
        #             #
        #             list_poit.append(list(radius_point))
        #             list_poit.append(list(end))
        #             list_point_cirle.append([list(start), list(radius_point)])
        #             list_point_cirle.append([list(radius_point), list(end)])
        #
        #
        #
        # lis_pos = []
        # if(list_poit[0][0] == list_poit[list_poit.__len__()-1][0] and list_poit[0][1] == list_poit[list_poit.__len__()-1][1] ):
        #     list_poit.pop((list_poit.__len__()-1))
        # for i in  range(list_poit.__len__()) :
        #     self.g.point(list_poit[i])
        #
        #
        # for i in range(list_Center_cirle.__len__()) :
        #
        #
        #     lis_pos.append(list_poit.__len__() +i)
        #     lis_pos.append(list_poit.__len__() +i)
        #
        #     self.g.point(list_Center_cirle[i])
        # for i in range(list_poit.__len__()):
        #     list_Surface.append(i)
        #
        #
        #
        #
        #
        # for i in range(  list_poit.__len__()-1) :
        #     if(list_point_cirle.__len__() != 0) :
        #         if(list_poit[i][0] == list_point_cirle[0][0][0] and list_poit[i][1] == list_point_cirle[0][0][1] ) :
        #             if(lis_pos.__len__() != 0 ) :
        #                 self.g.circle([i , lis_pos[0] , i+1])
        #                 list_point_cirle.pop(0)
        #                 continue
        #
        #
        #     self.g.spline([i, i+1])
        #
        # self.g.spline([ list_poit.__len__()-1 , 0 ])
        #
        # self.g.surface(list_Surface)

        self.Cal_displayment.Set_Fix(6)

        self.Cal_displayment.Set_Load(6e5, 1)

        self.Cal_displayment.Preprocessing()

        self.Cal_displayment.Cal_Displace()

        count = 0


        self.Messhing_Process()
    def Displacement(self):
        pass
    def Messhing_Process(self):
        mesh = cfm.GmshMesh(self.g)

        mesh.el_type = 2  # quad
        mesh.dofs_per_node = 2
        mesh.el_size_factor = 4

        coords, edof, dofs, bdofs, elementmarkers = mesh.create()

        cfv.figure()

        # Draw the mesh.

        cfv.draw_mesh(coords=coords, edof=edof, dofs_per_node=mesh.dofs_per_node, el_type=mesh.el_type, filled=True)
        cfv.showAndWait()

    def get_angle_3_point(self, point):
        vector1 = [abs(point[0][0] - point[1][0]), abs(point[0][1] - point[1][1])]
        vector2 = [abs(point[1][0] - point[2][0]), abs(point[1][1] - point[2][1])]
        angle3 = (vector1[0] * vector2[0] + vector1[1] * vector2[1]) / (
                    math.sqrt(math.pow(vector1[0], 2) + math.pow(vector1[1], 2)) * math.sqrt(
                math.pow(vector2[0], 2) + math.pow(vector2[1], 2)))
        if (angle3 > 1):
            angle3 = 1
        return math.degrees(math.acos(angle3))

    def Set_Curve_Area(self , curve_area):
        self.Curve_area =  curve_area

    def Set_Lisegment(self , list):
        self.List_segment =  copy.deepcopy(list )

    def rotate(self , points, origin, angle):
        z =  (points - origin) * np.exp(complex(0, angle)) + origin
        print(z.real , z.imag)
        return [z.real  , z.imag]

    def Rotate_Polygon(self , _list1):
        _list = copy.deepcopy(_list1)
        print(_list)
        vector1 = [  _list[-1][0] - _list[0][0]  ,  _list[-1][1] - _list[0][1]]
        vector2 = [ 0 ,  300]
        angle3_ra = ( vector1[0]*vector2[0] +  vector1[1]*vector2[1]) / (math.sqrt(math.pow( vector1[0], 2) + math.pow( vector1[1], 2)) * math.sqrt(math.pow(vector2[0], 2) + math.pow(vector2[1], 2)))
        if(angle3_ra >1 ) :
            angle3_ra = 1

        angle3 =  math.degrees(math.acos(angle3_ra))
        if(angle3 > 1) :

            start_Pont_x = _list[0][0]
            start_Pont_y =  _list[0][1]
            for i in range(1, _list.__len__()) :
                x=  _list[i][0]
                y =  _list[i][1]
                points = complex(x, y)
                origin = complex(start_Pont_x, start_Pont_y)

                angle = np.deg2rad(-angle3)

                _list[i] = self.rotate(points  ,origin, angle)
        return _list

    def Meshing_Process(self):
        list_Surface = []
        list_spline = []
        self.List_segment.pop(self.List_segment.__len__()-1)
        for i in range(self.List_segment.__len__()) :
            self.g.point([self.List_segment[i][0] , self.List_segment[i][1]])
            if(i+1 < self.List_segment.__len__()) :
                list_spline.append([i,i+1])
                self.g.spline([i ,  i+1])
            else :
                list_spline.append([i,0])
                self.g.spline([i , 0])
            list_Surface.append(i)
        self.g.surface(list_Surface)
        cfv.drawGeometry(self.g)

        cfv.showAndWait()

        mesh = cfm.GmshMesh(self.g)
        mesh.elType = 2  # Degrees of freedom per node.
        mesh.dofsPerNode = 5  # Factor that changes element sizes.
        mesh.elSizeFactor = 5  # Element size Factor
        coords, edof, dofs, bdofs, elementmarkers = mesh.create()
        cfv.figure()

        # Draw the mesh.

        cfv.drawMesh(
            coords=coords,
            edof=edof,
            dofs_per_node=mesh.dofsPerNode,
            el_type=mesh.elType,
            filled=True,
            title="Example 01"
        )
        cfv.showAndWait()
    def check(self):

        pass
