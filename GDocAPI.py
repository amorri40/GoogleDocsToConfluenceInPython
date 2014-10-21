from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools
import httplib2
import os
import argparse

# CLIENT_SECRETS is name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret. You can see the Client ID
# and Client secret on the APIs page in the Cloud Console:
# <https://cloud.google.com/console#/project/83613060314/apiui>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Set up a Flow object to be used for authentication.
# Add one or more of the following scopes. PLEASE ONLY ADD THE SCOPES YOU
# NEED. For more information on using scopes please see
# <https://developers.google.com/+/best-practices>.
FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/drive',
      'https://www.googleapis.com/auth/drive.appdata',
      'https://www.googleapis.com/auth/drive.apps.readonly',
      'https://www.googleapis.com/auth/drive.file',
      'https://www.googleapis.com/auth/drive.metadata.readonly',
      'https://www.googleapis.com/auth/drive.readonly',
      'https://www.googleapis.com/auth/drive.scripts',
    ],
    message=tools.message_if_missing(CLIENT_SECRETS))

def get_html_of_gdoc(gdoc_fileId,http):
  service = discovery.build('drive', 'v2', http=http) # Construct the service object for the interacting with the Drive API.
  try:
    doc_files = service.files()
    doc_file = doc_files.get(fileId=gdoc_fileId).execute()
    export_links = doc_file['exportLinks']
    print export_links
    url=""
    try:
        url = export_links['text/html']
    except:
        url = export_links['application/pdf'].replace('exportFormat=pdf','exportFormat=html')
    resp, gdoc_content = http.request(url, "GET")
    return gdoc_content
  except client.AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run the application to re-authorize")
  return "" # an error occured so just return an empty string

# init returns HTML from a google doc id
def init(doc_id):
    storage = file.Storage('sample.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        # Parser for command-line arguments.
        parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, parents=[tools.argparser])
        flags = parser.parse_args([])
        credentials = tools.run_flow(FLOW, storage,flags)

    http = httplib2.Http()
    http = credentials.authorize(http)
    return get_html_of_gdoc(doc_id,http)