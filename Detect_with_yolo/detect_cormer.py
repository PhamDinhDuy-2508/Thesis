import calfem.geometry as cfg
import calfem.mesh as cfm
import calfem.vis as cfv
g = cfg.Geometry()
g.point([173.0, 136.0]) # point 0
g.point([169.0, 272.0]) # point 1
g.point([329.0, 272.0]) # point 2
g.point([334.0, 143.0]) # point 2
g.point([294.0, 143.0]) # point 2
g.point([290.0, 235]) # point 2
g.point([214.0, 235.0]) # point 2
g.point( [214.0, 140.0]) # point 2





g.spline([0, 1]) # line 0
g.spline([1, 2]) # line 1
g.spline([2, 3]) # line 2
g.spline([3, 4]) # line 2
g.spline([4, 5]) # line 2
g.spline([5, 6]) # line 2

g.spline([6, 7]) # line 2
g.spline([7, 0]) # line 2





g.surface( [0, 1, 2, 3, 4, 5, 6, 7])
cfv.drawGeometry(g)
cfv.showAndWait()
mesh = cfm.GmshMesh(g)
mesh.elType = 3          # Degrees of freedom per node.
mesh.dofsPerNode = 5    # Factor that changes element sizes.
mesh.elSizeFactor = 1 # Element size Factor
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



print("test")# Draw the mesh.

