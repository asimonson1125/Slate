from datetime import datetime, timedelta
from apple_calendar_integration import ICloudCalendarAPI
from requests.models import stream_decode_response_unicode
import testcred

class EmailValidationError(Exception):
    '''Throw this error if an email address is found to be invalid.'''
    def __init__(self, message):
        '''Constructor that calls the base class (Exception) constructor.'''
        super(EmailValidationError, self).__init__(message)


def format_timestamp(datetime_obj: datetime) -> str:
    '''Create a nicely formatted timestamp.
        print(datetime.now())
        print(format_timestamp(datetime.now()))
    '''
    #return datetime_obj.strftime('%Y%m%dT%H%M%SZ')
    return datetime_obj.strftime('%m/%d/%y, %H:%M:%S')

'''
api = ICloudCalendarAPI(testcred.user, testcred.passw)

start_date = int(datetime.now().timestamp())
end_date = start_date + 7200
etag, ctag, guid = api.create_event('Your title', start_date, end_date)
'''

try:
    api = ICloudCalendarAPI(testcred.user, testcred.passw)
except Exception as err:
    if err == 'Cant login: Bad credentials':
        print("Incorrect email or password")
    else:
        print(err)


