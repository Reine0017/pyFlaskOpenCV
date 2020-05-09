# Import required packages:
from flask import Flask, request, render_template, send_from_directory, redirect, send_file
import os
import test
import neuralStyleProcess
import cv2

app = Flask(__name__)

#do function that checks for uploaded file types (extensions).
#https://stackoverflow.com/questions/41105700/how-can-i-restrict-the-file-types-a-user-can-upload-to-my-form

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

	data = request.form.get("style")
	print(data)

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

	return render_template("complete.html", image_names=myFiles, selected_style=data)

# in this function send_image will HAVE to take in the parameter name <filename>
@app.route('/upload/<filename>')
def send_original_image(filename):
	return send_from_directory("images", filename)

# this app route cant be the same as above
@app.route('/complete/<filename>/<selected_style>')
def send_processed_image(filename, selected_style):
	directoryName = os.path.join(APP_ROOT, 'images/')

	newImg = neuralStyleProcess.neuralStyleTransfer(directoryName, filename, selected_style)
	
	return send_from_directory("images", newImg)


#good practise to have this: this means this will only run if its run directly (and not called from somewhere else)
if __name__ == "__main__":
	#remove debug and host when hosting to cloud
	# Add parameter host='0.0.0.0' to run on your machines IP address:
	app.run(host='0.0.0.0')


