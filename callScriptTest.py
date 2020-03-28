import neuralStyleProcess

def testingFunction(directoryName, filename):
	neuralStyleProcess.neuralStyleTransfer(directoryName,filename)


if __name__=='__main__':
	testingFunction('/Users/fangran/Documents/pyFlaskCV/images/', 'bbq.jpg')