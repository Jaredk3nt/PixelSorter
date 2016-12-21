import sys, getopt
from PIL import Image

def displayImage(image):
	image.show()

def sortImage(pixels):
	sortHelper(0, len(pixels) - 1, pixels)

#quicksort on the image
def sortHelper(lowIndex, highIndex, pixels):
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
		sortHelper(lowIndex, high, pixels)
	if (highIndex > low):
		sortHelper(low, highIndex, pixels)

#swap helper function for swapping pixels in sort
def swap(i, j, pixels):
	temp = pixels[i]
	pixels[i] = pixels[j]
	pixels[j] = temp

def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv, "hi:o:", ["ifile=","ofile="])
	except getopt.GetoptError:
		print 'test.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	im = Image.open(inputfile)
	pixels = list(im.getdata())
	sortImage(pixels)
	imSorted = Image.new(im.mode, im.size)
	imSorted.putdata(pixels)
	imSorted.save(outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
