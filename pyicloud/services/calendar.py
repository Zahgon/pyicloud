"""Calendar service."""
from datetime import datetime
from calendar import monthrange

from tzlocal import get_localzone_name


class CalendarService:
    """
    The 'Calendar' iCloud service, connects to iCloud and returns events.
    """

    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root
        self._calendar_endpoint = "%s/ca" % self._service_root
        self._calendar_refresh_url = "%s/events" % self._calendar_endpoint
        self._calendar_event_detail_url = f"{self._calendar_endpoint}/eventdetail"
        self._calendars = "%s/startup" % self._calendar_endpoint

        self.response = {}

    def get_event_detail(self, pguid, guid):
        """
        Fetches a single event's details by specifying a pguid
        (a calendar) and a guid (an event's ID).
        """
        pass

    def refresh_client(self, from_dt=None, to_dt=None):
        """
        Refreshes the CalendarService endpoint, ensuring that the
        event data is up-to-date. If no 'from_dt' or 'to_dt' datetimes
        have been given, the range becomes this month.
        """
        pass

    def events(self, from_dt=None, to_dt=None):
        """
        Retrieves events for a given date range, by default, this month.
        """
        pass

    def calendars(self):
        """
        Retrieves calendars of this month.
        """
        pass
