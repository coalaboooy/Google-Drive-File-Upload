from __future__ import print_function
from httplib2 import Http
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload,MediaIoBaseDownload
import io
import pickle
import os.path

def login():
    SCOPES = 'https://www.googleapis.com/auth/drive.file'
    creds = None
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

def upload(drive_service, filename):
    file_metadata = {
        'name': filename,
        'mimeType': '*/*'
        }
    media = MediaFileUpload(filename,
                            mimetype='*/*',
                            resumable=True)
    drive_service.files().create(body=file_metadata, media_body=media,
                                  fields='id').execute()
    print ('Succesfully uploaded file to Google Drive, go check it out!')

def update (drive_service, filename):
    results = drive_service.files().list(q=f"name='{filename}'",
                                   fields='nextPageToken, files(id)').execute()
    if not results.get('files'):
        print('No files found on drive')
    elif len(list(results.values())[0]) > 1:
        print('More than one file found on drive')
    else:
        file_metadata = {
        'name': filename,
        'mimeType': '*/*'
        }
        media = MediaFileUpload(filename,
                                mimetype='*/*',
                                resumable=True)
        drive_service.files().update(fileId=list(list(results.values())[0][0].values())[0],
                                     body=file_metadata, media_body=media).execute()
        print('Succesfully updated file!')
    
def work(serv):
    print('If you want to stop, type \'quit\'')
    if input().lower() == 'quit':
        return 1
    print("Choose the file from a current directory by typing its name and extension:")
    name = input()
    while not os.path.exists(name):
        print('There is no such file in the current directory')
        name = input()
    print('Do you want to upload or update the file? Type the corresponding number:')
    print('1 - Upload. Use this if there is no file with this name, as it will dulicate the existing ones')
    print('2 - Update. Use this if you already have file with the same name')
    option = int(input())
    while option != 1 and option != 2:
        print('Wrong option number entered')
        option = int(input())
    if option == 1:
        func = upload
    elif option == 2:
        func = update
    print(f'File {name} will be ', 'uploaded' if option == 1 else 'updated',
          ', are you sure about that?\nY/N', sep='')
    answer = input().upper()
    while answer != 'Y' and answer != 'N':
        print('Y/N?\n')
        answer = input().upper()
    if answer == 'Y':
        func(serv, name)
    elif answer == 'N':
        print('You\'ll have to enter everything again')
    return 0

serv = login()
while work(serv) == 0:
    pass
