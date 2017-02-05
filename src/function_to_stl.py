from marching_cubes import Cube
from marching_cubes import MarchingCubes
from simple_stl import SimpleSTL
import multiprocessing as mp 
import numpy as np
import time
import math

#parallelized function to STL

def MeshSection(arg):
	[function, xmin, xmax, ymin, ymax, zmin, zmax, step_size] = arg

	meshes = []
	for x in np.arange(xmin,xmax,step_size):
		for y in np.arange(ymin,ymax,step_size):
			for z in np.arange(zmin,zmax,step_size):
				origin = [x, y, z]
				testCube = Cube(origin, step_size, function)
				new_meshes = MarchingCubes(testCube)

				if(new_meshes is not None):
					for new in new_meshes:
						meshes.append(new)
	return meshes

def TestFunction1(point):
	[x,y,z] = point
	#lower bound
	if( (x<0.2) or (y<0.2) or (z<0.2)):
		return 0
	#upper bound
	elif ((x>(max_size-0.2)) or (y>(max_size-0.2)) or (z>(max_size-0.2))):
		return 0
	elif (math.sin(((x/3)*(y/4))+z/4) < 0.7):
		return 1
	else: 
		return 0
def TestFunction2(point):
	[x,y,z] = point
	if( (x<0.2) or (y<0.2) or (z<0.2)):
		return 0
	#upper bound
	elif ((x>(max_size-0.2)) or (y>(max_size-0.2)) or (z>(max_size-0.2))):
		return 0
	#radius 
	elif((x*x+y*y)>90 or (x*x+y*y<70)):
		return 0

	elif(x+z+math.sin(x)) < 10:
		return 1

	else: return 0



cubeMin = 0.
cubeMax = 10.
cubeStep = 0.05
max_size = cubeMax
mySTL = SimpleSTL('test2')
if __name__ == '__main__':
	start_time = time.time()
	numCPU = mp.cpu_count()
	p = mp.Pool(numCPU)
	slice_size = cubeMax / numCPU
	args = []
	for n in range(numCPU):
		args.append((TestFunction2, n * slice_size, (n + 1) * slice_size, cubeMin, cubeMax, cubeMin, cubeMax, cubeStep))


	results = (p.map(MeshSection, args))

	for subResult in results:
		for triangleMesh in subResult:
			mySTL.addFacet(triangleMesh)

	mySTL.ExportSTL()
	print("--- %s seconds ---" % (time.time() - start_time))