import math

#stl object

class SimpleSTL:

	facetList = []
	name = "None"

	def __init__(self, name):
		self.name = name

	def ExportSTL(self):
		f = open((self.name + '.stl'), 'w')
		#
		f.write('solid ' + self.name + '\n')
		for facet in self.facetList:
			f.write('facet normal ' + str(facet.unit_norm[0]) + ' ' + str(facet.unit_norm[1]) + ' ' + str(facet.unit_norm[2]) + '\n')
			f.write('outer loop\n')
			f.write('	vertex ' + str(facet.V1[0]) + ' ' + str(facet.V1[1]) + ' ' + str(facet.V1[2]) + '\n')
			f.write('	vertex ' + str(facet.V2[0]) + ' ' + str(facet.V2[1]) + ' ' + str(facet.V2[2]) + '\n')
			f.write('	vertex ' + str(facet.V3[0]) + ' ' + str(facet.V3[1]) + ' ' + str(facet.V3[2]) + '\n')
			f.write('endloop\n')
			f.write('endfacet\n')
		f.write('endsolid\n')
		f.close()
	def addFacet(self, facet):
		self.facetList.append(facet)

	def exportBinSTL(self):
		#80 byte header

		#4 byte long int (number of facets)

		#normal and 3 edges. each as three 4 byte floats, 2 byte empty spacer (50 bytes each facet)
		pass


