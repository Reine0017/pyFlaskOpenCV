import imutils
import cv2
import os
import numpy as np

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def neuralStyleTransfer(directoryName, filename, selected_style):
	print("style transfer script called")


	# load the neural style transfer model from disk
	print("[INFO] loading style transfer model...")
	target = os.path.join(APP_ROOT, 'static/models/')
	print("neuralStyleTransfer target", target)
	net = cv2.dnn.readNetFromTorch(target + selected_style)

	# load the input image, resize it to have a width of 600 pixels, and
	# then grab the image dimensions
	image = cv2.imread(directoryName+filename)
	image = imutils.resize(image, width=600)
	(h, w) = image.shape[:2]

	# construct a blob from the image, set the input, and then perform a
	# forward pass of the network
	blob = cv2.dnn.blobFromImage(image, 1.0, (w, h),
		(103.939, 116.779, 123.680), swapRB=False, crop=False)
	net.setInput(blob)

	#start = time.time()
	output = net.forward()
	#end = time.time()

	# reshape the output tensor, add back in the mean subtraction, and
	# then swap the channel ordering
	output = output.reshape((3, output.shape[2], output.shape[3]))
	output[0] += 103.939
	output[1] += 116.779
	output[2] += 123.680
	output /= 255.0
	output = output.transpose(1, 2, 0)

	
	# show information on how long inference took
	#print("[INFO] neural style transfer took {:.4f} seconds".format(
	#	end - start))
		
	'''
	# show the images
	cv2.imshow("Input", image)
	cv2.imshow("Output", output)
	cv2.waitKey(0)
	'''
	

	filename, file_extension = os.path.splitext(filename)
	print(filename)
	newFileName = 'processedImg'+ '_' + filename + file_extension
	print(newFileName)
	print(directoryName)
	
	#needs normalization because imread
	output_normed = 255 * (output - output.min()) / (output.max() - output.min())
	np.array(output_normed, np.int)

	cv2.imwrite(directoryName+newFileName, output_normed)
	print(cv2.imwrite(directoryName+newFileName, output_normed))

	return newFileName

if __name__=='__main__':
	neuralStyleTransfer('/Users/fangran/Documents/pyFlaskCV/images/', 'bbq.jpg')