import pickle, os, requests, pydrive
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from time import sleep

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

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

endpointslist = [str(os.environ['index'])] #['http://index.commoncrawl.org/CC-MAIN-2019-04-index']#, 'http://index.commoncrawl.org/CC-MAIN-2018-51-index', 'http://index.commoncrawl.org/CC-MAIN-2018-47-index', 'http://index.commoncrawl.org/CC-MAIN-2018-43-index', 'http://index.commoncrawl.org/CC-MAIN-2018-39-index', 'http://index.commoncrawl.org/CC-MAIN-2018-34-index', 'http://index.commoncrawl.org/CC-MAIN-2018-30-index', 'http://index.commoncrawl.org/CC-MAIN-2018-26-index', 'http://index.commoncrawl.org/CC-MAIN-2018-22-index', 'http://index.commoncrawl.org/CC-MAIN-2018-17-index', 'http://index.commoncrawl.org/CC-MAIN-2018-13-index', 'http://index.commoncrawl.org/CC-MAIN-2018-09-index', 'http://index.commoncrawl.org/CC-MAIN-2018-05-index', 'http://index.commoncrawl.org/CC-MAIN-2017-51-index', 'http://index.commoncrawl.org/CC-MAIN-2017-47-index', 'http://index.commoncrawl.org/CC-MAIN-2017-43-index', 'http://index.commoncrawl.org/CC-MAIN-2017-39-index', 'http://index.commoncrawl.org/CC-MAIN-2017-34-index', 'http://index.commoncrawl.org/CC-MAIN-2017-30-index', 'http://index.commoncrawl.org/CC-MAIN-2017-26-index', 'http://index.commoncrawl.org/CC-MAIN-2017-22-index', 'http://index.commoncrawl.org/CC-MAIN-2017-17-index', 'http://index.commoncrawl.org/CC-MAIN-2017-13-index', 'http://index.commoncrawl.org/CC-MAIN-2017-09-index', 'http://index.commoncrawl.org/CC-MAIN-2017-04-index', 'http://index.commoncrawl.org/CC-MAIN-2016-50-index', 'http://index.commoncrawl.org/CC-MAIN-2016-44-index', 'http://index.commoncrawl.org/CC-MAIN-2016-40-index', 'http://index.commoncrawl.org/CC-MAIN-2016-36-index', 'http://index.commoncrawl.org/CC-MAIN-2016-30-index', 'http://index.commoncrawl.org/CC-MAIN-2016-26-index', 'http://index.commoncrawl.org/CC-MAIN-2016-22-index', 'http://index.commoncrawl.org/CC-MAIN-2016-18-index', 'http://index.commoncrawl.org/CC-MAIN-2016-07-index', 'http://index.commoncrawl.org/CC-MAIN-2015-48-index', 'http://index.commoncrawl.org/CC-MAIN-2015-40-index', 'http://index.commoncrawl.org/CC-MAIN-2015-35-index', 'http://index.commoncrawl.org/CC-MAIN-2015-32-index', 'http://index.commoncrawl.org/CC-MAIN-2015-27-index', 'http://index.commoncrawl.org/CC-MAIN-2015-22-index', 'http://index.commoncrawl.org/CC-MAIN-2015-18-index', 'http://index.commoncrawl.org/CC-MAIN-2015-14-index', 'http://index.commoncrawl.org/CC-MAIN-2015-11-index', 'http://index.commoncrawl.org/CC-MAIN-2015-06-index', 'http://index.commoncrawl.org/CC-MAIN-2014-52-index', 'http://index.commoncrawl.org/CC-MAIN-2014-49-index', 'http://index.commoncrawl.org/CC-MAIN-2014-42-index', 'http://index.commoncrawl.org/CC-MAIN-2014-41-index', 'http://index.commoncrawl.org/CC-MAIN-2014-35-index', 'http://index.commoncrawl.org/CC-MAIN-2014-23-index', 'http://index.commoncrawl.org/CC-MAIN-2014-15-index', 'http://index.commoncrawl.org/CC-MAIN-2014-10-index', 'http://index.commoncrawl.org/CC-MAIN-2013-48-index', 'http://index.commoncrawl.org/CC-MAIN-2013-20-index']
try:
    mys = set(requests.get("https://gist.githubusercontent.com/tech234a/6b44df89870d703ca909d811e74d51b8/raw").text.split("\n"))
except:
    print('Exception!')
    sleep(10)
    mys = set(requests.get("https://gist.githubusercontent.com/tech234a/6b44df89870d703ca909d811e74d51b8/raw").text.split("\n"))
for endpt in endpointslist:
    print('\nNew endpoint:', endpt, '\n')
    max = requests.get(endpt+'?url=*.blogspot.com/&fl=url&filter=~url:.*\.com/$&limit=999999&showNumPages=true').json()["pages"]
    #Cite the link format origin
    #Thanks jopik for referring me to the CommonCrawl
    for i in range(0, max):
        complete = False
        while complete == False:
            mylistrequest = requests.get(endpt+'?url=*.blogspot.com/&fl=url&filter=~url:.*\.com/$&limit=999999&page='+str(i))
            complete = mylistrequest.ok
            if not complete and mylistrequest.status_code != 404:
                print('Not ok!')
                print(mylistrequest.status_code)
                print(mylistrequest.text)
                sleep(60)
                mylistrequest = requests.get(endpt+'?url=*.blogspot.com/&fl=url&filter=~url:.*\.com/$&limit=999999&page='+str(i))
            if mylistrequest.status_code == 404:
                complete = True
        
        print('Completed request:', mylistrequest.url)
        if mylistrequest.status_code != 404:
            mys.update(re.findall(r"https?:\/\/(?:w{3}.)?(.+?)\.", url)) #Thanks afrmtbl!

file1 = drive.CreateFile({'title': endpointslist[0]+'-01'})
file1.SetContentString('\n'.join(sorted(mys)))
file1.Upload()
del file1
print('All done!')
while True:
    sleep(10000)
