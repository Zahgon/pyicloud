"""Drive service."""
from datetime import datetime, timedelta
import json
import logging
import io
import mimetypes
import os
import time
from re import search
from requests import Response

from pyicloud.exceptions import PyiCloudAPIResponseException


LOGGER = logging.getLogger(__name__)


class DriveService:
    """The 'Drive' iCloud service."""

    def __init__(self, service_root, document_root, session, params):
        self._service_root = service_root
        self._document_root = document_root
        self.session = session
        self.params = dict(params)
        self._root = None

    def _get_token_from_cookie(self):
        pass

    def get_node_data(self, node_id):
        """Returns the node data."""
        pass

    def get_file(self, file_id, **kwargs):
        """Returns iCloud Drive file."""
        pass

    def get_app_data(self):
        """Returns the app library (previously ubiquity)."""
        pass

    def _get_upload_contentws_url(self, file_object):
        """Get the contentWS endpoint URL to add a new file."""
        pass

    def _update_contentws(self, folder_id, sf_info, document_id, file_object):
        pass

    def send_file(self, folder_id, file_object):
        """Send new file to iCloud Drive."""
        pass

    def create_folders(self, parent, name):
        """Creates a new iCloud Drive folder"""
        pass

    def rename_items(self, node_id, etag, name):
        """Renames an iCloud Drive node"""
        pass

    def move_items_to_trash(self, node_id, etag):
        """Moves an iCloud Drive node to the trash bin"""
        pass

    @property
    def root(self):
        """Returns the root node."""
        pass

    def __getattr__(self, attr):
        return getattr(self.root, attr)

    def __getitem__(self, key):
        return self.root[key]

    def _raise_if_error(self, response):  # pylint: disable=no-self-use
        pass


class DriveNode:
    """Drive node."""

    def __init__(self, conn, data):
        self.data = data
        self.connection = conn
        self._children = None

    @property
    def name(self):
        """Gets the node name."""
        pass

    @property
    def type(self):
        """Gets the node type."""
        pass

    def get_children(self):
        """Gets the node children."""
        pass

    @property
    def size(self):
        """Gets the node size."""
        pass

    @property
    def date_changed(self):
        """Gets the node changed date (in UTC)."""
        pass

    @property
    def date_modified(self):
        """Gets the node modified date (in UTC)."""
        pass

    @property
    def date_last_open(self):
        """Gets the node last open date (in UTC)."""
        pass

    def open(self, **kwargs):
        """Gets the node file."""
        pass

    def upload(self, file_object, **kwargs):
        """Upload a new file."""
        pass

    def dir(self):
        """Gets the node list of directories."""
        pass

    def mkdir(self, folder):
        """Create a new directory directory."""
        pass

    def rename(self, name):
        """Rename an iCloud Drive item."""
        pass

    def delete(self):
        """Delete an iCloud Drive item."""
        pass

    def get(self, name):
        """Gets the node child."""
        pass

    def __getitem__(self, key):
        try:
            return self.get(key)
        except IndexError as i:
            raise KeyError(f"No child named '{key}' exists") from i

    def __str__(self):
        return rf"\{type: {self.type}, name: {self.name}\}"

    def __repr__(self):
        return f"<{type(self).__name__}: {str(self)}>"


def _date_to_utc(date):
    pass
