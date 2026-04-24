"""Find my iPhone service."""
import json

from pyicloud.exceptions import PyiCloudNoDevicesException


class FindMyiPhoneServiceManager:
    """The 'Find my iPhone' iCloud service

    This connects to iCloud and return phone data including the near-realtime
    latitude and longitude.
    """

    def __init__(self, service_root, session, params, with_family=False):
        self.session = session
        self.params = params
        self.with_family = with_family

        fmip_endpoint = "%s/fmipservice/client/web" % service_root
        self._fmip_refresh_url = "%s/refreshClient" % fmip_endpoint
        self._fmip_sound_url = "%s/playSound" % fmip_endpoint
        self._fmip_message_url = "%s/sendMessage" % fmip_endpoint
        self._fmip_lost_url = "%s/lostDevice" % fmip_endpoint

        self._devices = {}
        self.refresh_client()

    def refresh_client(self):
        """Refreshes the FindMyiPhoneService endpoint,

        This ensures that the location data is up-to-date.

        """
        pass

    def __getitem__(self, key):
        if isinstance(key, int):
            key = list(self.keys())[key]
        return self._devices[key]

    def __getattr__(self, attr):
        return getattr(self._devices, attr)

    def __str__(self):
        return f"{self._devices}"

    def __repr__(self):
        return f"{self}"


class AppleDevice:
    """Apple device."""

    def __init__(
        self,
        content,
        session,
        params,
        manager,
        sound_url=None,
        lost_url=None,
        message_url=None,
    ):
        self.content = content
        self.manager = manager
        self.session = session
        self.params = params

        self.sound_url = sound_url
        self.lost_url = lost_url
        self.message_url = message_url

    def update(self, data):
        """Updates the device data."""
        pass

    def location(self):
        """Updates the device location."""
        pass

    def status(self, additional=[]):  # pylint: disable=dangerous-default-value
        """Returns status information for device.

        This returns only a subset of possible properties.
        """
        pass

    def play_sound(self, subject="Find My iPhone Alert"):
        """Send a request to the device to play a sound.

        It's possible to pass a custom message by changing the `subject`.
        """
        pass

    def display_message(
        self, subject="Find My iPhone Alert", message="This is a note", sounds=False
    ):
        """Send a request to the device to play a sound.

        It's possible to pass a custom message by changing the `subject`.
        """
        pass

    def lost_device(
        self, number, text="This iPhone has been lost. Please call me.", newpasscode=""
    ):
        """Send a request to the device to trigger 'lost mode'.

        The device will show the message in `text`, and if a number has
        been passed, then the person holding the device can call
        the number without entering the passcode.
        """
        pass

    @property
    def data(self):
        """Gets the device data."""
        pass

    def __getitem__(self, key):
        return self.content[key]

    def __getattr__(self, attr):
        return getattr(self.content, attr)

    def __str__(self):
        return f"{self['deviceDisplayName']}: {self['name']}"

    def __repr__(self):
        return f"<AppleDevice({self})>"
