import copy

import calfem.geometry as cfg
import calfem.mesh as cfm
import calfem.vis as cfv
from  collections  import  defaultdict
class Meshing :

    def __init__(self) -> None:

        super().__init__()
        self.List_segment = []
        self.Result = []
        self.g = cfg.Geometry()
        self.Curve_area = []
        self.Hastable_Segment = defaultdict(lambda : list)
        self.Segment_Area = []



    def Set_Hastable_Segment (self , hash) :
        self.Hastable_Segment =  hash
        list_key =  list( self.Hastable_Segment.keys()  )
        for i in range(list_key.__len__()) :
            self.Segment_Area.append(self.Hastable_Segment.get(list_key[i]))
        print(self.Segment_Area)
    def Messing_2(self):

        for i in range(self.List_segment.__len__()) :
            if  self.List_segment[i][0] == 'Line' :
                self.g.point(self.List_segment[i][1])
                self.g.point(self.List_segment[i][2])
            else :
                pass


    def Set_Curve_Area(self , curve_area):
        self.Curve_area =  curve_area

    def Set_Lisegment(self , list):
        self.List_segment =  copy.deepcopy(list )

    def pre_process_Curve(self):
        pass


    def Meshing(self):
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
