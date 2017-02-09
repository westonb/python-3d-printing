import marching_cubes as mc
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
	generator = mc.CubeGrid(function,[xmax-xmin,ymax-ymin,zmax-zmin], [xmin, ymin, zmin], step_size)
	generator.SearchCube(True)
	
	return generator.triangles



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
	mySTL.ExportBinSTL()



if __name__ == '__main__':
	start_time = time.time()
	FunctionToSTL(fn.sine_grid, 0.025, 0, 400, "test2")
	print("--- %s seconds ---" % (time.time() - start_time))