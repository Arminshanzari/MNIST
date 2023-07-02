# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__


import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import optimization
import step
import interaction
import load
import mesh
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
from math import *
Mdb()

for i in range(40):
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(-2.5, 0.0), point2=(2.5, 10.0))
    p = mdb.models['Model-1'].Part(name='Block-%d'%(i+1), dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Block-%d'%(i+1)]
    p.BaseSolidExtrude(sketch=s, depth=15.0+i)
    s.unsetPrimaryObject()
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']

#Assembly
a1 = mdb.models['Model-1'].rootAssembly
a1.DatumCsysByDefault(CARTESIAN)

for i in range(40):
    p = mdb.models['Model-1'].parts['Block-%d'%(i+1)]
    a1.Instance(name='Block-%d-1'%(i+1), part=p, dependent=ON)

points1 = []
j=0
for x in range(40):
    y=20*sin(x*pi/10)
    points1.append([x+j,y])
    j+=9
    
##s = mdb.models['Model-1'].ConstrainedSketch(name='mySketch', 
##    sheetSize=200.0)
##s.Spline(points=points1)

for k in range(1,len(points1)):
    tet = atan((points1[k][1]-points1[k-1][1])/(points1[k][0]-points1[k-1][0]))
    a1.rotate(instanceList=('Block-%d-1'%(k+1), ), axisPoint=(0.0, 0.0, 0.0), 
        axisDirection=(0.0, 0.0, 1.0), angle=degrees(tet))

for i in range(len(points1)):
    a1.translate(instanceList=('Block-%d-1'%(i+1), ), vector=(points1[i][0]+(i*3), points1[i][1], 0.0))


mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((2000.0, 0.3), ))
mdb.models['Model-1'].materials['Material-1'].Density(table=((1.4e-09, ), ))

mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
    material='Material-1', thickness=None)

for i in range(40):
    p = mdb.models['Model-1'].parts['Block-%d'%(i+1)]
    c = p.cells
    cells = p.cells[0:1]
    region = regionToolset.Region(cells=cells)
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)












