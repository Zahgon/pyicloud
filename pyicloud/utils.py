"""Utils."""
import getpass
import keyring
import sys

from .exceptions import PyiCloudNoStoredPasswordAvailableException


KEYRING_SYSTEM = "pyicloud://icloud-password"


def get_password(username, interactive=sys.stdout.isatty()):
    """Get the password from a username."""
    pass


def password_exists_in_keyring(username):
    """Return true if the password of a username exists in the keyring."""
    pass


def get_password_from_keyring(username):
    """Get the password from a username."""
    pass


def store_password_in_keyring(username, password):
    """Store the password of a username."""
    pass


def delete_password_in_keyring(username):
    """Delete the password of a username."""
    pass


def underscore_to_camelcase(word, initial_capital=False):
    """Transform a word to camelCase."""
    pass
