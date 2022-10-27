import calfem.core as cfc
import calfem.geometry as cfg
import calfem.mesh as cfm
import calfem.vis_mpl as cfv
import calfem.utils as cfu
import numpy as np

from scipy.sparse import lil_matrix
t = 0.2
v = 0.2
E1 = 2e9
E2 = 0.2e9
ptype = 1
ep = [ptype,t]
D1 = cfc.hooke(ptype, E1, v)
D2 = cfc.hooke(ptype, E2, v)

# Define marker constants instead of using numbers in the code

mark_E1 = 55
mark_E2 = 66
mark_fixed = 70
mark_load = 90

# Create dictionary for the different element properties

elprop = {}
elprop[mark_E1] = [ep, D1]
elprop[mark_E2] = [ep, D2]

# Parameters controlling mesh

el_size_factor = 5    # Element size factor
el_type = 3             # Triangle element
dofs_per_node = 2        # Dof per node
g = cfg.Geometry()
g.point([282, 236]) # point 0
g.point([171.5, 347.5]) # point 1

g.point([283, 458]) # point 2
g.point([347, 457]) # point 3
g.point( [347, 402]) # point 4

g.point([282, 399]) # point 5
g.point([229.0, 346.0]) # point 6
g.point( [282, 293]) # point 7

g.point([346, 292]) # point 8
g.point([346, 237]) # point 9
g.point([282.5, 347.0]) # point 10
g.point([282.0, 346.0]) # point 1111



g.circle([0,10,1]  , marker = mark_E2)
g.circle([1,10,2]  ,  marker = mark_E2)
g.spline([2, 3]  ,marker = mark_load) # line 2
g.spline([3, 4]) # line 2

g.spline([4, 5]) # line 2
g.circle([5,11,6]  ,  marker = mark_E2)
g.circle([6,11,7]  ,  marker = mark_E2)
g.spline([7, 8]  , marker = mark_E2) # line 2
g.spline([8, 9], marker = mark_E2) # line 2
g.spline([9, 0] ,marker = mark_fixed) # line 2
g.surface([0,1,2,3,4,5,6,7,8,9], marker = mark_E2)





mesh = cfm.GmshMeshGenerator(g)
mesh.el_size_factor = el_size_factor
mesh.el_type = el_type
mesh.dofs_per_node = dofs_per_node
cfv.figure(fig_size=(10,10))
cfv.draw_geometry(g, title="Geometry")

# Mesh the geometry:
#  The first four return values are the same as those that trimesh2d() returns.
#  value elementmarkers is a list of markers, and is used for finding the
#  marker of a given element (index).

coords, edof, dofs, bdofs, elementmarkers = mesh.create()
nDofs = np.size(dofs)
K = lil_matrix((nDofs,nDofs))

ex, ey = cfc.coordxtr(edof, coords, dofs)

for eltopo, elx, ely, elMarker in zip(edof, ex, ey, elementmarkers):

    if el_type == 2:
        Ke = cfc.plante(elx, ely, elprop[elMarker][0], elprop[elMarker][1])
    else:
        Ke = cfc.planqe(elx, ely, elprop[elMarker][0], elprop[elMarker][1])

    cfc.assem(eltopo, K, Ke)
bc = np.array([],'i')
bcVal = np.array([],'i')

bc, bcVal = cfu.applybc(bdofs, bc, bcVal, mark_fixed, 0.0)

f = np.zeros([nDofs,1])

cfu.applyforcetotal(bdofs, f, mark_load, value =- 5e5, dimension=2)

a,r = cfc.spsolveq(K, f, bc, bcVal)
ed = cfc.extractEldisp(edof, a)
von_mises = []

for i in range(edof.shape[0]):

    # Handle triangle elements

    if el_type == 2:
        es, et = cfc.plants(ex[i,:], ey[i,:],
                        elprop[elementmarkers[i]][0],
                        elprop[elementmarkers[i]][1],
                        ed[i,:])

        von_mises.append( np.math.sqrt( pow(es[0,0],2) - es[0,0]*es[0,1] + pow(es[0,1],2) + 3*pow(es[0,2],2) ) )

    else:

        # Handle quad elements

        es, et = cfc.planqs(ex[i,:], ey[i,:],
                        elprop[elementmarkers[i]][0],
                        elprop[elementmarkers[i]][1],
                        ed[i,:])

        von_mises.append( np.math.sqrt( pow(es[0],2) - es[0]*es[1] + pow(es[1],2) + 3*pow(es[2],2) ) )

cfv.figure(fig_size=(10,10))
cfv.draw_element_values(von_mises, coords, edof, dofs_per_node, el_type, a,
                      draw_elements=True, draw_undisplaced_mesh=False,
                      title="Effective Stress", magnfac=25.0)

cfv.colorbar()
cfv.showAndWait()