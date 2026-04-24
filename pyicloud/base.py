"""Library base file."""
from uuid import uuid1
import inspect
import json
import logging
from requests import Session
from tempfile import gettempdir
from os import path, mkdir
from re import match
import http.cookiejar as cookielib
import getpass

from pyicloud.exceptions import (
    PyiCloudFailedLoginException,
    PyiCloudAPIResponseException,
    PyiCloud2SARequiredException,
    PyiCloudServiceNotActivatedException,
)
from pyicloud.services import (
    FindMyiPhoneServiceManager,
    CalendarService,
    UbiquityService,
    ContactsService,
    RemindersService,
    PhotosService,
    AccountService,
    DriveService,
)
from pyicloud.utils import get_password_from_keyring


LOGGER = logging.getLogger(__name__)

HEADER_DATA = {
    "X-Apple-ID-Account-Country": "account_country",
    "X-Apple-ID-Session-Id": "session_id",
    "X-Apple-Session-Token": "session_token",
    "X-Apple-TwoSV-Trust-Token": "trust_token",
    "scnt": "scnt",
}


class PyiCloudPasswordFilter(logging.Filter):
    """Password log hider."""

    def __init__(self, password):
        super().__init__(password)

    def filter(self, record):
        pass


class PyiCloudSession(Session):
    """iCloud session."""

    def __init__(self, service):
        self.service = service
        super().__init__()

    def request(self, method, url, **kwargs):  # pylint: disable=arguments-differ

        # Charge logging to the right service endpoint
        pass

    def _raise_error(self, code, reason):
        pass


class PyiCloudService:
    """
    A base authentication class for the iCloud service. Handles the
    authentication required to access iCloud services.

    Usage:
        from pyicloud import PyiCloudService
        pyicloud = PyiCloudService('username@apple.com', 'password')
        pyicloud.iphone.location()
    """

    AUTH_ENDPOINT = "https://idmsa.apple.com/appleauth/auth"
    HOME_ENDPOINT = "https://www.icloud.com"
    SETUP_ENDPOINT = "https://setup.icloud.com/setup/ws/1"

    def __init__(
        self,
        apple_id,
        password=None,
        cookie_directory=None,
        verify=True,
        client_id=None,
        with_family=True,
        china_mainland=False,
    ):
        # If the country or region setting of your Apple ID is China mainland.
        # See https://support.apple.com/en-us/HT208351
        if china_mainland:
            self.AUTH_ENDPOINT = "https://idmsa.apple.com.cn/appleauth/auth"
            self.HOME_ENDPOINT = "https://www.icloud.com.cn"
            self.SETUP_ENDPOINT = "https://setup.icloud.com.cn/setup/ws/1"

        if password is None:
            password = get_password_from_keyring(apple_id)

        self.user = {"accountName": apple_id, "password": password}
        self.data = {}
        self.params = {}
        self.client_id = client_id or ("auth-%s" % str(uuid1()).lower())
        self.with_family = with_family

        self.password_filter = PyiCloudPasswordFilter(password)
        LOGGER.addFilter(self.password_filter)

        if cookie_directory:
            self._cookie_directory = path.expanduser(path.normpath(cookie_directory))
            if not path.exists(self._cookie_directory):
                mkdir(self._cookie_directory, 0o700)
        else:
            topdir = path.join(gettempdir(), "pyicloud")
            self._cookie_directory = path.join(topdir, getpass.getuser())
            if not path.exists(topdir):
                mkdir(topdir, 0o777)
            if not path.exists(self._cookie_directory):
                mkdir(self._cookie_directory, 0o700)

        LOGGER.debug("Using session file %s", self.session_path)

        self.session_data = {}
        try:
            with open(self.session_path, encoding="utf-8") as session_f:
                self.session_data = json.load(session_f)
        except:  # pylint: disable=bare-except
            LOGGER.info("Session file does not exist")
        if self.session_data.get("client_id"):
            self.client_id = self.session_data.get("client_id")
        else:
            self.session_data.update({"client_id": self.client_id})

        self.session = PyiCloudSession(self)
        self.session.verify = verify
        self.session.headers.update(
            {"Origin": self.HOME_ENDPOINT, "Referer": "%s/" % self.HOME_ENDPOINT}
        )

        cookiejar_path = self.cookiejar_path
        self.session.cookies = cookielib.LWPCookieJar(filename=cookiejar_path)
        if path.exists(cookiejar_path):
            try:
                self.session.cookies.load(ignore_discard=True, ignore_expires=True)
                LOGGER.debug("Read cookies from %s", cookiejar_path)
            except:  # pylint: disable=bare-except
                # Most likely a pickled cookiejar from earlier versions.
                # The cookiejar will get replaced with a valid one after
                # successful authentication.
                LOGGER.warning("Failed to read cookiejar %s", cookiejar_path)

        self.authenticate()

        self._drive = None
        self._files = None
        self._photos = None

    def authenticate(self, force_refresh=False, service=None):
        """
        Handles authentication, and persists cookies so that
        subsequent logins will not cause additional e-mails from Apple.
        """
        pass

    def _authenticate_with_token(self):
        """Authenticate using session token."""
        pass

    def _authenticate_with_credentials_service(self, service):
        """Authenticate to a specific service using credentials."""
        pass

    def _validate_token(self):
        """Checks if the current access token is still valid."""
        pass

    def _get_auth_headers(self, overrides=None):
        pass

    @property
    def cookiejar_path(self):
        """Get path for cookiejar file."""
        pass

    @property
    def session_path(self):
        """Get path for session data file."""
        pass

    @property
    def requires_2sa(self):
        """Returns True if two-step authentication is required."""
        pass

    @property
    def requires_2fa(self):
        """Returns True if two-factor authentication is required."""
        pass

    @property
    def is_trusted_session(self):
        """Returns True if the session is trusted."""
        pass

    @property
    def trusted_devices(self):
        """Returns devices trusted for two-step authentication."""
        pass

    def send_verification_code(self, device):
        """Requests that a verification code is sent to the given device."""
        pass

    def validate_verification_code(self, device, code):
        """Verifies a verification code received on a trusted device."""
        pass

    def validate_2fa_code(self, code):
        """Verifies a verification code received via Apple's 2FA system (HSA2)."""
        pass

    def trust_session(self):
        """Request session trust to avoid user log in going forward."""
        pass

    def _get_webservice_url(self, ws_key):
        """Get webservice URL, raise an exception if not exists."""
        pass

    @property
    def devices(self):
        """Returns all devices."""
        pass

    @property
    def iphone(self):
        """Returns the iPhone."""
        pass

    @property
    def account(self):
        """Gets the 'Account' service."""
        pass

    @property
    def files(self):
        """Gets the 'File' service."""
        pass

    @property
    def photos(self):
        """Gets the 'Photo' service."""
        pass

    @property
    def calendar(self):
        """Gets the 'Calendar' service."""
        pass

    @property
    def contacts(self):
        """Gets the 'Contacts' service."""
        pass

    @property
    def reminders(self):
        """Gets the 'Reminders' service."""
        pass

    @property
    def drive(self):
        """Gets the 'Drive' service."""
        pass

    def __str__(self):
        return f"iCloud API: {self.user.get('apple_id')}"

    def __repr__(self):
        return f"<{self}>"
