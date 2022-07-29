from django.shortcuts import render
from django.urls import reverse 
from django.http import HttpResponseRedirect, HttpResponse
import msal 
import mainapp.config as cfg
import requests
import datetime
import pytz  

# Create your views here.

def index(request):
    context = {
        "page_name" : "Home",
        "url": getAuthorityRequestUrl()
    }
    return render(request,'index.html',context)

def retrieveCallbackCode(request):
    callbackCode = request.GET.get('code')
    accessToken = retrieveAccessToken(callbackCode)
    request.session['access_token'] = accessToken
    return HttpResponseRedirect(reverse('displayMeeting'))

def displayMeeting(request):
    context = {
        "page_name" : "Schedule Meeting"
    }
    return render(request,'schedule.html',context)

def createMeeting(request):
    meeting_title = request.GET['meeting_title']
    meeting_start_date = request.GET['start_time']
    meeting_end_date = request.GET['end_time']
    meeting_data  = createMeetingUsingAPI(request,meeting_title,meeting_start_date,meeting_end_date)
    context = {
        "page_name" : "Displaying Meeting Details",
        "meeting_data" : meeting_data
    }
    return render(request, 'display.html',context)

# def tempDisplay(request):
#     meeting_data = {'@odata.context': "https://graph.microsoft.com/v1.0/$metadata#users('5e073137-b0e2-4c87-918c-2036840ec30f')/onlineMeetings/$entity", 'id': 'MSo1ZTA3MzEzNy1iMGUyLTRjODctOTE4Yy0yMDM2ODQwZWMzMGYqMCoqMTk6bWVldGluZ19NakF4WldJNFltRXRaakl6WkMwME1qbGpMV0UzWmpjdFlXVXlaR05qWlRsaU16UXpAdGhyZWFkLnYy', 'creationDateTime': '2022-07-29T12:32:45.5168198Z', 'startDateTime': '2022-07-29T20:00:00Z', 'endDateTime': '2022-07-29T20:20:00Z', 'joinUrl': 'https://teams.microsoft.com/l/meetup-join/19%3ameeting_MjAxZWI4YmEtZjIzZC00MjljLWE3ZjctYWUyZGNjZTliMzQz%40thread.v2/0?context=%7b%22Tid%22%3a%2290b563d8-24b8-4e9b-8cfb-95ca1592fb01%22%2c%22Oid%22%3a%225e073137-b0e2-4c87-918c-2036840ec30f%22%7d', 'joinWebUrl': 'https://teams.microsoft.com/l/meetup-join/19%3ameeting_MjAxZWI4YmEtZjIzZC00MjljLWE3ZjctYWUyZGNjZTliMzQz%40thread.v2/0?context=%7b%22Tid%22%3a%2290b563d8-24b8-4e9b-8cfb-95ca1592fb01%22%2c%22Oid%22%3a%225e073137-b0e2-4c87-918c-2036840ec30f%22%7d', 'meetingCode': '274216975634', 'subject': 'Meeting #1', 'isBroadcast': False, 'autoAdmittedUsers': 'everyoneInCompany', 'outerMeetingAutoAdmittedUsers': None, 'isEntryExitAnnounced': True, 'allowedPresenters': 'everyone', 'allowMeetingChat': 'enabled', 'allowTeamworkReactions': True, 'allowAttendeeToEnableMic': True, 'allowAttendeeToEnableCamera': True, 'recordAutomatically': False, 'anonymizeIdentityForRoles': [], 'capabilities': [], 'videoTeleconferenceId': None, 'externalId': None, 'broadcastSettings': None, 'joinMeetingIdSettings': {'isPasscodeRequired': False, 'joinMeetingId': '274216975634', 'passcode': None}, 'audioConferencing': None, 'meetingInfo': None, 'participants': {'organizer': {'upn': 'vjaiwantx@xzmrk.onmicrosoft.com', 'role': 'presenter', 'identity': {'acsUser': None, 'spoolUser': None, 'phone': None, 'guest': None, 'encrypted': None, 'onPremises': None, 'acsApplicationInstance': None, 'spoolApplicationInstance': None, 'applicationInstance': None, 'application': None, 'device': None, 'user': {'id': '5e073137-b0e2-4c87-918c-2036840ec30f', 'displayName': None, 'tenantId': '90b563d8-24b8-4e9b-8cfb-95ca1592fb01', 'registrantId': None, 'identityProvider': 'AAD'}}}, 'attendees': []}, 'lobbyBypassSettings': {'scope': 'organization', 'isDialInBypassEnabled': False}, 'chatInfo': {'threadId': '19:meeting_MjAxZWI4YmEtZjIzZC00MjljLWE3ZjctYWUyZGNjZTliMzQz@thread.v2', 'messageId': '0', 'replyChainMessageId': None}, 'joinInformation': {'content': 'data:text/html,%3cdiv+style%3d%22width%3a100%25%3bheight%3a+20px%3b%22%3e%0d%0a++++%3cspan+style%3d%22white-space%3anowrap%3bcolor%3a%235F5F5F%3bopacity%3a.36%3b%22%3e________________________________________________________________________________%3c%2fspan%3e%0d%0a%3c%2fdiv%3e%0d%0a+%0d%0a+%3cdiv+class%3d%22me-email-text%22+style%3d%22color%3a%23252424%3bfont-family%3a%27Segoe+UI%27%2c%27Helvetica+Neue%27%2cHelvetica%2cArial%2csans-serif%3b%22+lang%3d%22en-US%22%3e%0d%0a++++%3cdiv+style%3d%22margin-top%3a+24px%3b+margin-bottom%3a+20px%3b%22%3e%0d%0a++++++++%3cspan+style%3d%22font-size%3a+24px%3b+color%3a%23252424%22%3eMicrosoft+Teams+meeting%3c%2fspan%3e%0d%0a++++%3c%2fdiv%3e%0d%0a++++%3cdiv+style%3d%22margin-bottom%3a+20px%3b%22%3e%0d%0a++++++++%3cdiv+style%3d%22margin-top%3a+0px%3b+margin-bottom%3a+0px%3b+font-weight%3a+bold%22%3e%0d%0a++++++++++%3cspan+style%3d%22font-size%3a+14px%3b+color%3a%23252424%22%3eJoin+on+your+computer+or+mobile+app%3c%2fspan%3e%0d%0a++++++++%3c%2fdiv%3e%0d%0a++++++++%3ca+class%3d%22me-email-headline%22+style%3d%22font-size%3a+14px%3bfont-family%3a%27Segoe+UI+Semibold%27%2c%27Segoe+UI%27%2c%27Helvetica+Neue%27%2cHelvetica%2cArial%2csans-serif%3btext-decoration%3a+underline%3bcolor%3a+%236264a7%3b%22+href%3d%22https%3a%2f%2fteams.microsoft.com%2fl%2fmeetup-join%2f19%253ameeting_MjAxZWI4YmEtZjIzZC00MjljLWE3ZjctYWUyZGNjZTliMzQz%2540thread.v2%2f0%3fcontext%3d%257b%2522Tid%2522%253a%252290b563d8-24b8-4e9b-8cfb-95ca1592fb01%2522%252c%2522Oid%2522%253a%25225e073137-b0e2-4c87-918c-2036840ec30f%2522%257d%22+target%3d%22_blank%22+rel%3d%22noreferrer+noopener%22%3eClick+here+to+join+the+meeting%3c%2fa%3e%0d%0a++++%3c%2fdiv%3e%0d%0a++++%3cdiv+style%3d%22margin-bottom%3a20px%3b+margin-top%3a20px%22%3e%0d%0a++++%3cdiv+style%3d%22margin-bottom%3a4px%22%3e%0d%0a++++++++%3cspan+data-tid%3d%22meeting-code%22+style%3d%22font-size%3a+14px%3b+color%3a%23252424%3b%22%3e%0d%0a++++++++++++Meeting+ID%3a+%3cspan+style%3d%22font-size%3a16px%3b+color%3a%23252424%3b%22%3e274+216+975+634%3c%2fspan%3e%0d%0a+++++++%3c%2fspan%3e%0d%0a++++++++%0d%0a++++++++%3cdiv+style%3d%22font-size%3a+14px%3b%22%3e%3ca+class%3d%22me-email-link%22+style%3d%22font-size%3a+14px%3btext-decoration%3a+underline%3bcolor%3a+%236264a7%3bfont-family%3a%27Segoe+UI%27%2c%27Helvetica+Neue%27%2cHelvetica%2cArial%2csans-serif%3b%22+target%3d%22_blank%22+href%3d%22https%3a%2f%2fwww.microsoft.com%2fen-us%2fmicrosoft-teams%2fdownload-app%22+rel%3d%22noreferrer+noopener%22%3e%0d%0a++++++++Download+Teams%3c%2fa%3e+%7c+%3ca+class%3d%22me-email-link%22+style%3d%22font-size%3a+14px%3btext-decoration%3a+underline%3bcolor%3a+%236264a7%3bfont-family%3a%27Segoe+UI%27%2c%27Helvetica+Neue%27%2cHelvetica%2cArial%2csans-serif%3b%22+target%3d%22_blank%22+href%3d%22https%3a%2f%2fwww.microsoft.com%2fmicrosoft-teams%2fjoin-a-meeting%22+rel%3d%22noreferrer+noopener%22%3eJoin+on+the+web%3c%2fa%3e%3c%2fdiv%3e%0d%0a++++%3c%2fdiv%3e%0d%0a+%3c%2fdiv%3e%0d%0a++++%0d%0a++++++%0d%0a++++%0d%0a++++%0d%0a++++%0d%0a++++%3cdiv+style%3d%22margin-bottom%3a+24px%3bmargin-top%3a+20px%3b%22%3e%0d%0a++++++++%3ca+class%3d%22me-email-link%22+style%3d%22font-size%3a+14px%3btext-decoration%3a+underline%3bcolor%3a+%236264a7%3bfont-family%3a%27Segoe+UI%27%2c%27Helvetica+Neue%27%2cHelvetica%2cArial%2csans-serif%3b%22+target%3d%22_blank%22+href%3d%22https%3a%2f%2faka.ms%2fJoinTeamsMeeting%22+rel%3d%22noreferrer+noopener%22%3eLearn+More%3c%2fa%3e++%7c+%3ca+class%3d%22me-email-link%22+style%3d%22font-size%3a+14px%3btext-decoration%3a+underline%3bcolor%3a+%236264a7%3bfont-family%3a%27Segoe+UI%27%2c%27Helvetica+Neue%27%2cHelvetica%2cArial%2csans-serif%3b%22+target%3d%22_blank%22+href%3d%22https%3a%2f%2fteams.microsoft.com%2fmeetingOptions%2f%3forganizerId%3d5e073137-b0e2-4c87-918c-2036840ec30f%26tenantId%3d90b563d8-24b8-4e9b-8cfb-95ca1592fb01%26threadId%3d19_meeting_MjAxZWI4YmEtZjIzZC00MjljLWE3ZjctYWUyZGNjZTliMzQz%40thread.v2%26messageId%3d0%26language%3den-US%22+rel%3d%22noreferrer+noopener%22%3eMeeting+options%3c%2fa%3e+%0d%0a++++++%3c%2fdiv%3e%0d%0a%3c%2fdiv%3e%0d%0a%3cdiv+style%3d%22font-size%3a+14px%3b+margin-bottom%3a+4px%3bfont-family%3a%27Segoe+UI%27%2c%27Helvetica+Neue%27%2cHelvetica%2cArial%2csans-serif%3b%22%3e%0d%0a%0d%0a%3c%2fdiv%3e%0d%0a%3cdiv+style%3d%22font-size%3a+12px%3b%22%3e%0d%0a%0d%0a%3c%2fdiv%3e%0d%0a%0d%0a%3c%2fdiv%3e%0d%0a%3cdiv+style%3d%22width%3a100%25%3bheight%3a+20px%3b%22%3e%0d%0a++++%3cspan+style%3d%22white-space%3anowrap%3bcolor%3a%235F5F5F%3bopacity%3a.36%3b%22%3e________________________________________________________________________________%3c%2fspan%3e%0d%0a%3c%2fdiv%3e', 'contentType': 'html'}}
#     context = {
#         "page_name" : "Displaying Meeting Details",
#         "meeting_data" : meeting_data
#     }
#     return render(request, 'display.html',context)



# methods are defined here
def retrieveClientInstance():
    client_instance = msal.ConfidentialClientApplication(
    client_id = cfg.APPLICATION_ID,
    client_credential = cfg.CLIENT_SECRET,
    authority = cfg.authority_url
)
    return client_instance

def getAuthorityRequestUrl():
    client_instance = retrieveClientInstance()
    authority_request_url = client_instance.get_authorization_request_url(cfg.SCOPES)
    return authority_request_url 

def retrieveAccessToken(callbackCode):
    client_instance = retrieveClientInstance()
    access_token = client_instance.acquire_token_by_authorization_code(
    code = callbackCode,
    scopes = cfg.SCOPES
)
    access_token_id = access_token['access_token']
    return access_token_id 

def createMeetingUsingAPI(request,title,startTime,endTime):
    headers = {'Authorization': 'Bearer ' + request.session['access_token'], 'Content-Type': 'application/json'}
    meeting_data = {
    "startDateTime": toAzureTimeFormatTest(startTime),
    "endDateTime": toAzureTimeFormatTest(endTime),
    "subject": title
    }
    response = requests.post(cfg.endpoint,json=meeting_data,headers=headers)
    data = response.json()
    return data

def toAzureTimeFormatTest(localtime):
    conv_time = datetime.datetime.strptime(localtime,'%Y-%m-%dT%H:%M')
    final_timeformat = str(datetime.datetime.strftime(conv_time,'%Y-%m-%dT%H:%M:%S.%f'))+'-00:00'
    return final_timeformat