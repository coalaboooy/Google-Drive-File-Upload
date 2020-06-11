This python script lets you upload or update chosen file to your Google Drive.\
\
To run it, you'll first need to download 'credentials.json' file, which you can do here:\
https://developers.google.com/drive/api/v3/quickstart/python  
\
List of modules used (you'll need to install them to run the script):
httplib2 - https://pypi.org/project/httplib2/  
googleapiclient - https://pypi.org/project/google-api-python-client/  
google_auth_oauthlib - https://pypi.org/project/google-auth-oauthlib/  
google.auth - https://pypi.org/project/google-auth/  
apiclient - https://pypi.org/project/apiclient/  
Also make sure your io, pickle and os.path modules are working properly.\
\
Place the 'credentials.json' file you downloaded and the file you want to upload to the
directory in which script is, run the script and follow instructions.\
\
Currently working on feature to select file from dialog window.