# Import required packages:
import cv2
from flask import Flask, request, render_template, send_from_directory, redirect, send_file
import os
import test
import neuralStyleProcess
import time

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

	myFiles = []

	for file in request.files.getlist("file"):
		print("file", file)
		filename = file.filename
		print("filename", filename)
		destination = "".join([target, filename])
		print("destination", destination)
		file.save(destination)
		myFiles.append(filename)
	print(myFiles)

	return render_template("complete.html", image_names=myFiles)

# in this function send_image will HAVE to take in the parameter name <filename>
@app.route('/upload/<filename>')
def send_original_image(filename):
	return send_from_directory("images", filename)

# this app route cant be the same as above
@app.route('/complete/<filename>')
def send_processed_image(filename):
	print("@@@@@@@@###########")
	print("TEST SCRIPT CALLED")
	directoryName = os.path.join(APP_ROOT, 'images/')

	#newImg = test.printTest(directoryName, filename)
	newImg = neuralStyleProcess.neuralStyleTransfer(directoryName, filename)
	print(filename)

	print(newImg)
	return send_from_directory("images", newImg)
	#return send_file(directoryName+newImg, as_attachment=True)


#good practise to have this: this means this will only run if its run directly (and not called from somewhere else)
if __name__ == "__main__":
	# Add parameter host='0.0.0.0' to run on your machines IP address:
	app.run(host='0.0.0.0', debug=True)


