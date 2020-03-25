'''
# Import required packages:
import cv2
from flask import Flask, request, make_response
import numpy as np
import urllib.request

app = Flask(__name__)


@app.route('/canny', methods=['GET'])
def canny_processing():
    # Get the image:
	with urllib.request.urlopen(request.args.get('url')) as url:
		image_array = np.asarray(bytearray(url.read()), dtype=np.uint8)

	# Convert the image to OpenCV format:
	img_opencv = cv2.imdecode(image_array, -1)

	# Convert image to grayscale:
	gray = cv2.cvtColor(img_opencv, cv2.COLOR_BGR2GRAY)

	# Perform canny edge detection:
	edges = cv2.Canny(gray, 100, 200)

	# Compress the image and store it in the memory buffer:
	retval, buffer = cv2.imencode('.jpg', edges)

	# Build the response:
	response = make_response(buffer.tobytes())
	response.headers['Content-Type'] = 'image/jpeg'

	    # Return the response:
	return response


if __name__ == "__main__":
	# Add parameter host='0.0.0.0' to run on your machines IP address:
	app.run(host='0.0.0.0', debug=True)

'''
# Import required packages:
import cv2
from flask import Flask, request, render_template, send_from_directory, redirect
import os
import test

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
	return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
	target = os.path.join(APP_ROOT, 'images/')
	print("TARGET", target)

	if not os.path.isdir(target):
		os.mkdir(target)
	else:
		print("Couldn't create upload directory: {}".format(target))

	for file in request.files.getlist("file"):
		print("file", file)
		filename = file.filename
		print("filename", filename)
		destination = "/".join([target, filename])
		print("destination", destination)
		file.save(destination)
		#prints - birthday-party.png (e.g.)
		print("!!!!!!!!filename", filename)

	return render_template("complete.html", image_name=filename)

@app.route('/upload/<filename>')
def send_image(filename):
	print("!!!!!!!!!!!!!!!!")
	print("!!!!!filename",filename)
	directoryName = os.path.join(APP_ROOT, 'images/')

	newImg = test.printTest(directoryName, filename)
	print(newImg)
	#newImg = test.printTest(fullpath)
	#return send_from_directory("images",newImg)
	return send_from_directory("images",newImg)



#good practise to have this: this means this will only run if its run directly (and not called from somewhere else)
if __name__ == "__main__":
	# Add parameter host='0.0.0.0' to run on your machines IP address:
	app.run(host='0.0.0.0', debug=True)


