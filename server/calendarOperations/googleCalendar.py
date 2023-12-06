from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main():
    """
    Main function to run the GoogleClient class.
    """
    client = GoogleClient()
    
    
    client.deleteEvent("TestCal")
    #client.createCalendar()
    #client.addEventToCalendar()   
    #client.test()
    

# Class to handle everything with the Creation, Deletion of events, calendars and so forth
class GoogleClient():
    """
    Class to handle everything with the Creation, Deletion of events, calendars and so forth.
    """
    # Class variables    
    SCOPES = ["https://www.googleapis.com/auth/calendar"] 
    CREDENTIALS_PATH = 'credentials.json'

    def __init__(self, calendarName="BrainWaive"):
        """
        Initializes the GoogleClient class.

        Args:
          calendarName (str, optional): The name of the calendar to create. Defaults to "BrainWaive".

        Side Effects:
          Creates a calendar with the given name.
        """
        self.service = GoogleClient.createService()
        self.calendarName = calendarName
        calendar = self.createCalendar(calendarName, "Europe/Zurich")
        self.calendarId = calendar["id"]
          
          
    # create the service, that is going to be used to make the requests to the GoogleCalendarApi
    @classmethod
    def createService(self):  
        """
        Creates the service used to make requests to the Google Calendar API.

        Returns:
          googleapiclient.discovery.Resource: The service used to make requests to the Google Calendar API.
        """
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', GoogleClient.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                   GoogleClient.CREDENTIALS_PATH , GoogleClient.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds)
            return service
        
        except HttpError as error:
            print('An error occurred: %s' % error)
        
        
    # creates a calendar with the calendarName in the specified timezone
    def createCalendar(self, calendarName="BrainWaive", timezone ="Europe/Zurich"):
        """
        Creates a calendar with the given name in the specified timezone.

        Args:
          calendarName (str): The name of the calendar to create.
          timezone (str): The timezone of the calendar.

        Returns:
          dict: The calendar created.

        Examples:
          >>> GoogleClient.createCalendar("TestCal", "Europe/Zurich")
          {'summary': 'TestCal', 'timeZone': 'Europe/Zurich'}
        """
        exists, calendar = self.calendarExist(calendarName, returnCalendar=True)
        if not exists:    
            try:  
                calendar = {
                    'summary': calendarName,
                    'timeZone': timezone
                }
                return self.service.calendars().insert(body=calendar).execute()
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                return None
        else:
            return calendar

    # adds an Event with the most important fields to the calendar  
    # DateTimes in ISO 8601 format, for example '2013-02-14T13:15:03-08:00' (YYYY-MM-DDTHH:mm:ssZ) 
    def insertEvent(self, eventName, eventDescription, startDateTime, endDateTime, timezone = "Europe/Zurich"):
        """
        Adds an event with the most important fields to the calendar.

        Args:
          eventName (str): The name of the event.
          eventDescription (str): The description of the event.
          startDateTime (str): The start date and time of the event in ISO 8601 format.
          endDateTime (str): The end date and time of the event in ISO 8601 format.
          timezone (str, optional): The timezone of the event. Defaults to "Europe/Zurich".

        Side Effects:
          Prints the link to the event.
        """
        event = {
        'summary': eventName,
        'description': eventDescription,
        'start': {
            'dateTime': startDateTime,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': endDateTime,
            'timeZone': timezone,
        }
        }
        event = self.service.events().insert(calendarId=self.calendarId, body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

    # Deletes an event from the calendar by its name
    def deleteEvent(self, eventName):
        """
        Deletes an event from the calendar by its name.

        Args:
          eventName (str): The name of the event to delete.

        Examples:
          >>> GoogleClient.deleteEvent("TestEvent")
          Event deleted.
        """
        eventId = self.getIdOfEventByName(eventName)
        self.service.events().delete(calendarId=self.calendarId, eventId=eventId).execute()


    def updateEvent(self, eventName, eventDescription, startDateTime, endDateTime, timezone = "Europe/Zurich"):
        """
        Updates an event in the Google Calendar.

        Args:
          eventName (str): The name of the event to update.
          eventDescription (str): The description of the event to update.
          startDateTime (str): The start date and time of the event to update.
          endDateTime (str): The end date and time of the event to update.
          timezone (str): The timezone of the event to update. Defaults to "Europe/Zurich".

        Returns:
          None

        Examples:
          >>> updateEvent("My Event", "My event description", "2020-08-01T10:00:00", "2020-08-01T11:00:00")
        """
        # First retrieve the event from the API.
        eventId = self.getIdOfEventByName(eventName)
        event = self.service.events().get(calendarId=self.calendarId, eventId=eventId).execute()

        event['summary'] = eventName
        event["description"] = eventDescription
        event["start"]["dateTime"] = startDateTime
        event["start"]["timeZone"] = timezone
        event["end"]["dateTime"] = endDateTime
        event["end"]["timeZone"] = timezone

        updated_event = self.service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

        # Print the updated date.
        print(updated_event['updated'])
        
        

    # gets the id of an event by its name
    def getIdOfEventByName(self, eventName):
        """
        Retrieves the ID of an event by its name.

        Args:
          eventName (str): The name of the event to retrieve.

        Returns:
          str: The ID of the event.

        Examples:
          >>> getIdOfEventByName("My Event")
          "123456789"
        """
        try:
            events_result = self.service.events().list(
                calendarId=self.calendarId,
                q=eventName
            ).execute()

            events = events_result.get('items', [])
            
            for event in events:
                if event['summary'] == eventName:
                    return event['id']

            return None

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
            
        
    # Gets the Id of the calendar by name, searching in the Calendarlist of the authenticated user
    def getIdOfCalendarByName(self, calendarName):
        """
        Retrieves the ID of a calendar by its name.

        Args:
          calendarName (str): The name of the calendar to retrieve.

        Returns:
          str: The ID of the calendar.

        Examples:
          >>> getIdOfCalendarByName("My Calendar")
          "987654321"
        """
        try:
            calendar_list = self.service.calendarList().list().execute()
            calendar_id = None
            for calendar in calendar_list.get('items', []):
                if calendar['summary'] == calendarName:
                    calendar_id = calendar['id']
                    break
            return calendar_id
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    # true if the calendar already exists else false
    # by name
    def calendarExist(self, calendarName, returnCalendar=False):
        """
        Checks if a calendar exists by its name.

        Args:
          calendarName (str): The name of the calendar to check.
          returnCalendar (bool): Whether to return the calendar object. Defaults to False.

        Returns:
          bool: Whether the calendar exists.
          dict: The calendar object, if returnCalendar is True.

        Examples:
          >>> calendarExist("My Calendar")
          True
        """
        # The scope for the Calendar API
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

        try:
            calendar_list = self.service.calendarList().list().execute()
            for calendar in calendar_list.get('items', []):
                if calendar['summary'] == calendarName:
                    if returnCalendar:
                        return True, calendar
                    return True, None
            return False, None

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False, None


                    
if __name__ == '__main__':
    main()