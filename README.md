This python script lets you upload or update chosen file to your Google Drive.\
\
There is a version without an interface, it works by executing script from your terminal with a path to file next to it. Does not require tkinter module.\
If your filepath contains spaces, place it in the double qoutation marks (")\
To run it, you'll first need to download 'credentials.json' file, which you can do here:\
https://developers.google.com/drive/api/v3/quickstart/python  
\
List of modules used (you'll need to install them to run the script):\
httplib2 - https://pypi.org/project/httplib2/  
googleapiclient - https://pypi.org/project/google-api-python-client/  
google_auth_oauthlib - https://pypi.org/project/google-auth-oauthlib/  
google.auth - https://pypi.org/project/google-auth/  
apiclient - https://pypi.org/project/apiclient/  
Also make sure your io, pickle, tkinter and os.path modules are working properly.\
\
Place the 'credentials.json' file you downloaded to the directory in which script is,
run the script and follow instructions.\
\
Added feature of selecting file from dialog window, now it is possible to choose any file
from any directory.\
Now files on disk will have their name and extension only, without absolute path.
