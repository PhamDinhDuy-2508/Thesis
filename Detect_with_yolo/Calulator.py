import copy
import math

import calfem.core as cfc
import calfem.geometry as cfg
import calfem.mesh as cfm
import calfem.vis_mpl as cfv2
import calfem.vis as cfv

import calfem.utils as cfu
import numpy as np

from scipy.sparse import lil_matrix

from  collections  import  defaultdict

import numpy as np
class Calculator :
    mark_E1 = 55
    mark_E2 = 66
    mark_fixed = 70
    mark_load = 90
    def __init__(self )  :

        self.Lis_Point = []
        self.surface = []
        self.spline = []
        self.Force  = 0
        self.t = 0
        self.v = 0
        self.ptype = 1
        self.fix = []
        self.load = []
        self.Segment_Area  = []
        self.g=  cfg.Geometry()
    def Set_Segment_area(self , segment):

        self.Segment_Area =  copy.deepcopy( segment)
    def Set_point(self , point):
        self.Lis_Point = point
    def Set_Fix(self , position):
        self.fix .append(position)
    def Set_Load(self , force , position):
        self.Force =  force
        self.load.append(position)

    def Fix_Object(self):
        pass
    def  Preprocessing(self):
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
                        if i == self.fix[0] :
                            self.g.circle([i, lis_pos[0], i + 1] , marker= self.mark_fixed)
                            list_point_cirle.pop(0)
                            self.fix.pop(0)

                            if(self.fix.__len__() == 0) : self.fix.append(100)
                            continue
                        elif i == self.load[0] :
                            self.g.circle([i, lis_pos[0], i + 1], marker= self.load)
                            list_point_cirle.pop(0)
                            self.load.pop(0)
                            if(self.load.__len__() == 0) : self.load.append(100)
                            continue


                        else :
                            self.g.circle([i, lis_pos[0], i + 1], marker= self.mark_E2)
                            list_point_cirle.pop(0)
                            continue
            if i == self.fix[0]:

                self.g.spline([i, i + 1] , marker= self.mark_fixed)
                self.fix.pop(0)


                if (self.fix.__len__() == 0): self.fix.append(100)
                continue

            if i == self.load[0]:
                self.g.spline([i, i + 1] , marker= self.mark_load)
                self.load.pop(0)
                if (self.load.__len__() == 0): self.load.append(100)
                continue
            else  :
                self.g.spline([i, i + 1], marker=self.mark_E2)
        if(self.fix[0] == list_poit.__len__()-1) :
            self.g.spline([list_poit.__len__() - 1, 0] , marker=self.mark_fixed)
        elif(self.load[0] == list_poit.__len__()-1) :
            self.g.spline([list_poit.__len__() - 1, 0] , marker=self.mark_load)
        else :
            self.g.spline([list_poit.__len__() - 1, 0] , marker=self.mark_E2)



        self.g.surface(list_Surface , marker=self.mark_E2)
        # cfv.drawGeometry(self.g)
        # cfv.drawGeometry(self.g2)

        # cfv.showAndWait()
    def check_radius(self , mid_point , start_point , center_point):

        hastable =  defaultdict(lambda :list())
        radius_p1 = self.rotate_matrix(start_point[0] , start_point[1] ,  -90 , mid_point[0] , mid_point[1])
        radius_p2 =  self.rotate_matrix(start_point[0] , start_point[1] ,  90 , mid_point[0] , mid_point[1])
        if(math.dist(radius_p1 ,center_point) < math.dist(radius_p2,center_point)) :
            return radius_p1
        else :
            return radius_p2

    def rotate_matrix(self, x, y, angle, x_shift=0, y_shift=0, units="DEGREES"):
        x = x - x_shift
        y = y - y_shift

        # Convert degrees to radians
        if units == "DEGREES":
            angle = math.radians(angle)

        # Rotation matrix multiplication to get rotated x & y
        xr = (x * math.cos(angle)) - (y * math.sin(angle)) + x_shift
        yr = (x * math.sin(angle)) + (y * math.cos(angle)) + y_shift

        return [xr, yr]

    def Cal_Displace(self):
        t = 0.35
        v = 0.2
        E1 = 2e9
        E2 = 0.2e9
        ptype = 1
        el_size_factor = 5  # Element size factor
        el_type = 2  # Triangle element
        dofs_per_node = 2  # Dof per node
        ep = [ptype, t]
        D1 = cfc.hooke(ptype, E1, v)
        D2 = cfc.hooke(ptype, E2, v)

        elprop = {}
        elprop[self.mark_E1] = [ep, D1]
        elprop[self.mark_E2] = [ep, D2]
        mesh = cfm.GmshMeshGenerator(self.g)
        mesh.el_size_factor = el_size_factor
        mesh.el_type = el_type
        mesh.dofs_per_node = dofs_per_node
        cfv2.figure(fig_size=(10, 10))
        cfv2.draw_geometry(self.g, title="Geometry")



        coords, edof, dofs, bdofs, elementmarkers = mesh.create()
        nDofs = np.size(dofs)
        K = lil_matrix((nDofs, nDofs))

        ex, ey = cfc.coordxtr(edof, coords, dofs)

        for eltopo, elx, ely, elMarker in zip(edof, ex, ey, elementmarkers):

            if el_type == 2:
                Ke = cfc.plante(elx, ely, elprop[elMarker][0], elprop[elMarker][1])
            else:
                Ke = cfc.planqe(elx, ely, elprop[elMarker][0], elprop[elMarker][1])

            cfc.assem(eltopo, K, Ke)
        bc = np.array([], 'i')
        bcVal = np.array([], 'i')

        bc, bcVal = cfu.applybc(bdofs, bc, bcVal, self.mark_fixed, 0.0)

        f = np.zeros([nDofs, 1])

        cfu.applyforcetotal(bdofs, f, self.mark_load, value=self.Force, dimension=2)

        a, r = cfc.spsolveq(K, f, bc, bcVal)
        ed = cfc.extractEldisp(edof, a)
        von_mises = []

        for i in range(edof.shape[0]):

            # Handle triangle elements

            if el_type == 2:
                es, et = cfc.plants(ex[i, :], ey[i, :],
                                    elprop[elementmarkers[i]][0],
                                    elprop[elementmarkers[i]][1],
                                    ed[i, :])

                von_mises.append(
                    np.math.sqrt(pow(es[0, 0], 2) - es[0, 0] * es[0, 1] + pow(es[0, 1], 2) + 3 * pow(es[0, 2], 2)))

            else:

                # Handle quad elements

                es, et = cfc.planqs(ex[i, :], ey[i, :],
                                    elprop[elementmarkers[i]][0],
                                    elprop[elementmarkers[i]][1],
                                    ed[i, :])

                von_mises.append(np.math.sqrt(pow(es[0], 2) - es[0] * es[1] + pow(es[1], 2) + 3 * pow(es[2], 2)))

        # cfv2.figure(fig_size=(10, 10))
        cfv.draw_element_values(von_mises, coords, edof, dofs_per_node, el_type, a,
                                draw_elements=True, draw_undisplaced_mesh=False,
                                title="Effective Stress", magnfac=25.0)


        # cfv2.colorbar()
        cfv2.showAndWait()




