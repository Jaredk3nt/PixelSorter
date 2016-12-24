import sys, getopt
from PIL import Image

#define different thresholds
SThreshold = 0.1
LThreshold = 0.2
mode = 0

def displayImage(image):
	image.show()

# sort the pixels by their hue
def colorSort(pixels):
	start = 0
	end = 0
	while (end < len(pixels) - 1):
		start = getNextStart(start, pixels)
		end = getNextEnd(start, pixels)
		if (end < 0):
			break

		quicksortHelper(start, end, pixels)

		start = end + 1

#get the next pixel with a sum greater than 60
def getNextStart(index, pixels):
	# find the mode being used currently
	threshold = findThreshold()

	while (findHSL(pixels[index]) < threshold):
		index += 1
		if (index >= len(pixels)):
			return -1
	return index

# get the next pixel with a sum less than 60
def getNextEnd(index, pixels):
	value = 0
	colorThreshold = 0
	# find the mode being used currently
	threshold = findThreshold()

	while (findHSL(pixels[index]) > threshold):
		index += 1
		if (index >= len(pixels)):
			return -1
	return index

def findValue(index, pixels):
	value = 0
	if(mode == 0 or mode == 1):
		value = findHSL(pixels[index])
	else:
		#for now since there is nothing else
		value = findHSL(pixels[index])
	return value

def findThreshold():
	threshold = 0
	if(mode == 0):
		threshold = LThreshold
	else:
		threshold = SThreshold
	return threshold

# find HSL values for the RGB color
def findHSL(color):
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
	return s

def quicksortImage(pixels):
	quicksortHelper(1000, len(pixels) - 1000, pixels)

#quicksort on the image
def quicksortHelper(lowIndex, highIndex, pixels):
	low = lowIndex
	high = highIndex
	pivot = pixels[lowIndex+(highIndex-lowIndex)/2]

	while (low <= high):
		while (pixels[low] < pivot):
			low+= 1
		while (pixels[high] > pivot):
			high-= 1
		if (low <= high):
			swap(low, high, pixels)
			low+= 1;
			high-= 1;

	if (lowIndex < high):
		quicksortHelper(lowIndex, high, pixels)
	if (highIndex > low):
		quicksortHelper(low, highIndex, pixels)

#swap helper function for swapping pixels in sort
def swap(i, j, pixels):
	temp = pixels[i]
	pixels[i] = pixels[j]
	pixels[j] = temp

def main(argv):
	global mode
	inputfile = ''
	outputfile = ''
	colorSorting = False
	try:
		opts, args = getopt.getopt(argv, "hlsi:o:", ["ifile=","ofile="])
	except getopt.GetoptError:
		print 'test.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt == "-l":
			colorSorting = True
		elif opt == "-s":
			colorSorting = True
			mode = 1
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	im = Image.open(inputfile)
	pixels = list(im.getdata())

	if (colorSorting):
		colorSort(pixels)
	else:
		quicksortImage(pixels)
	imSorted = Image.new(im.mode, im.size)
	imSorted.putdata(pixels)
	imSorted.save(outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
