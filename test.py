import cv2
import os 
import imutils

def printTest(directoryName, filename):
	print("test script called")
	newImg = cv2.imread(directoryName+filename)
	gray = cv2.cvtColor(newImg, cv2.COLOR_BGR2GRAY)
	filename, file_extension = os.path.splitext(filename)
	print(filename)
	newFileName = 'processedImg'+ '_' + filename + file_extension
	print(newFileName)
	cv2.imwrite(directoryName+newFileName, gray)

	return newFileName

if __name__=='__main__':
	printTest()