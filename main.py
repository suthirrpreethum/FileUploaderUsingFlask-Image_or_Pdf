

import os , subprocess, datetime, mimetypes,shutil
from flask import Flask, render_template, request, jsonify,redirect

UPLOAD_FOLDER = '/var/www/html/imageUploader/static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/main')
def mainPage():
  return render_template("mainPage.html")
@app.route('/upload')
def upload_file():
    '''hists =[f for f in listdir(UPLOAD_FOLDER+'/uploadedFiles/') if isfile(join(UPLOAD_FOLDER+'/uploadedFiles/', f))]'''
    res=os.listdir(UPLOAD_FOLDER+'/uploadedFiles/')
    hist=os.listdir('/var/www/html/imageUploader/static/uploadedFiles')
    '''print(hist)'''
    return render_template('upload.html',hist=hist)

@app.route('/fileInfo', methods=["POST"])
def fileInfo():
	fileName=request.form['fileName']
	'''print('fileName: '+fileName)'''
	fileDirectory=UPLOAD_FOLDER+'/uploadedFiles/'+fileName
	cmd1="stat "+fileDirectory
	'''stat /home/suthirr/Pictures/hii.jpg'''
	returned_value =subprocess.check_output(cmd1,shell=True)
	'''print('returned value:', returned_value.decode("utf-8"))'''
	cnt=0;
        output={};
	splittedValue=returned_value.decode("utf-8").split('\n')
	for line in splittedValue:
		'''print(cnt, " value", line);'''
		
		if ('Size' in line):
        		line=line.strip()
        		splitForSize=line.split(' ');
        		'''print(splitForSize[0]+' '+splitForSize[1]+' bytes')'''
                        output[' '+splitForSize[0].replace('u\'','')]=' '+splitForSize[1].replace('u\'','')+' bytes'
    		elif(('Modify' in line) or ('Birth' in line)):
        		line=line.strip()
        		splitToGetDate=line.split(' ')
        		splitToGetDate[0]=splitToGetDate[0].replace(':','')
        		if('-'!=splitToGetDate[1]):
        			splitTimeForMillis=splitToGetDate[2].split('.')
        			millis=str(int(splitTimeForMillis[1])/1000);
				date=datetime.datetime.strptime(splitToGetDate[1]+' '+splitTimeForMillis[0],'%Y-%m-%d %H:%M:%S');
				'''print( splitToGetDate[0]+" date: "+date.strftime("%m-%d-%y %H:%M:%S"))'''
                                output[splitToGetDate[0].replace('u\'','')+" date"]=date.strftime("%m-%d-%y %H:%M:%S")
        		else:
				'''print( splitToGetDate[0]+" date: No date found")'''
                                output[splitToGetDate[0].replace('u\'','')+" date"]='No date found'
    		cnt+=1
    		averageRgbHeaderReached= False
	if 'image' in (mimetypes.MimeTypes().guess_type(fileDirectory)[0]):

    		'''identify -verbose /home/suthirr/Pictures/hii.jpg'''
    		'''cmdForImageDetails=['identify','-verbose',fileDirectory]'''
    		cmdForImageDetails="identify -verbose "+fileDirectory
    		outputImageDetails=subprocess.check_output(cmdForImageDetails,shell=True)
    		cnt=0
    		for eachLine in outputImageDetails.decode("utf-8").split('\n'):
        		eachLine=eachLine.strip()
        		'''print(cnt, " value", eachLine)'''
        		if 'Filesize:' in eachLine:
        	    		splitTOGetFileSize=eachLine.split(' ')
        	    		'''print('File size details:', splitTOGetFileSize[1])'''
                                output['File size details']=splitTOGetFileSize[1]
        		elif 'Geometry' in eachLine:
        	    		resolution=eachLine.split(' ')[1].split('+')[0]
        	    		'''print('resolution: ',resolution)'''
                                output['resolution']=resolution
           		elif 'Image statistics' in eachLine:
        	    		averageRgbHeaderReached=True
        		elif averageRgbHeaderReached and 'mean' in eachLine:
        	    		'''print('average RGB:',eachLine.split(' ')[1])'''
                                output['average RGB']=eachLine.split(' ')[1]
        	    		averageRgbHeaderReached=False

        		cnt+=1
	elif 'pdf' in (mimetypes.MimeTypes().guess_type(fileDirectory)[0]):
    		'''print('inside pdf')'''
    		cmdForWordCount = "pdftotext "+fileDirectory+" - | tr -d '.' | wc -w"
    		'''pdftotext test.pdf - | tr -d '.' | wc -w'''
    		wordcount=subprocess.check_output(cmdForWordCount, shell=True)
    		'''print('word count: '+wordcount.decode('utf-8').strip())'''
		output['word count']=wordcount.decode('utf-8').strip()

    		'''qpdf --show-npages test.pdf'''
    		cmdForNoOfPages="qpdf --show-npages "+fileDirectory
    		'''print('No of pages: '+subprocess.check_output(cmdForNoOfPages,shell=True).decode('utf-8'))'''
                outputString=subprocess.check_output(cmdForNoOfPages,shell=True).decode('utf-8')
                output['No of pages']=outputString

    		'''pdftotext -layout test.pdf - | wc -l'''
    		cmdForNoOfLines="pdftotext -layout "+fileDirectory+" - | wc -l"
    		'''print('No of lines: '+subprocess.check_output(cmdForNoOfLines,shell=True).decode('utf-8'))'''
                outputString=subprocess.check_output(cmdForNoOfLines,shell=True).decode('utf-8')
                output['No of lines']=outputString
        '''print(output)'''
        return jsonify(output)

@app.route('/deleteFile', methods=["POST"])
def delete_file():
    fileName=request.form['fileName']
    print('fileName: '+fileName)
    files=os.listdir(UPLOAD_FOLDER+'/backupFiles/')
    IsfilePresent=0
    for file in files:
        if file==fileName:
            IsfilePresent=1
    if IsfilePresent==0:
        shutil.move(UPLOAD_FOLDER+'/uploadedFiles/'+fileName,UPLOAD_FOLDER+'/backupFiles/')
    else:
        os.remove(UPLOAD_FOLDER+'/uploadedFiles/'+fileName);
    '''cmd='sudo mv '+UPLOAD_FOLDER+'/uploadedFiles/'+fileName+' '+UPLOAD_FOLDER+'/backupFiles/';
    returnValue=subprocess.check_output(cmd,shell=True);'''
    return redirect("/upload")

@app.route("/abc")
def abc():
    hist=os.listdir('/var/www/html/imageUploader/static/uploadedFiles')
    '''hist='sssd'''
    print(hist)
    return render_template('abc.html',hist=hist)
    
@app.route("/uploader", methods=["POST"])
def upload():
  targetFile=os.path.join(UPLOAD_FOLDER,"uploadedFiles/")

  if not os.path.isdir(targetFile):
    os.mkdir(targetFile)

  for file in request.files.getlist("file"):
    fileName=file.filename
    if (('.jpg' in fileName) or ('jpeg' in fileName) or ('.png' in fileName) or ('.pdf' in fileName)):
        print(file.filename)
        destination="/".join([targetFile,fileName])
        file.save(destination)
        print(os.path.getsize(destination))
        fileSize=os.path.getsize(destination)
        fileInMb=float(fileSize/1000000)
        if(fileInMb>=2):
            os.remove(destination);
            hist=os.listdir('/var/www/html/imageUploader/static/uploadedFiles')
            return render_template('upload.html',fileSize='False',hist=hist)
        print(fileInMb)
    else:
        print('file type not matching')
        hist=os.listdir('/var/www/html/imageUploader/static/uploadedFiles')
        return render_template('upload.html',fileType='False',hist=hist)
  return redirect("/upload")
  '''hist=os.listdir('/var/www/html/imageUploader/static/uploadedFiles')
  return render_template('upload.html',hist=hist)
  return jsonify(res)
  return render_template("mainPage.html")
  return jsonify(res=file.filename)'''


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
