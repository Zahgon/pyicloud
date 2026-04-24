"""Contacts service."""


class ContactsService:
    """
    The 'Contacts' iCloud service, connects to iCloud and returns contacts.
    """

    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root
        self._contacts_endpoint = "%s/co" % self._service_root
        self._contacts_refresh_url = "%s/startup" % self._contacts_endpoint
        self._contacts_next_url = "%s/contacts" % self._contacts_endpoint
        self._contacts_changeset_url = "%s/changeset" % self._contacts_endpoint

        self.response = {}

    def refresh_client(self):
        """
        Refreshes the ContactsService endpoint, ensuring that the
        contacts data is up-to-date.
        """
        pass

    def all(self):
        """
        Retrieves all contacts.
        """
        pass
