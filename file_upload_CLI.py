from __future__ import print_function
from httplib2 import Http
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload,MediaIoBaseDownload
import sys
import io
import pickle
import os.path

#establish connection and authorize, returns drive API object
def login():
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = None
    #token.pickle used for storing your auth data
    #so you don't need to relogin every time
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json',
                                                             SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)
    return service

#uploads the chosen file to the drive
#this function uses as little as possible metadata so it won't mess up anything
def upload(drive_service, filepath):
    #creating metadata
    file_metadata = {
        'name': filepath.split('/')[-1],
        'mimeType': '*/*'
        }
    #creating file content using MediaFileUpload instance
    media = MediaFileUpload(filepath,
                            mimetype='*/*',
                            resumable=True)
    #creating the file on disk
    #if there is a file with the same name, duplicate will be created
    drive_service.files().create(body=file_metadata, media_body=media,
                                  fields='id').execute()
    

#updating existing file on disk
#doing pretty much the same as what upload function does
def update (drive_service, filepath, results):
    file_metadata = {
        'name': filepath.split('/')[-1],
        'mimeType': '*/*'
    }
    media = MediaFileUpload(filepath,
                            mimetype='*/*',
                            resumable=True)
    drive_service.files().update(fileId=list(list(results.values())[0][0].values())[0],
                                 body=file_metadata, media_body=media).execute()
    



file_path = sys.argv[1]
if os.path.exists(file_path) and os.path.isfile(file_path):
    filename = file_path.split(os.path.sep)[-1]
    serv = login()
    #check if file exists
    results = serv.files().list(q=f"name='{filename}'",
                                   fields='nextPageToken, files(id)').execute()
    #got a strange bug(?) here, only file it can find at all is some .mkv,
    #other seem to not exist for the script
    if len(list(results.values())[0]) >= 1:
        print(f"Updating file {file_path}")
        update(serv, file_path, results)
        print('Finished updating')
    else:
        print(f"Uploading file {file_path}")
        upload(serv, file_path)
        print('Finished uploading')
else:
    print(f"Can't find file {file_path}")
    quit()
