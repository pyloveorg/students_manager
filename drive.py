# from main import app
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
#
# @app.route('/drive', methods=['GET'])
# def drive():
#     gauth = GoogleAuth()
#     gauth.LocalWebserverAuth()
#     drive = GoogleDrive(gauth)
#     file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
#     print(file_list)
#     for file1 in file_list:
#         print('title: %s, id: %s' % (file1['title'], file1['id']))
#

# from pydrive.drive import GoogleDrive
# from pydrive.auth import GoogleAuth
# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()
# drive = GoogleDrive(gauth)
#
# file1 = drive.CreateFile({'title': 'Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
# file1.SetContentString('Hello World!') # Set content of the file from given string.
# file1.Upload()