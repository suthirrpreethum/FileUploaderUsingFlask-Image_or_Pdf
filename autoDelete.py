import os, time, subprocess, mimetypes
from datetime import datetime

Filelist=os.listdir('/var/www/html/imageUploader/static/uploadedFiles')
for file in Filelist:
    print(file)
    fileDirectory='/var/www/html/imageUploader/static/uploadedFiles/'+file
    '''cmd1="stat "+fileDirectory
    
    returned_value =subprocess.check_output(cmd1,shell=True)'''
    FileTimeInmillis=int(round(os.path.getctime(fileDirectory)))
    print('image: ')
    print(FileTimeInmillis)

    currentTimeInMillis = int(round(time.time()))
    print(currentTimeInMillis)
    difference=(currentTimeInMillis/60)-(FileTimeInmillis/60)
    print("difference", difference)
    if(difference>5):
        print(fileDirectory)
        cmd1=os.remove(fileDirectory)
