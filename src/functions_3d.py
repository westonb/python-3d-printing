import math

#test functions

def circle_grid(point):
	[x,y,z] = point
	if bounds(point) == 0:
		return 0

def square_grid(point):
	[x,y,z] = point
	if bounds(point) == 0:
		return 0
	dist = min((x%2), (y%2))
	if dist <0.4:
		return 1
	else:
		return 0
def cube_grid(point):
	[x,y,z] = point
	x = round(x,8)
	y = round(y,8)
	z = round(z,8)
	#x = round(x-0.5,8) 
	#y = round(y-0.5,8)
	#z = round(z,8)

	width = 0.4
	spacing = 2.1
	if bounds(point) == 0:
		return 0
	if(((x%spacing)<width) and ((y%spacing)<width)):
		return 1
	elif(z%spacing)<width and (x%spacing)<width:
		return 1
	elif(z%spacing)<width and (y%spacing)<width:
		return 1
	else:
		return 0

def sine_grid(point):
	[x,y,z] = point
	x = round(x,8)
	y = round(y,8)
	z = round(z,8) 
	
	if bounds([x,y,z]) == 0:
		return 0

	#if(abs(math.sin(x)*math.cos(y)*math.cos(z))>0.2):
	if((math.cos(y*2.) * math.sin(x*2.))<0.2):
		if((math.cos(y*2.) * math.cos(z*2.))<0.2):
			if((math.cos(x*2.) * math.cos(z*2.))<0.2):
				return 1
	
	return 0

def test3(point):
	[x,y,z] = point
	width = 0.4
	spacing = 1.1
	if bounds(point) == 0:
		return 0
	if(round(y,8) >0.5) or (round(z,8)>0.5):
		return 0
	if (abs(round(x,8)-spacing) < width):
		return 1

	else:
		return 0

def bounds(point):
	[x,y,z] = point
	max_size = 7.5
	if( (x<=.5) or (y<=.5) or (z<=0.01)):
		return 0
	#upper bound
	elif ((x>(max_size-1.6)) or (y>(max_size-1.6)) or (z>(max_size-1.6))):
		return 0
	else: 
		return 1

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