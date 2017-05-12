import sys, getopt, time
from oopixelSorter import PixelSorter

def main(argv):
	
	try:
		opts, args = getopt.getopt(argv, ':hlsd', ['hue','saturation','lightness', 'display'])
	except getopt.GetoptError:
		print 'test.py <inputfile> <outputfile>'
		sys.exit(2)
	# grab in the input and outpul file paths
	ifile = args[0]
	ofile = args[1]
	# find the mode of sorting
	mode = -1
	display = False
	for arg in args:
		if arg in ('-h', '--hue'):
			mode = 2
		elif arg in ('-l', '--lightness'):
			mode = 0
		elif arg in ('-s', '--saturation'):
			mode = 1
		elif arg in ('-d', '--display'):
			display = True
	
	#start = time.time()
	pxlsrt = PixelSorter(ifile)
	if (mode == 0):
		pxlsrt.lightnessSort()
	elif (mode == 1):
		pxlsrt.saturationSort()
	elif (mode == 2):
		pxlsrt.hueSort()
	else:
		pxlsrt.quicksortImage()

	pxlsrt.saveImage(ofile)
	if(display):
		pxlsrt.displayImage(ofile)

	#end = time.time()
	#print(end - start)


if __name__ == '__main__':
    main(sys.argv[1:])
