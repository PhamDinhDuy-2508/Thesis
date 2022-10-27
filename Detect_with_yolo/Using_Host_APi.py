import calfem.geometry as cfg
import calfem.mesh as cfm
import calfem.vis as cfv
import calfem.core as cfc
import numpy as np

t = 0.2
v = 0.35
E = 2.1e9
ptype = 1
ep = [ptype,t]
D = cfc.hooke(ptype, E, v)
g = cfg.geometry()
s2 = 1/np.sqrt(2)

points = [[0, 3], [2.5, 3], [3, 3], [4-s2, 3-s2], [4, 2],     #0-4
          [4+s2, 3-s2], [5, 3], [5.5, 3], [8,3], [0, 1.5],    #5-9
          [2.5, 1.5], [4, 1.5], [5.5, 1.5], [8, 1.5], [0, 0], #10-14
          [2.5, 0], [3, 0], [4-s2, s2], [4, 1], [4+s2, s2],   #15-19
          [5, 0], [5.5, 0], [8,0], [4,3], [4,0]]              #20-24

for xp, yp in points:
    g.point([xp*0.1, yp*0.1])
splines = [[0,1], [1,2], [6,7], [7,8], [8,13],          #0-4
           [13,22], [22,21], [21,20], [16,15], [15,14], #5-9
           [14,9], [9,0], [9,10], [10,1], [10, 15],     #10-14
           [10,11], [11,4], [11,18], [11,12], [12,7],   #15-19
           [12,21], [12,13], [3,10], [5,12], [10,17],   #20-24
           [12,19]]                                     #25
     #25

for s in splines:
    g.spline(s, el_on_curve=10)
# Points in circle arcs are [start, center, end]

circlearcs = [[2, 23, 3], [3, 23, 4], [4, 23, 5], [5, 23, 6],           #26-29
              [16, 24, 17], [17, 24, 18], [18, 24, 19], [19, 24, 20]]   #30-33

for c in circlearcs:
    g.circle(c, el_on_curve=10)
g.struct_surf([11,12,13,0]) #0
g.struct_surf([14, 12, 10, 9])
g.struct_surf([8, 30, 24, 14])
g.struct_surf([24, 31, 17, 15])
g.struct_surf([15, 16, 27, 22]) #4
g.struct_surf([22, 26, 1, 13])
g.struct_surf([16, 18, 23, 28])
g.struct_surf([19, 2, 29, 23])
g.struct_surf([19, 21, 4, 3]) #8
g.struct_surf([20, 6, 5, 21])
g.struct_surf([25, 20, 7, 33])
g.struct_surf([32, 17, 18, 25]) #11S
mesh = cfm.GmshMesh(g)
cfv.drawGeometry(g)
# cfv.draw_geometry(g, draw_points=True, label_curves=True, label_points=True)
cfv.showAndWait()
mesh.el_type = 3
mesh.dofs_per_node = 2

coords, edof, dofs, bdofs, elementmarkers = mesh.create()
cfv.draw_mesh(coords, edof, dofs_per_node=mesh.dofs_per_node, el_type=mesh.el_type)
cfv.showAndWait()
