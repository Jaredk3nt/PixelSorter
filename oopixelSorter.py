import sys, getopt
from PIL import Image

# make ENUM for sorttypes
# lightness = 0, saturation = 1 etc...

class PixelSorter:
	def __init__(self, inf):
		# the various thresholds for sorts
		self.HThreshold = 50
		self.SThreshold = 0.1
		self.LThreshold = 0.2

		self.inputfile = inf

		self.im = Image.open(self.inputfile)
		self.pixels = list(self.im.getdata())

	def saveImage(self):
		imSorted = Image.new(self.im.mode, self.im.size)
		imSorted.putdata(self.pixels)
		imSorted.save("sorts/new.jpg")

	def displayImage(self):
		self.im.show()

	# use a lightness value based sort
	def lightnessSort(self):
		self.sortImage(0)

	# use a saturation based sort
	def saturationSort(self):
		self.sortImage(1)

	# use a hue based sort
	def hueSort(self):
		self.sortImage(2)

	# sort the image by the desired method
	def sortImage(self, mode):
		start = 0
		end = 0
		while (end < len(self.pixels) - 1):
			start = self.getNextStart(start, mode)
			end = self.getNextEnd(start, mode)
			if (end < 0):
				break

			self.quicksortHelper(start, end)

			start = end + 1

	#get the next pixel with a sum greater than 60
	def getNextStart(self, index, mode):
		# find the mode being used currently
		threshold = self.findThreshold(mode)

		while (self.findValue(index, mode) < threshold):
			index += 1
			if (index >= len(self.pixels)):
				return -1
		return index

	# get the next pixel with a sum less than 60
	def getNextEnd(self, index, mode):
		value = 0
		colorThreshold = 0
		# find the mode being used currently
		threshold = self.findThreshold(mode)

		while (self.findValue(index, mode) > threshold):
			index += 1
			if (index >= len(self.pixels)):
				return -1
		return index

	# determine the pixels "value" based on the current mode
	def findValue(self, index, mode):
		value = 0
		if(mode == 0 or mode == 1 or mode == 2):
			value = self.findHSL(index, mode)
		else:
			#for now since there is nothing else
			value = self.findHSL(index, mode)
		return value

	# determine the threshold to be used on current sort
	def findThreshold(self, mode):
		threshold = 0
		if(mode == 0):
			threshold = self.LThreshold
		else:
			threshold = self.SThreshold
		return threshold

	# find HSL values for the RGB color
	def findHSL(self, index, mode):
		color = self.pixels[index]
		r = color[0]/255.0
		g = color[1]/255.0
		b = color[2]/255.0
		maxValue = max(r, g, b)
		minValue = min(r, g, b)
		l = (maxValue + minValue)/2.0
		# if lightness mode return l
		if (mode == 0):
			#print(l)
			return l
		# otherwise we use it to find the other values
		s = 0
		if (l > 0.5):
			s = (maxValue - minValue)/(2.0 - (maxValue - minValue))
		else:
			top = maxValue - minValue
			bottom = maxValue + minValue
			if (bottom == 0):
				s = 1.0
			else:
				s = (maxValue - minValue)/(maxValue + minValue)
		if (mode == 1):
			return s
		h = 0
		#determine which of the values in the max
		bottom = ((maxValue - minValue))
		if(bottom <= 0):
			bottom = 0.000001
		if (r > g and r > b):
			h = (g - b)/bottom
		elif (g > r and g > b):
			h = (2.0 + (b - r))/bottom
		else:
			h = (4.0 + (r - g))/bottom
		#convert to degrees
		h *= 60
		if (h < 0):
			h += 360
		return h

	def quicksortImage(self):
		self.quicksortHelper(0, len(self.pixels) - 1)

	#quicksort on the image
	def quicksortHelper(self, lowIndex, highIndex):
		low = lowIndex
		high = highIndex
		pivot = self.pixels[lowIndex+(highIndex-lowIndex)/2]

		while (low <= high):
			while (self.pixels[low] < pivot):
				low+= 1
			while (self.pixels[high] > pivot):
				high-= 1
			if (low <= high):
				self.swap(low, high)
				low+= 1;
				high-= 1;

		if (lowIndex < high):
			self.quicksortHelper(lowIndex, high)
		if (highIndex > low):
			self.quicksortHelper(low, highIndex)

	#swap helper function for swapping pixels in sort
	def swap(self, i, j):
		temp = self.pixels[i]
		self.pixels[i] = self.pixels[j]
		self.pixels[j] = temp

	def updateLThreshold(self, value):
		self.LThreshold = value

	def updateSThreshold(self, value):
		self.SThreshold = value

	def updateHThreshold(self, value):
		self.HThreshold = value


psorter = PixelSorter("data/picture.jpg")
psorter.hueSort()
psorter.saveImage()
