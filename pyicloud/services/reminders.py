"""Reminders service."""
from datetime import datetime
import time
import uuid
import json

from tzlocal import get_localzone_name


class RemindersService:
    """The 'Reminders' iCloud service."""

    def __init__(self, service_root, session, params):
        self.session = session
        self._params = params
        self._service_root = service_root

        self.lists = {}
        self.collections = {}

        self.refresh()

    def refresh(self):
        """Refresh data."""
        pass

    def post(self, title, description="", collection=None, due_date=None):
        """Adds a new reminder."""
        pass
