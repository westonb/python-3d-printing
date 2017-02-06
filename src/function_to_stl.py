from marching_cubes import Cube
from marching_cubes import MarchingCubes
from simple_stl import SimpleSTL
import multiprocessing as mp 
import numpy as np
import time
import math
import functions_3d as fn 

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



def FunctionToSTL(function, stepSize, Min, Max, fileName):
	mySTL = SimpleSTL(fileName)
	numCPU = mp.cpu_count()
	p = mp.Pool(numCPU)
	slice_size = Max / numCPU
	args = []
	for n in range(numCPU):
		args.append((function, n*slice_size, (n+1)*slice_size, Min, Max, Min, Max, stepSize))

	results = (p.map(MeshSection, args))
	for subResult in results:
		for triangleMesh in subResult:
			mySTL.addFacet(triangleMesh)

	#mySTL.ExportBinSTL()
	mySTL.ExportBinSTL()



if __name__ == '__main__':
	start_time = time.time()
	FunctionToSTL(fn.sine_grid, 0.05, 0., 10., "test2")
	print("--- %s seconds ---" % (time.time() - start_time))