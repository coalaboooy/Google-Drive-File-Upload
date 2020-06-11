from __future__ import print_function
from httplib2 import Http
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload,MediaIoBaseDownload
import io
import pickle
import os.path
import tkinter as tk
from tkinter import filedialog

#establish connection and authorize, returns drive API object
def login():
    SCOPES = 'https://www.googleapis.com/auth/drive.file'
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
def upload(drive_service, filename):
    #creating metadata
    file_metadata = {
        'name': filename,
        'mimeType': '*/*'
        }
    #creating file content using MediaFileUpload instance
    media = MediaFileUpload(filename,
                            mimetype='*/*',
                            resumable=True)
    #creating the file on disk
    #if there is a file with the same name, duplicate will be created
    drive_service.files().create(body=file_metadata, media_body=media,
                                  fields='id').execute()
    print('Succesfully uploaded file to Google Drive, go check it out!')

#updating existing file on disk
#doing pretty much the same as what upload function does
def update (drive_service, filename):
    #searching for the file on disk
    results = drive_service.files().list(q=f"name='{filename}'",
                                   fields='nextPageToken, files(id)').execute()
    if not results.get('files'):
        print('No files found on drive')
    #function will update only the first file if there is many,
    #so I decided to prevent confusion
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

#basically an user interface
def work(serv):
    print('If you want to quit application, type \'quit\' now. Anything else to continue.')
    if input().lower() == 'quit':
        return 1
    #creating tkinter root to create file dialog window
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    #and disposing of root so it can be opened again later
    root.destroy()
    if file_path == '':
        print('You haven\'t selected the file')
        return 0
    print('Do you want to upload or update the file? Type the corresponding number:')
    print('1 - Upload. Use this if there is no file with this name, as it will dulicate the existing ones')
    print('2 - Update. Use this if you already have file with the same name')
    option = option_input()
    if option == 1:
        func = upload
    elif option == 2:
        func = update
    print(f'File {file_path} will be ', 'uploaded' if option == 1 else 'updated',
          ', are you sure about that?\nY/N', sep='')
    answer = input().upper()
    while answer != 'Y' and answer != 'N':
        print('Y/N?\n')
        answer = input().upper()
    if answer == 'Y':
        func(serv, file_path)
    elif answer == 'N':
        print('The changes were not applied')
    return 0

#auxiliary function so I don't have to deal with exceptions in work functionn
def option_input():
    try:
        option = int(input())
        while option != 1 and option != 2:
            print('Wrong option number entered')
            option = int(input())
        return option
    except ValueError:
        print('Wrong entry, use listed numbers')
        return option_input()
        
#the main()
serv = login()
while work(serv) == 0:
    pass
