import math
import numpy as np
import time
import simple_stl as stl
import functions_3d as fn
#marching cubes

#helper classes
class Cube:
	stepSize = 0
	function = None
	points = [[0.0,0.0,0.0]]*8
	values = [0.0]*8
	origin = [0.0,0.0,0.0]
	def __init__(self, origin, stepSize, function):
		self.stepSize = stepSize
		self.origin = origin
		self.function = function
		self.points[0] = origin
		self.points[1] = [self.origin[0] + self.stepSize, self.origin[1], self.origin[2]]
		self.points[2] = [self.origin[0] + self.stepSize, self.origin[1] + self.stepSize, self.origin[2]]
		self.points[3] = [self.origin[0], self.origin[1] + self.stepSize, self.origin[2]]
		self.points[4] = [self.origin[0], self.origin[1], self.origin[2] + self.stepSize]
		self.points[5] = [self.origin[0] + self.stepSize, self.origin[1], self.origin[2] + self.stepSize]
		self.points[6] = [self.origin[0] + self.stepSize, self.origin[1] + self.stepSize, self.origin[2] + self.stepSize]
		self.points[7] = [self.origin[0], self.origin[1] + self.stepSize, self.origin[2] + self.stepSize]
		
		self.values[0] = self.function(self.points[0])
		self.values[1] = self.function(self.points[1])
		self.values[2] = self.function(self.points[2])
		self.values[3] = self.function(self.points[3])
		self.values[4] = self.function(self.points[4])
		self.values[5] = self.function(self.points[5])
		self.values[6] = self.function(self.points[6])
		self.values[7] = self.function(self.points[7])
class CubeGrid:
	Size = [0,0,0]
	Origin = [0,0,0]
	StepSize = 0.
	SequentalCount = [0,0,0]
	Function = None

	def __init__(self, Function, Size, Origin, StepSize):
		self.Size = Size
		self.Origin = Origin
		self.StepSize = StepSize
		self.SequentalCount = [0,0,0]
		self.Function = Function
		self.Solutions = np.full((Size[0]+1, Size[1]+1, Size[2]+1), -1, int)
	#(points, values)
	def SpawnSequentialCube(self):
		points = [[0,0,0]]*8
		values = [0]*8
		

		points[0] = [(self.SequentalCount[0]+self.Origin[0])*self.StepSize, 
					(self.SequentalCount[1]+self.Origin[1])*self.StepSize,
					(self.SequentalCount[2]+self.Origin[2])*self.StepSize]
		points[1] = [(self.SequentalCount[0]+self.Origin[0]+1)*self.StepSize, 
					(self.SequentalCount[1]+self.Origin[1])*self.StepSize,
					(self.SequentalCount[2]+self.Origin[2])*self.StepSize]
		points[2] = [(self.SequentalCount[0]+self.Origin[0]+1)*self.StepSize, 
					(self.SequentalCount[1]+self.Origin[1]+1)*self.StepSize,
					(self.SequentalCount[2]+self.Origin[2])*self.StepSize]
		points[3] = [(self.SequentalCount[0]+self.Origin[0])*self.StepSize, 
					(self.SequentalCount[1]+self.Origin[1]+1)*self.StepSize,
					(self.SequentalCount[2]+self.Origin[2])*self.StepSize]
		points[4] = [(self.SequentalCount[0]+self.Origin[0])*self.StepSize, 
					(self.SequentalCount[1]+self.Origin[1])*self.StepSize,
					(self.SequentalCount[2]+self.Origin[2]+1)*self.StepSize]
		points[5] = [(self.SequentalCount[0]+self.Origin[0]+1)*self.StepSize, 
					(self.SequentalCount[1]+self.Origin[1])*self.StepSize,
					(self.SequentalCount[2]+self.Origin[2]+1)*self.StepSize]
		points[6] = [(self.SequentalCount[0]+self.Origin[0]+1)*self.StepSize, 
					(self.SequentalCount[1]+self.Origin[1]+1)*self.StepSize,
					(self.SequentalCount[2]+self.Origin[2]+1)*self.StepSize]
		points[7] = [(self.SequentalCount[0]+self.Origin[0])*self.StepSize, 
					(self.SequentalCount[1]+self.Origin[1]+1)*self.StepSize,
					(self.SequentalCount[2]+self.Origin[2]+1)*self.StepSize]
		#memoize solutions 
		#point 0
		if (self.Solutions[self.SequentalCount[0]][self.SequentalCount[1]][self.SequentalCount[2]]) != -1:
			values[0] = (self.Solutions[self.SequentalCount[0]] [self.SequentalCount[1]][self.SequentalCount[2]])
			
		else:
			values[0] = self.Function(points[0])
			
			(self.Solutions[self.SequentalCount[0]][self.SequentalCount[1]][self.SequentalCount[2]]) = values[0]
		#point 1

		if (self.Solutions[self.SequentalCount[0]+1][self.SequentalCount[1]][self.SequentalCount[2]]) != -1:
			values[1] = (self.Solutions[self.SequentalCount[0]+1] [self.SequentalCount[1]][self.SequentalCount[2]])
		else:
			values[1] = self.Function(points[1])
			(self.Solutions[self.SequentalCount[0]+1][self.SequentalCount[1]][self.SequentalCount[2]]) = values[1]
		#point 2
		if (self.Solutions[self.SequentalCount[0]+1][self.SequentalCount[1]+1][self.SequentalCount[2]]) != -1:
			values[2] = (self.Solutions[self.SequentalCount[0]+1][self.SequentalCount[1]+1][self.SequentalCount[2]])
		else:
			values[2] = self.Function(points[2])
			(self.Solutions[self.SequentalCount[0]+1][self.SequentalCount[1]+1][self.SequentalCount[2]]) = values[2]
		#point 3
		if (self.Solutions[self.SequentalCount[0]][self.SequentalCount[1]+1][self.SequentalCount[2]]) != -1:
			values[3] = (self.Solutions[self.SequentalCount[0]] [self.SequentalCount[1]+1][self.SequentalCount[2]])
		else:
			values[3] = self.Function(points[2])
			(self.Solutions[self.SequentalCount[0]][self.SequentalCount[1]+1][self.SequentalCount[2]]) = values[3]
		#point 4
		if (self.Solutions[self.SequentalCount[0]][self.SequentalCount[1]][self.SequentalCount[2]+1]) != -1:
			values[4] = (self.Solutions[self.SequentalCount[0]][self.SequentalCount[1]][self.SequentalCount[2]+1])
		else:
			values[4] = self.Function(points[0])
			(self.Solutions[self.SequentalCount[0]][self.SequentalCount[1]][self.SequentalCount[2]+1]) = values[4]
		#point 5
		if (self.Solutions[self.SequentalCount[0]+1][self.SequentalCount[1]][self.SequentalCount[2]+1]) != -1:
			values[5] = (self.Solutions[self.SequentalCount[0]+1][self.SequentalCount[1]][self.SequentalCount[2]+1])
		else:
			values[5] = self.Function(points[0])
			(self.Solutions[self.SequentalCount[0]+1][self.SequentalCount[1]][self.SequentalCount[2]+1]) = values[5]
		#point 6
		if (self.Solutions[self.SequentalCount[0]+1][self.SequentalCount[1]+1][self.SequentalCount[2]+1]) != -1:
			values[6] = (self.Solutions[self.SequentalCount[0]+1][self.SequentalCount[1]+1][self.SequentalCount[2]+1])
		else:
			values[6] = self.Function(points[0])
			(self.Solutions[self.SequentalCount[0]+1][self.SequentalCount[1]+1][self.SequentalCount[2]+1]) = values[6]
		#point 7
		if (self.Solutions[self.SequentalCount[0]][self.SequentalCount[1]+1][self.SequentalCount[2]+1]) != -1:
			values[7] = (self.Solutions[self.SequentalCount[0]][self.SequentalCount[1]+1][self.SequentalCount[2]+1])
		else:
			values[7] = self.Function(points[0])
			(self.Solutions[self.SequentalCount[0]][self.SequentalCount[1]+1][self.SequentalCount[2]+1]) = values[7]
	




		#sequental count is incrimented by x, y, z
		if(self.SequentalCount[0] >= (self.Size[0]-1)):
			self.SequentalCount[0] = 0
			if(self.SequentalCount[1] >= (self.Size[1]-1)):
				self.SequentalCount[1] = 0
				if(self.SequentalCount[2] >= (self.Size[2]-1)):
					return None
				else:
					self.SequentalCount[2] = self.SequentalCount[2] + 1
			else:
				self.SequentalCount[1] = self.SequentalCount[1] + 1
		else: 
			self.SequentalCount[0] = self.SequentalCount[0] + 1

		return (points, values)

	def resetSequentialCount(self):
		self.SequentalCount = [0,0,0]

	def dfsCube(self):
		pass

class Facet:

	V1 = []
	V2 = []
	V3 = []
	unit_norm = []
	def __init__(self, points):
		self.V1 = points[0]
		self.V2 = points[1]
		self.V3 = points[2]
		self.calc_norm()

	def calc_norm(self):
		#x = (y2-y1)(z3-z1)-(y3-y1)(z2-z1)
		#y = (z2-z1)(x3-x1)-(x2-x1)(z3-z1)
		#z = (x2-x1)(y3-y1)-(x3-x1)(y2-y1)
		x = (self.V2[1]-self.V1[1])*(self.V3[2]-self.V1[2]) - (self.V3[1]-self.V1[1])*(self.V2[2]-self.V1[2])
		y = (self.V2[2]-self.V1[2])*(self.V3[0]-self.V1[0]) - (self.V2[0]-self.V1[0])*(self.V3[2]-self.V1[2])
		z = (self.V2[0]-self.V1[0])*(self.V3[1]-self.V1[1]) - (self.V3[0]-self.V1[0])*(self.V2[1]-self.V1[1])
		length = math.sqrt(x*x+y*y+z*z)
		self.unit_norm = [x/length, y/length, z/length]



def MarchingCubes(points, values):

	vert_list = [0]*12

	edgeTable = [0x0  , 0x109, 0x203, 0x30a, 0x406, 0x50f, 0x605, 0x70c,
	0x80c, 0x905, 0xa0f, 0xb06, 0xc0a, 0xd03, 0xe09, 0xf00,
	0x190, 0x99 , 0x393, 0x29a, 0x596, 0x49f, 0x795, 0x69c,
	0x99c, 0x895, 0xb9f, 0xa96, 0xd9a, 0xc93, 0xf99, 0xe90,
	0x230, 0x339, 0x33 , 0x13a, 0x636, 0x73f, 0x435, 0x53c,
	0xa3c, 0xb35, 0x83f, 0x936, 0xe3a, 0xf33, 0xc39, 0xd30,
	0x3a0, 0x2a9, 0x1a3, 0xaa , 0x7a6, 0x6af, 0x5a5, 0x4ac,
	0xbac, 0xaa5, 0x9af, 0x8a6, 0xfaa, 0xea3, 0xda9, 0xca0,
	0x460, 0x569, 0x663, 0x76a, 0x66 , 0x16f, 0x265, 0x36c,
	0xc6c, 0xd65, 0xe6f, 0xf66, 0x86a, 0x963, 0xa69, 0xb60,
	0x5f0, 0x4f9, 0x7f3, 0x6fa, 0x1f6, 0xff , 0x3f5, 0x2fc,
	0xdfc, 0xcf5, 0xfff, 0xef6, 0x9fa, 0x8f3, 0xbf9, 0xaf0,
	0x650, 0x759, 0x453, 0x55a, 0x256, 0x35f, 0x55 , 0x15c,
	0xe5c, 0xf55, 0xc5f, 0xd56, 0xa5a, 0xb53, 0x859, 0x950,
	0x7c0, 0x6c9, 0x5c3, 0x4ca, 0x3c6, 0x2cf, 0x1c5, 0xcc ,
	0xfcc, 0xec5, 0xdcf, 0xcc6, 0xbca, 0xac3, 0x9c9, 0x8c0,
	0x8c0, 0x9c9, 0xac3, 0xbca, 0xcc6, 0xdcf, 0xec5, 0xfcc,
	0xcc , 0x1c5, 0x2cf, 0x3c6, 0x4ca, 0x5c3, 0x6c9, 0x7c0,
	0x950, 0x859, 0xb53, 0xa5a, 0xd56, 0xc5f, 0xf55, 0xe5c,
	0x15c, 0x55 , 0x35f, 0x256, 0x55a, 0x453, 0x759, 0x650,
	0xaf0, 0xbf9, 0x8f3, 0x9fa, 0xef6, 0xfff, 0xcf5, 0xdfc,
	0x2fc, 0x3f5, 0xff , 0x1f6, 0x6fa, 0x7f3, 0x4f9, 0x5f0,
	0xb60, 0xa69, 0x963, 0x86a, 0xf66, 0xe6f, 0xd65, 0xc6c,
	0x36c, 0x265, 0x16f, 0x66 , 0x76a, 0x663, 0x569, 0x460,
	0xca0, 0xda9, 0xea3, 0xfaa, 0x8a6, 0x9af, 0xaa5, 0xbac,
	0x4ac, 0x5a5, 0x6af, 0x7a6, 0xaa , 0x1a3, 0x2a9, 0x3a0,
	0xd30, 0xc39, 0xf33, 0xe3a, 0x936, 0x83f, 0xb35, 0xa3c,
	0x53c, 0x435, 0x73f, 0x636, 0x13a, 0x33 , 0x339, 0x230,
	0xe90, 0xf99, 0xc93, 0xd9a, 0xa96, 0xb9f, 0x895, 0x99c,
	0x69c, 0x795, 0x49f, 0x596, 0x29a, 0x393, 0x99 , 0x190,
	0xf00, 0xe09, 0xd03, 0xc0a, 0xb06, 0xa0f, 0x905, 0x80c,
	0x70c, 0x605, 0x50f, 0x406, 0x30a, 0x203, 0x109, 0x0 ]

	triTable = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[0, 8, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[0, 1, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[1, 8, 3, 9, 8, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[1, 2, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[0, 8, 3, 1, 2, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[9, 2, 10, 0, 2, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[2, 8, 3, 2, 10, 8, 10, 9, 8, -1, -1, -1, -1, -1, -1, -1],
	[3, 11, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[0, 11, 2, 8, 11, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[1, 9, 0, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[1, 11, 2, 1, 9, 11, 9, 8, 11, -1, -1, -1, -1, -1, -1, -1],
	[3, 10, 1, 11, 10, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[0, 10, 1, 0, 8, 10, 8, 11, 10, -1, -1, -1, -1, -1, -1, -1],
	[3, 9, 0, 3, 11, 9, 11, 10, 9, -1, -1, -1, -1, -1, -1, -1],
	[9, 8, 10, 10, 8, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[4, 7, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[4, 3, 0, 7, 3, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[0, 1, 9, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[4, 1, 9, 4, 7, 1, 7, 3, 1, -1, -1, -1, -1, -1, -1, -1],
	[1, 2, 10, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[3, 4, 7, 3, 0, 4, 1, 2, 10, -1, -1, -1, -1, -1, -1, -1],
	[9, 2, 10, 9, 0, 2, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1],
	[2, 10, 9, 2, 9, 7, 2, 7, 3, 7, 9, 4, -1, -1, -1, -1],
	[8, 4, 7, 3, 11, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[11, 4, 7, 11, 2, 4, 2, 0, 4, -1, -1, -1, -1, -1, -1, -1],
	[9, 0, 1, 8, 4, 7, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1],
	[4, 7, 11, 9, 4, 11, 9, 11, 2, 9, 2, 1, -1, -1, -1, -1],
	[3, 10, 1, 3, 11, 10, 7, 8, 4, -1, -1, -1, -1, -1, -1, -1],
	[1, 11, 10, 1, 4, 11, 1, 0, 4, 7, 11, 4, -1, -1, -1, -1],
	[4, 7, 8, 9, 0, 11, 9, 11, 10, 11, 0, 3, -1, -1, -1, -1],
	[4, 7, 11, 4, 11, 9, 9, 11, 10, -1, -1, -1, -1, -1, -1, -1],
	[9, 5, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[9, 5, 4, 0, 8, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[0, 5, 4, 1, 5, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[8, 5, 4, 8, 3, 5, 3, 1, 5, -1, -1, -1, -1, -1, -1, -1],
	[1, 2, 10, 9, 5, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[3, 0, 8, 1, 2, 10, 4, 9, 5, -1, -1, -1, -1, -1, -1, -1],
	[5, 2, 10, 5, 4, 2, 4, 0, 2, -1, -1, -1, -1, -1, -1, -1],
	[2, 10, 5, 3, 2, 5, 3, 5, 4, 3, 4, 8, -1, -1, -1, -1],
	[9, 5, 4, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[0, 11, 2, 0, 8, 11, 4, 9, 5, -1, -1, -1, -1, -1, -1, -1],
	[0, 5, 4, 0, 1, 5, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1],
	[2, 1, 5, 2, 5, 8, 2, 8, 11, 4, 8, 5, -1, -1, -1, -1],
	[10, 3, 11, 10, 1, 3, 9, 5, 4, -1, -1, -1, -1, -1, -1, -1],
	[4, 9, 5, 0, 8, 1, 8, 10, 1, 8, 11, 10, -1, -1, -1, -1],
	[5, 4, 0, 5, 0, 11, 5, 11, 10, 11, 0, 3, -1, -1, -1, -1],
	[5, 4, 8, 5, 8, 10, 10, 8, 11, -1, -1, -1, -1, -1, -1, -1],
	[9, 7, 8, 5, 7, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[9, 3, 0, 9, 5, 3, 5, 7, 3, -1, -1, -1, -1, -1, -1, -1],
	[0, 7, 8, 0, 1, 7, 1, 5, 7, -1, -1, -1, -1, -1, -1, -1],
	[1, 5, 3, 3, 5, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[9, 7, 8, 9, 5, 7, 10, 1, 2, -1, -1, -1, -1, -1, -1, -1],
	[10, 1, 2, 9, 5, 0, 5, 3, 0, 5, 7, 3, -1, -1, -1, -1],
	[8, 0, 2, 8, 2, 5, 8, 5, 7, 10, 5, 2, -1, -1, -1, -1],
	[2, 10, 5, 2, 5, 3, 3, 5, 7, -1, -1, -1, -1, -1, -1, -1],
	[7, 9, 5, 7, 8, 9, 3, 11, 2, -1, -1, -1, -1, -1, -1, -1],
	[9, 5, 7, 9, 7, 2, 9, 2, 0, 2, 7, 11, -1, -1, -1, -1],
	[2, 3, 11, 0, 1, 8, 1, 7, 8, 1, 5, 7, -1, -1, -1, -1],
	[11, 2, 1, 11, 1, 7, 7, 1, 5, -1, -1, -1, -1, -1, -1, -1],
	[9, 5, 8, 8, 5, 7, 10, 1, 3, 10, 3, 11, -1, -1, -1, -1],
	[5, 7, 0, 5, 0, 9, 7, 11, 0, 1, 0, 10, 11, 10, 0, -1],
	[11, 10, 0, 11, 0, 3, 10, 5, 0, 8, 0, 7, 5, 7, 0, -1],
	[11, 10, 5, 7, 11, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[10, 6, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[0, 8, 3, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[9, 0, 1, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[1, 8, 3, 1, 9, 8, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1],
	[1, 6, 5, 2, 6, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[1, 6, 5, 1, 2, 6, 3, 0, 8, -1, -1, -1, -1, -1, -1, -1],
	[9, 6, 5, 9, 0, 6, 0, 2, 6, -1, -1, -1, -1, -1, -1, -1],
	[5, 9, 8, 5, 8, 2, 5, 2, 6, 3, 2, 8, -1, -1, -1, -1],
	[2, 3, 11, 10, 6, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[11, 0, 8, 11, 2, 0, 10, 6, 5, -1, -1, -1, -1, -1, -1, -1],
	[0, 1, 9, 2, 3, 11, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1],
	[5, 10, 6, 1, 9, 2, 9, 11, 2, 9, 8, 11, -1, -1, -1, -1],
	[6, 3, 11, 6, 5, 3, 5, 1, 3, -1, -1, -1, -1, -1, -1, -1],
	[0, 8, 11, 0, 11, 5, 0, 5, 1, 5, 11, 6, -1, -1, -1, -1],
	[3, 11, 6, 0, 3, 6, 0, 6, 5, 0, 5, 9, -1, -1, -1, -1],
	[6, 5, 9, 6, 9, 11, 11, 9, 8, -1, -1, -1, -1, -1, -1, -1],
	[5, 10, 6, 4, 7, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[4, 3, 0, 4, 7, 3, 6, 5, 10, -1, -1, -1, -1, -1, -1, -1],
	[1, 9, 0, 5, 10, 6, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1],
	[10, 6, 5, 1, 9, 7, 1, 7, 3, 7, 9, 4, -1, -1, -1, -1],
	[6, 1, 2, 6, 5, 1, 4, 7, 8, -1, -1, -1, -1, -1, -1, -1],
	[1, 2, 5, 5, 2, 6, 3, 0, 4, 3, 4, 7, -1, -1, -1, -1],
	[8, 4, 7, 9, 0, 5, 0, 6, 5, 0, 2, 6, -1, -1, -1, -1],
	[7, 3, 9, 7, 9, 4, 3, 2, 9, 5, 9, 6, 2, 6, 9, -1],
	[3, 11, 2, 7, 8, 4, 10, 6, 5, -1, -1, -1, -1, -1, -1, -1],
	[5, 10, 6, 4, 7, 2, 4, 2, 0, 2, 7, 11, -1, -1, -1, -1],
	[0, 1, 9, 4, 7, 8, 2, 3, 11, 5, 10, 6, -1, -1, -1, -1],
	[9, 2, 1, 9, 11, 2, 9, 4, 11, 7, 11, 4, 5, 10, 6, -1],
	[8, 4, 7, 3, 11, 5, 3, 5, 1, 5, 11, 6, -1, -1, -1, -1],
	[5, 1, 11, 5, 11, 6, 1, 0, 11, 7, 11, 4, 0, 4, 11, -1],
	[0, 5, 9, 0, 6, 5, 0, 3, 6, 11, 6, 3, 8, 4, 7, -1],
	[6, 5, 9, 6, 9, 11, 4, 7, 9, 7, 11, 9, -1, -1, -1, -1],
	[10, 4, 9, 6, 4, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[4, 10, 6, 4, 9, 10, 0, 8, 3, -1, -1, -1, -1, -1, -1, -1],
	[10, 0, 1, 10, 6, 0, 6, 4, 0, -1, -1, -1, -1, -1, -1, -1],
	[8, 3, 1, 8, 1, 6, 8, 6, 4, 6, 1, 10, -1, -1, -1, -1],
	[1, 4, 9, 1, 2, 4, 2, 6, 4, -1, -1, -1, -1, -1, -1, -1],
	[3, 0, 8, 1, 2, 9, 2, 4, 9, 2, 6, 4, -1, -1, -1, -1],
	[0, 2, 4, 4, 2, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[8, 3, 2, 8, 2, 4, 4, 2, 6, -1, -1, -1, -1, -1, -1, -1],
	[10, 4, 9, 10, 6, 4, 11, 2, 3, -1, -1, -1, -1, -1, -1, -1],
	[0, 8, 2, 2, 8, 11, 4, 9, 10, 4, 10, 6, -1, -1, -1, -1],
	[3, 11, 2, 0, 1, 6, 0, 6, 4, 6, 1, 10, -1, -1, -1, -1],
	[6, 4, 1, 6, 1, 10, 4, 8, 1, 2, 1, 11, 8, 11, 1, -1],
	[9, 6, 4, 9, 3, 6, 9, 1, 3, 11, 6, 3, -1, -1, -1, -1],
	[8, 11, 1, 8, 1, 0, 11, 6, 1, 9, 1, 4, 6, 4, 1, -1],
	[3, 11, 6, 3, 6, 0, 0, 6, 4, -1, -1, -1, -1, -1, -1, -1],
	[6, 4, 8, 11, 6, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[7, 10, 6, 7, 8, 10, 8, 9, 10, -1, -1, -1, -1, -1, -1, -1],
	[0, 7, 3, 0, 10, 7, 0, 9, 10, 6, 7, 10, -1, -1, -1, -1],
	[10, 6, 7, 1, 10, 7, 1, 7, 8, 1, 8, 0, -1, -1, -1, -1],
	[10, 6, 7, 10, 7, 1, 1, 7, 3, -1, -1, -1, -1, -1, -1, -1],
	[1, 2, 6, 1, 6, 8, 1, 8, 9, 8, 6, 7, -1, -1, -1, -1],
	[2, 6, 9, 2, 9, 1, 6, 7, 9, 0, 9, 3, 7, 3, 9, -1],
	[7, 8, 0, 7, 0, 6, 6, 0, 2, -1, -1, -1, -1, -1, -1, -1],
	[7, 3, 2, 6, 7, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[2, 3, 11, 10, 6, 8, 10, 8, 9, 8, 6, 7, -1, -1, -1, -1],
	[2, 0, 7, 2, 7, 11, 0, 9, 7, 6, 7, 10, 9, 10, 7, -1],
	[1, 8, 0, 1, 7, 8, 1, 10, 7, 6, 7, 10, 2, 3, 11, -1],
	[11, 2, 1, 11, 1, 7, 10, 6, 1, 6, 7, 1, -1, -1, -1, -1],
	[8, 9, 6, 8, 6, 7, 9, 1, 6, 11, 6, 3, 1, 3, 6, -1],
	[0, 9, 1, 11, 6, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[7, 8, 0, 7, 0, 6, 3, 11, 0, 11, 6, 0, -1, -1, -1, -1],
	[7, 11, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[7, 6, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[3, 0, 8, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[0, 1, 9, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[8, 1, 9, 8, 3, 1, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1],
	[10, 1, 2, 6, 11, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[1, 2, 10, 3, 0, 8, 6, 11, 7, -1, -1, -1, -1, -1, -1, -1],
	[2, 9, 0, 2, 10, 9, 6, 11, 7, -1, -1, -1, -1, -1, -1, -1],
	[6, 11, 7, 2, 10, 3, 10, 8, 3, 10, 9, 8, -1, -1, -1, -1],
	[7, 2, 3, 6, 2, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[7, 0, 8, 7, 6, 0, 6, 2, 0, -1, -1, -1, -1, -1, -1, -1],
	[2, 7, 6, 2, 3, 7, 0, 1, 9, -1, -1, -1, -1, -1, -1, -1],
	[1, 6, 2, 1, 8, 6, 1, 9, 8, 8, 7, 6, -1, -1, -1, -1],
	[10, 7, 6, 10, 1, 7, 1, 3, 7, -1, -1, -1, -1, -1, -1, -1],
	[10, 7, 6, 1, 7, 10, 1, 8, 7, 1, 0, 8, -1, -1, -1, -1],
	[0, 3, 7, 0, 7, 10, 0, 10, 9, 6, 10, 7, -1, -1, -1, -1],
	[7, 6, 10, 7, 10, 8, 8, 10, 9, -1, -1, -1, -1, -1, -1, -1],
	[6, 8, 4, 11, 8, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[3, 6, 11, 3, 0, 6, 0, 4, 6, -1, -1, -1, -1, -1, -1, -1],
	[8, 6, 11, 8, 4, 6, 9, 0, 1, -1, -1, -1, -1, -1, -1, -1],
	[9, 4, 6, 9, 6, 3, 9, 3, 1, 11, 3, 6, -1, -1, -1, -1],
	[6, 8, 4, 6, 11, 8, 2, 10, 1, -1, -1, -1, -1, -1, -1, -1],
	[1, 2, 10, 3, 0, 11, 0, 6, 11, 0, 4, 6, -1, -1, -1, -1],
	[4, 11, 8, 4, 6, 11, 0, 2, 9, 2, 10, 9, -1, -1, -1, -1],
	[10, 9, 3, 10, 3, 2, 9, 4, 3, 11, 3, 6, 4, 6, 3, -1],
	[8, 2, 3, 8, 4, 2, 4, 6, 2, -1, -1, -1, -1, -1, -1, -1],
	[0, 4, 2, 4, 6, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[1, 9, 0, 2, 3, 4, 2, 4, 6, 4, 3, 8, -1, -1, -1, -1],
	[1, 9, 4, 1, 4, 2, 2, 4, 6, -1, -1, -1, -1, -1, -1, -1],
	[8, 1, 3, 8, 6, 1, 8, 4, 6, 6, 10, 1, -1, -1, -1, -1],
	[10, 1, 0, 10, 0, 6, 6, 0, 4, -1, -1, -1, -1, -1, -1, -1],
	[4, 6, 3, 4, 3, 8, 6, 10, 3, 0, 3, 9, 10, 9, 3, -1],
	[10, 9, 4, 6, 10, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[4, 9, 5, 7, 6, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[0, 8, 3, 4, 9, 5, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1],
	[5, 0, 1, 5, 4, 0, 7, 6, 11, -1, -1, -1, -1, -1, -1, -1],
	[11, 7, 6, 8, 3, 4, 3, 5, 4, 3, 1, 5, -1, -1, -1, -1],
	[9, 5, 4, 10, 1, 2, 7, 6, 11, -1, -1, -1, -1, -1, -1, -1],
	[6, 11, 7, 1, 2, 10, 0, 8, 3, 4, 9, 5, -1, -1, -1, -1],
	[7, 6, 11, 5, 4, 10, 4, 2, 10, 4, 0, 2, -1, -1, -1, -1],
	[3, 4, 8, 3, 5, 4, 3, 2, 5, 10, 5, 2, 11, 7, 6, -1],
	[7, 2, 3, 7, 6, 2, 5, 4, 9, -1, -1, -1, -1, -1, -1, -1],
	[9, 5, 4, 0, 8, 6, 0, 6, 2, 6, 8, 7, -1, -1, -1, -1],
	[3, 6, 2, 3, 7, 6, 1, 5, 0, 5, 4, 0, -1, -1, -1, -1],
	[6, 2, 8, 6, 8, 7, 2, 1, 8, 4, 8, 5, 1, 5, 8, -1],
	[9, 5, 4, 10, 1, 6, 1, 7, 6, 1, 3, 7, -1, -1, -1, -1],
	[1, 6, 10, 1, 7, 6, 1, 0, 7, 8, 7, 0, 9, 5, 4, -1],
	[4, 0, 10, 4, 10, 5, 0, 3, 10, 6, 10, 7, 3, 7, 10, -1],
	[7, 6, 10, 7, 10, 8, 5, 4, 10, 4, 8, 10, -1, -1, -1, -1],
	[6, 9, 5, 6, 11, 9, 11, 8, 9, -1, -1, -1, -1, -1, -1, -1],
	[3, 6, 11, 0, 6, 3, 0, 5, 6, 0, 9, 5, -1, -1, -1, -1],
	[0, 11, 8, 0, 5, 11, 0, 1, 5, 5, 6, 11, -1, -1, -1, -1],
	[6, 11, 3, 6, 3, 5, 5, 3, 1, -1, -1, -1, -1, -1, -1, -1],
	[1, 2, 10, 9, 5, 11, 9, 11, 8, 11, 5, 6, -1, -1, -1, -1],
	[0, 11, 3, 0, 6, 11, 0, 9, 6, 5, 6, 9, 1, 2, 10, -1],
	[11, 8, 5, 11, 5, 6, 8, 0, 5, 10, 5, 2, 0, 2, 5, -1],
	[6, 11, 3, 6, 3, 5, 2, 10, 3, 10, 5, 3, -1, -1, -1, -1],
	[5, 8, 9, 5, 2, 8, 5, 6, 2, 3, 8, 2, -1, -1, -1, -1],
	[9, 5, 6, 9, 6, 0, 0, 6, 2, -1, -1, -1, -1, -1, -1, -1],
	[1, 5, 8, 1, 8, 0, 5, 6, 8, 3, 8, 2, 6, 2, 8, -1],
	[1, 5, 6, 2, 1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[1, 3, 6, 1, 6, 10, 3, 8, 6, 5, 6, 9, 8, 9, 6, -1],
	[10, 1, 0, 10, 0, 6, 9, 5, 0, 5, 6, 0, -1, -1, -1, -1],
	[0, 3, 8, 5, 6, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[10, 5, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[11, 5, 10, 7, 5, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[11, 5, 10, 11, 7, 5, 8, 3, 0, -1, -1, -1, -1, -1, -1, -1],
	[5, 11, 7, 5, 10, 11, 1, 9, 0, -1, -1, -1, -1, -1, -1, -1],
	[10, 7, 5, 10, 11, 7, 9, 8, 1, 8, 3, 1, -1, -1, -1, -1],
	[11, 1, 2, 11, 7, 1, 7, 5, 1, -1, -1, -1, -1, -1, -1, -1],
	[0, 8, 3, 1, 2, 7, 1, 7, 5, 7, 2, 11, -1, -1, -1, -1],
	[9, 7, 5, 9, 2, 7, 9, 0, 2, 2, 11, 7, -1, -1, -1, -1],
	[7, 5, 2, 7, 2, 11, 5, 9, 2, 3, 2, 8, 9, 8, 2, -1],
	[2, 5, 10, 2, 3, 5, 3, 7, 5, -1, -1, -1, -1, -1, -1, -1],
	[8, 2, 0, 8, 5, 2, 8, 7, 5, 10, 2, 5, -1, -1, -1, -1],
	[9, 0, 1, 5, 10, 3, 5, 3, 7, 3, 10, 2, -1, -1, -1, -1],
	[9, 8, 2, 9, 2, 1, 8, 7, 2, 10, 2, 5, 7, 5, 2, -1],
	[1, 3, 5, 3, 7, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[0, 8, 7, 0, 7, 1, 1, 7, 5, -1, -1, -1, -1, -1, -1, -1],
	[9, 0, 3, 9, 3, 5, 5, 3, 7, -1, -1, -1, -1, -1, -1, -1],
	[9, 8, 7, 5, 9, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[5, 8, 4, 5, 10, 8, 10, 11, 8, -1, -1, -1, -1, -1, -1, -1],
	[5, 0, 4, 5, 11, 0, 5, 10, 11, 11, 3, 0, -1, -1, -1, -1],
	[0, 1, 9, 8, 4, 10, 8, 10, 11, 10, 4, 5, -1, -1, -1, -1],
	[10, 11, 4, 10, 4, 5, 11, 3, 4, 9, 4, 1, 3, 1, 4, -1],
	[2, 5, 1, 2, 8, 5, 2, 11, 8, 4, 5, 8, -1, -1, -1, -1],
	[0, 4, 11, 0, 11, 3, 4, 5, 11, 2, 11, 1, 5, 1, 11, -1],
	[0, 2, 5, 0, 5, 9, 2, 11, 5, 4, 5, 8, 11, 8, 5, -1],
	[9, 4, 5, 2, 11, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[2, 5, 10, 3, 5, 2, 3, 4, 5, 3, 8, 4, -1, -1, -1, -1],
	[5, 10, 2, 5, 2, 4, 4, 2, 0, -1, -1, -1, -1, -1, -1, -1],
	[3, 10, 2, 3, 5, 10, 3, 8, 5, 4, 5, 8, 0, 1, 9, -1],
	[5, 10, 2, 5, 2, 4, 1, 9, 2, 9, 4, 2, -1, -1, -1, -1],
	[8, 4, 5, 8, 5, 3, 3, 5, 1, -1, -1, -1, -1, -1, -1, -1],
	[0, 4, 5, 1, 0, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[8, 4, 5, 8, 5, 3, 9, 0, 5, 0, 3, 5, -1, -1, -1, -1],
	[9, 4, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[4, 11, 7, 4, 9, 11, 9, 10, 11, -1, -1, -1, -1, -1, -1, -1],
	[0, 8, 3, 4, 9, 7, 9, 11, 7, 9, 10, 11, -1, -1, -1, -1],
	[1, 10, 11, 1, 11, 4, 1, 4, 0, 7, 4, 11, -1, -1, -1, -1],
	[3, 1, 4, 3, 4, 8, 1, 10, 4, 7, 4, 11, 10, 11, 4, -1],
	[4, 11, 7, 9, 11, 4, 9, 2, 11, 9, 1, 2, -1, -1, -1, -1],
	[9, 7, 4, 9, 11, 7, 9, 1, 11, 2, 11, 1, 0, 8, 3, -1],
	[11, 7, 4, 11, 4, 2, 2, 4, 0, -1, -1, -1, -1, -1, -1, -1],
	[11, 7, 4, 11, 4, 2, 8, 3, 4, 3, 2, 4, -1, -1, -1, -1],
	[2, 9, 10, 2, 7, 9, 2, 3, 7, 7, 4, 9, -1, -1, -1, -1],
	[9, 10, 7, 9, 7, 4, 10, 2, 7, 8, 7, 0, 2, 0, 7, -1],
	[3, 7, 10, 3, 10, 2, 7, 4, 10, 1, 10, 0, 4, 0, 10, -1],
	[1, 10, 2, 8, 7, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[4, 9, 1, 4, 1, 7, 7, 1, 3, -1, -1, -1, -1, -1, -1, -1],
	[4, 9, 1, 4, 1, 7, 0, 8, 1, 8, 7, 1, -1, -1, -1, -1],
	[4, 0, 3, 7, 4, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[4, 8, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[9, 10, 8, 10, 11, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[3, 0, 9, 3, 9, 11, 11, 9, 10, -1, -1, -1, -1, -1, -1, -1],
	[0, 1, 10, 0, 10, 8, 8, 10, 11, -1, -1, -1, -1, -1, -1, -1],
	[3, 1, 10, 11, 3, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[1, 2, 11, 1, 11, 9, 9, 11, 8, -1, -1, -1, -1, -1, -1, -1],
	[3, 0, 9, 3, 9, 11, 1, 2, 9, 2, 11, 9, -1, -1, -1, -1],
	[0, 2, 11, 8, 0, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[3, 2, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[2, 3, 8, 2, 8, 10, 10, 8, 9, -1, -1, -1, -1, -1, -1, -1],
	[9, 10, 2, 0, 9, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[2, 3, 8, 2, 8, 10, 0, 1, 8, 1, 10, 8, -1, -1, -1, -1],
	[1, 10, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[1, 3, 8, 9, 1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[0, 9, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[0, 3, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

	#check cube to generate cube index
	#list of indexes that are inside the surface
	cube_index = 0
	if(values[0] == 0):
		cube_index += 1
	if(values[1] == 0):
		cube_index += 2
	if(values[2] == 0):
		cube_index += 4
	if(values[3] == 0):
		cube_index += 8
	if(values[4] == 0):
		cube_index += 16
	if(values[5] == 0):
		cube_index += 32
	if(values[6] == 0):
		cube_index += 64
	if(values[7] == 0):
		cube_index += 128

	#check if cube actually intersects with surface mesh
	if(edgeTable[cube_index] == 0):
		return None

	#find vertices for which surface intersects cube
	if(edgeTable[cube_index] & 1):
		vert_list[0] = PointInterp(points[0], points[1])
		

	if(edgeTable[cube_index] & 2):
		vert_list[1] = PointInterp(points[1], points[2]) 

	if(edgeTable[cube_index] & 4):
		vert_list[2] = PointInterp(points[2], points[3])

	if(edgeTable[cube_index] & 8):
		vert_list[3] = PointInterp(points[3], points[0])

	if(edgeTable[cube_index] & 16):
		vert_list[4] = PointInterp(points[4], points[5])

	if(edgeTable[cube_index] & 32):
		vert_list[5] = PointInterp(points[5], points[6])

	if(edgeTable[cube_index] & 64):
		vert_list[6] = PointInterp(points[6], points[7])

	if(edgeTable[cube_index] & 128):
		vert_list[7] = PointInterp(points[7], points[4])

	if(edgeTable[cube_index] & 256):
		vert_list[8] = PointInterp(points[0], points[4])

	if(edgeTable[cube_index] & 512):
		vert_list[9] = PointInterp(points[1], points[5])

	if(edgeTable[cube_index] & 1024):
		vert_list[10] = PointInterp(points[2], points[6])

	if(edgeTable[cube_index] & 2048):
		vert_list[11] = PointInterp(points[3], points[7])

	# create triangles
	i = 0
	triangles= []

	while(triTable[cube_index][i] != -1):
		new_triangle = Facet(
							[vert_list[triTable[cube_index][i]], 
							vert_list[triTable[cube_index][i+1]],
							vert_list[triTable[cube_index][i+2]]])

		triangles.append(new_triangle)
		i+=3

	return triangles

def PointInterp(p1, p2):
	x = round((p1[0]+p2[0])/2.0, 8)
	y = round((p1[1]+p2[1])/2.0, 8)
	z = round((p1[2]+p2[2])/2.0, 8)
	return[x,y,z]


if __name__ == '__main__':
	start_time = time.time()
	mySTL = stl.SimpleSTL('test1')
	generator = CubeGrid(fn.sine_grid, [200,200,200], [0,0,0], 0.05)

	nextCube = generator.SpawnSequentialCube()

	while nextCube is not None:
		#print nextCube
		newMeshes = MarchingCubes(nextCube[0], nextCube[1])
		
		nextCube = generator.SpawnSequentialCube()
		if(newMeshes is not None):
			#print "yay"
			for new in newMeshes:
				mySTL.addFacet(new)
	mySTL.ExportBinSTL()
	#print generator.Solutions
	print("--- %s seconds ---" % (time.time() - start_time))





