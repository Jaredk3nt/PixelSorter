import sys, getopt
from PIL import Image

def displayImage(image):
	image.show()

# sort the pixels by their hue
def colorSort(pixels):
	start = 0
	end = 0;
	while (end < len(pixels) - 1):
		print("color sorting")
		start = getFirstNonBlack(start, pixels)
		end = getNextBlack(start, pixels)

		if (end < 0):
			break

		quicksortHelper(start, end, pixels)

		start = end + 1

#get the next pixel with a sum greater than 60
def getFirstNonBlack(index, pixels):
	while (rgbsum(pixels[index]) < 60):
		index += 1
		if (index >= len(pixels)):
			return -1
	return index

# get the next pixel with a sum less than 60
def getNextBlack(index, pixels):
	while (rgbsum(pixels[index]) > 60):
		index += 1
		if (index >= len(pixels)):
			return -1
	return index

# return the sum of the rgb values
def rgbsum(color):
	return color[0] + color[1] + color[2]

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
	inputfile = ''
	outputfile = ''
	colorSorting = False
	try:
		opts, args = getopt.getopt(argv, "hci:o:", ["ifile=","ofile="])
	except getopt.GetoptError:
		print 'test.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt == "-c":
			colorSorting = True
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
