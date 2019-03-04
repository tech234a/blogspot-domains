import pickle, os, re, time, datetime, signal, requests, pydrive, tldextract, heroku3
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from time import sleep

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class GracefulKiller:
    kill_now = False
    def __init__(self):
        #self.listindex = None
        #self.pagenumber = None
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self,signum, frame):
        self.kill_now = True

    #print "End of the program. I was killed gracefully :)"

def getcell(cellloc):

        # The ID and range of a sample spreadsheet.
    spreadsheet_id = os.environ['memsheetid']
    range_name = 'Sheet1!A1:A'


    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    # The ID of the spreadsheet to update.
    spreadsheet_id = os.environ['memsheetid']  # TODO: Update placeholder value.

    # The A1 notation of the values to update.
    range_ = 'Sheet1!'+cellloc  # TODO: Update placeholder value.

    # How the input data should be interpreted.
    value_render_option = 'RAW'  # TODO: Update placeholder value.

    request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_) #, valueRenderOption=value_render_option, dateTimeRenderOption=date_time_render_option)
    response = request.execute()
    #print(response)
    return response['values'][0][0]

def updatecells(cellloc, value):

    # The ID and range of a sample spreadsheet.
    #spreadsheet_id = os.environ['memsheetid']
    #range_name = 'Sheet1!A1:A'


    #"""Shows basic usage of the Sheets API.
    #Prints values from a sample spreadsheet.
    #"""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    # The ID of the spreadsheet to update.
    spreadsheet_id = os.environ['memsheetid']  # TODO: Update placeholder value.

    # The A1 notation of the values to update.
    range_ = 'Sheet1!'+cellloc  # TODO: Update placeholder value.

    # How the input data should be interpreted.
    value_input_option = 'RAW'  # TODO: Update placeholder value.

    value_range_body = {
            'values': [[str(value)]]
    }

    request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()

    
def savestate(v1, v2):

    # The ID and range of a sample spreadsheet.
    #spreadsheet_id = os.environ['memsheetid']
    #range_name = 'Sheet1!A1:A'


    #"""Shows basic usage of the Sheets API.
    #Prints values from a sample spreadsheet.
    #"""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    # The ID of the spreadsheet to update.
    spreadsheet_id = os.environ['memsheetid']  # TODO: Update placeholder value.

    # The A1 notation of the values to update.
    range_ = 'Sheet1!A1:A2' #+cellloc  # TODO: Update placeholder value.

    # How the input data should be interpreted.
    value_input_option = 'RAW'  # TODO: Update placeholder value.

    value_range_body = {
            'values': [[str(v1)], [str(v2)]]
    }

    request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()    

def appendtosheet(inlist):
    mylist = [str(datetime.datetime.now()).split('.')[0]]
    mylist.extend(inlist)
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # The ID and range of a sample spreadsheet.
    spreadsheet_id = os.environ['logsheetid']
    range_name = 'Sheet1!A1:A'


    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    values = [mylist]
    body = {
            'values': values
    }
    result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption="RAW", body=body).execute()
    print('{0} cells appended.'.format(result \
                                                                               .get('updates') \
                                                                               .get('updatedCells')))

myreqsess_get = requests.session().get

extrurl = tldextract.extract

gauth = GoogleAuth()

gauth.LoadCredentialsFile("credentials.txt")
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("credentials.txt")

drive = GoogleDrive(gauth)

#mysf = drive.CreateFile({'id': str(os.environ['driveid'])})
#mys = set(mysf.GetContentString().split("\n"))
#del mysf

endpointslist = ['http://web.archive.org/cdx/search/cdx'] #str(os.environ['index']).split(',') #['http://index.commoncrawl.org/CC-MAIN-2019-04-index']#, 'http://index.commoncrawl.org/CC-MAIN-2018-51-index', 'http://index.commoncrawl.org/CC-MAIN-2018-47-index', 'http://index.commoncrawl.org/CC-MAIN-2018-43-index', 'http://index.commoncrawl.org/CC-MAIN-2018-39-index', 'http://index.commoncrawl.org/CC-MAIN-2018-34-index', 'http://index.commoncrawl.org/CC-MAIN-2018-30-index', 'http://index.commoncrawl.org/CC-MAIN-2018-26-index', 'http://index.commoncrawl.org/CC-MAIN-2018-22-index', 'http://index.commoncrawl.org/CC-MAIN-2018-17-index', 'http://index.commoncrawl.org/CC-MAIN-2018-13-index', 'http://index.commoncrawl.org/CC-MAIN-2018-09-index', 'http://index.commoncrawl.org/CC-MAIN-2018-05-index', 'http://index.commoncrawl.org/CC-MAIN-2017-51-index', 'http://index.commoncrawl.org/CC-MAIN-2017-47-index', 'http://index.commoncrawl.org/CC-MAIN-2017-43-index', 'http://index.commoncrawl.org/CC-MAIN-2017-39-index', 'http://index.commoncrawl.org/CC-MAIN-2017-34-index', 'http://index.commoncrawl.org/CC-MAIN-2017-30-index', 'http://index.commoncrawl.org/CC-MAIN-2017-26-index', 'http://index.commoncrawl.org/CC-MAIN-2017-22-index', 'http://index.commoncrawl.org/CC-MAIN-2017-17-index', 'http://index.commoncrawl.org/CC-MAIN-2017-13-index', 'http://index.commoncrawl.org/CC-MAIN-2017-09-index', 'http://index.commoncrawl.org/CC-MAIN-2017-04-index', 'http://index.commoncrawl.org/CC-MAIN-2016-50-index', 'http://index.commoncrawl.org/CC-MAIN-2016-44-index', 'http://index.commoncrawl.org/CC-MAIN-2016-40-index', 'http://index.commoncrawl.org/CC-MAIN-2016-36-index', 'http://index.commoncrawl.org/CC-MAIN-2016-30-index', 'http://index.commoncrawl.org/CC-MAIN-2016-26-index', 'http://index.commoncrawl.org/CC-MAIN-2016-22-index', 'http://index.commoncrawl.org/CC-MAIN-2016-18-index', 'http://index.commoncrawl.org/CC-MAIN-2016-07-index', 'http://index.commoncrawl.org/CC-MAIN-2015-48-index', 'http://index.commoncrawl.org/CC-MAIN-2015-40-index', 'http://index.commoncrawl.org/CC-MAIN-2015-35-index', 'http://index.commoncrawl.org/CC-MAIN-2015-32-index', 'http://index.commoncrawl.org/CC-MAIN-2015-27-index', 'http://index.commoncrawl.org/CC-MAIN-2015-22-index', 'http://index.commoncrawl.org/CC-MAIN-2015-18-index', 'http://index.commoncrawl.org/CC-MAIN-2015-14-index', 'http://index.commoncrawl.org/CC-MAIN-2015-11-index', 'http://index.commoncrawl.org/CC-MAIN-2015-06-index', 'http://index.commoncrawl.org/CC-MAIN-2014-52-index', 'http://index.commoncrawl.org/CC-MAIN-2014-49-index', 'http://index.commoncrawl.org/CC-MAIN-2014-42-index', 'http://index.commoncrawl.org/CC-MAIN-2014-41-index', 'http://index.commoncrawl.org/CC-MAIN-2014-35-index', 'http://index.commoncrawl.org/CC-MAIN-2014-23-index', 'http://index.commoncrawl.org/CC-MAIN-2014-15-index', 'http://index.commoncrawl.org/CC-MAIN-2014-10-index', 'http://index.commoncrawl.org/CC-MAIN-2013-48-index', 'http://index.commoncrawl.org/CC-MAIN-2013-20-index']

killer = GracefulKiller()

gracefulshutdown = False
#except:
#    print('Exception!')
#    sleep(60)
#    mys = set(requests.get("https://blogspot-domains.herokuapp.com/list/domains.txt").text.split("\n"))

#try:
#    mys = set(requests.get("https://gist.githubusercontent.com/tech234a/6b44df89870d703ca909d811e74d51b8/raw").text.split("\n"))
#except:
#    print('Exception!')
#    sleep(10)
#    mys = set(requests.get("https://gist.githubusercontent.com/tech234a/6b44df89870d703ca909d811e74d51b8/raw").text.split("\n"))

#Restore previous values if necessary

print('Waiting 90 seconds to ensure previous instance has shutdown...')
sleep(90)

print('Restoring data...')

#try:
myrnew = myreqsess_get("https://blogspot-domains.herokuapp.com/list/domains.txt") #'http://blogstore.bot.nu/worker/domains.txt')
#mys = set(myrnew.text.split("\n"))
myftow = open('domains.txt', 'a')
myftow_write = myftow.write
myftow_write(myrnew.text)
del myrnew

if int(getcell('A3')) == 0:
    start_index_override = int(getcell('A1'))
    start_page_override = int(getcell('A2'))
    print('No override, '+str(start_index_override)+', '+str(start_page_override))
    #updatecells('A3', 0)
else:
    start_index_override = 0
    start_page_override = 0
    print('Override, '+str(start_index_override)+', '+str(start_page_override))

for i in range(0, start_index_override):
    print('Skipping: '+endpointslist.pop(0))

for endpt in endpointslist:
    print('\nNew endpoint:', endpt, '\n')
    appendtosheet([endpt, 'New Endpoint'])
    max = 217044 #Web Archive #myreqsess_get(endpt+'?url=*.blogspot.com/&fl=url&filter=~url:.*\.com/$&limit=999999&showNumPages=true').json()["pages"]
    #Cite the link format origin
    #Thanks jopik for referring me to the CommonCrawl
    startnum = 0
    if endpt == endpointslist[0]:
        print('Applying start page override...')
        startnum = start_page_override
    for i in range(startnum, max):
        if killer.kill_now:
            savestate(0, i)
            #updatecells('A1', i)
            #updatecells('A2', endpointslist.index(endpt))
            #updatecells('A3', 0)
            gracefulshutdown = True
            break
        complete = False
        while complete == False:
            mylistrequest = myreqsess_get(endpt+'?url=blogspot.com&matchType=domain&fl=original&collapse=original&filter=~original:@blogspot.com&page='+str(i))
            complete = mylistrequest.ok
            if not complete and mylistrequest.status_code != 404:
                print('Not ok!')
                print(mylistrequest.status_code)
                print(mylistrequest.text)
                sleep(60)
                mylistrequest = myreqsess_get(endpt+'?url=blogspot.com&matchType=domain&fl=original&collapse=original&filter=~original:@blogspot.com&page='+str(i))
            if mylistrequest.status_code == 404:
                complete = True

        print('Completed request:', mylistrequest.url)
        #if mylistrequest.status_code != 404:
        #    mys.update(re.findall(r"(?:https?:\/\/)?(?:w{3}\.)?(.+?)\.blogspot\.com", mylistrequest.text)) #Thanks afrmtbl!
        mylistrequest_text = mylistrequest.text.replace("@", ".")
        mylist = mylistrequest_text.split('\n')
        skip = False
        if mylistrequest.status_code == 404 or mylistrequest_text.strip() == '':
            mylist = []
            skip = True
        #el mylistrequest
        if not skip:
            mylist = [extrurl(element).subdomain.split('.')[-1] for element in mylist]
        #    mylist = [element.replace('http://', '') for element in mylist]
        #    mylist = [element.replace('https://', '') for element in mylist]
        #    mylist = [element.replace('.blogspot.com/', '') for element in mylist]
        #    for element in range(0, len(mylist)):
        #        if mylist[element].startswith('www.'):
        #            mylist[element] = mylist[element].replace('www.', '', 1)
            #mys.update(mylist)
            myftow_write("\n".join(mylist))
            print(mylist)
            del mylist
        if killer.kill_now:
            savestate(0, i)
            #updatecells('A1', i)
            #updatecells('A2', endpointslist.index(endpt))
            #updatecells('A3', 0)
            gracefulshutdown = True
            break
    if killer.kill_now:
        break

    appendtosheet([endpt, 'Cleaning up file'])
    #Clean up on endpoint completion
    os.system('tr -d \'\\r\' < domains.txt | sort -S 850M -u  > domains_sorted.txt') #Thanks @jopik
    
    file1 = drive.CreateFile({'title': endpt+'-01'})
    file1.SetContentFile('domains_sorted.txt')
    file1.Upload()
    heroku3.from_key(os.environ['heroku-key']).apps()['blogspot-domains'].config()['driveid'] = file1['id']
    del file1
    appendtosheet([endpt, 'Finished Endpoint'])

file1 = drive.CreateFile({'title': endpointslist[0]+'-01'})
#file1.SetContentString('\n'.join(sorted(mys)))
#os.system('sort -u -o \'domains_sorted.txt\' \'domains.txt\'')
#file1.SetContentFile('domains_sorted.txt')
if not gracefulshutdown:
    os.system('tr -d \'\\r\' < domains.txt | sort -S 850M -u  > domains_sorted.txt') #Thanks @jopik
    file1.SetContentFile('domains_sorted.txt')
else:
    file1.SetContentFile('domains.txt')
file1.Upload()
heroku3.from_key(os.environ['heroku-key']).apps()['blogspot-domains'].config()['driveid'] = file1['id']
del file1
endingtext = 'All done!'
if gracefulshutdown:
    endingtext = 'Gracefully shutdown'
appendtosheet(['', endingtext])
print(endingtext)
if not gracefulshutdown:
    heroku3.from_key(os.environ['heroku-key']).apps()['getblogspot-01'].scale_formation_process('worker', 0)
    sleep(10)
    #while True:
    #    sleep(10000)
