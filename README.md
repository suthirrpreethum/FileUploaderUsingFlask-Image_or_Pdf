
The Website will be helpful for uploading Image or Pdf:
  1. Upload Image/PDF document (Max size: 2MB)
    i)   Allowed image formats are .png, .jpg and .jpeg
    ii)  Allowed document format is pdf only
  2. Provide thumbnail image of the uploaded file on the same page with properties button and delete button.
  3. Properties Include
    In case of image file:
    
      ○ Creation date
      ○ Modification Date
      ○ File size and image resolution
      ○ Average mean of RGB
  
    In case of pdf file:
    
      ○ Creation date
      ○ Modification Date
      ○ File size & Paper size
      ○ Total Number of Words in the file
      ○ Total number of lines in the file
  4. Auto delete file after 5 minutes


autoDelete.py is scheduled with the crontab shell to move the images to the backupFolder and the backup folder is cleared at the end of each hour
