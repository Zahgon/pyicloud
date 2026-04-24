"""Photo service."""
import json
import base64
from urllib.parse import urlencode

from datetime import datetime, timezone
from pyicloud.exceptions import PyiCloudServiceNotActivatedException


class PhotosService:
    """The 'Photos' iCloud service."""

    SMART_FOLDERS = {
        "All Photos": {
            "obj_type": "CPLAssetByAddedDate",
            "list_type": "CPLAssetAndMasterByAddedDate",
            "direction": "ASCENDING",
            "query_filter": None,
        },
        "Time-lapse": {
            "obj_type": "CPLAssetInSmartAlbumByAssetDate:Timelapse",
            "list_type": "CPLAssetAndMasterInSmartAlbumByAssetDate",
            "direction": "ASCENDING",
            "query_filter": [
                {
                    "fieldName": "smartAlbum",
                    "comparator": "EQUALS",
                    "fieldValue": {"type": "STRING", "value": "TIMELAPSE"},
                }
            ],
        },
        "Videos": {
            "obj_type": "CPLAssetInSmartAlbumByAssetDate:Video",
            "list_type": "CPLAssetAndMasterInSmartAlbumByAssetDate",
            "direction": "ASCENDING",
            "query_filter": [
                {
                    "fieldName": "smartAlbum",
                    "comparator": "EQUALS",
                    "fieldValue": {"type": "STRING", "value": "VIDEO"},
                }
            ],
        },
        "Slo-mo": {
            "obj_type": "CPLAssetInSmartAlbumByAssetDate:Slomo",
            "list_type": "CPLAssetAndMasterInSmartAlbumByAssetDate",
            "direction": "ASCENDING",
            "query_filter": [
                {
                    "fieldName": "smartAlbum",
                    "comparator": "EQUALS",
                    "fieldValue": {"type": "STRING", "value": "SLOMO"},
                }
            ],
        },
        "Bursts": {
            "obj_type": "CPLAssetBurstStackAssetByAssetDate",
            "list_type": "CPLBurstStackAssetAndMasterByAssetDate",
            "direction": "ASCENDING",
            "query_filter": None,
        },
        "Favorites": {
            "obj_type": "CPLAssetInSmartAlbumByAssetDate:Favorite",
            "list_type": "CPLAssetAndMasterInSmartAlbumByAssetDate",
            "direction": "ASCENDING",
            "query_filter": [
                {
                    "fieldName": "smartAlbum",
                    "comparator": "EQUALS",
                    "fieldValue": {"type": "STRING", "value": "FAVORITE"},
                }
            ],
        },
        "Panoramas": {
            "obj_type": "CPLAssetInSmartAlbumByAssetDate:Panorama",
            "list_type": "CPLAssetAndMasterInSmartAlbumByAssetDate",
            "direction": "ASCENDING",
            "query_filter": [
                {
                    "fieldName": "smartAlbum",
                    "comparator": "EQUALS",
                    "fieldValue": {"type": "STRING", "value": "PANORAMA"},
                }
            ],
        },
        "Screenshots": {
            "obj_type": "CPLAssetInSmartAlbumByAssetDate:Screenshot",
            "list_type": "CPLAssetAndMasterInSmartAlbumByAssetDate",
            "direction": "ASCENDING",
            "query_filter": [
                {
                    "fieldName": "smartAlbum",
                    "comparator": "EQUALS",
                    "fieldValue": {"type": "STRING", "value": "SCREENSHOT"},
                }
            ],
        },
        "Live": {
            "obj_type": "CPLAssetInSmartAlbumByAssetDate:Live",
            "list_type": "CPLAssetAndMasterInSmartAlbumByAssetDate",
            "direction": "ASCENDING",
            "query_filter": [
                {
                    "fieldName": "smartAlbum",
                    "comparator": "EQUALS",
                    "fieldValue": {"type": "STRING", "value": "LIVE"},
                }
            ],
        },
        "Recently Deleted": {
            "obj_type": "CPLAssetDeletedByExpungedDate",
            "list_type": "CPLAssetAndMasterDeletedByExpungedDate",
            "direction": "ASCENDING",
            "query_filter": None,
        },
        "Hidden": {
            "obj_type": "CPLAssetHiddenByAssetDate",
            "list_type": "CPLAssetAndMasterHiddenByAssetDate",
            "direction": "ASCENDING",
            "query_filter": None,
        },
    }

    def __init__(self, service_root, session, params):
        self.session = session
        self.params = dict(params)
        self._service_root = service_root
        self.service_endpoint = (
            "%s/database/1/com.apple.photos.cloud/production/private"
            % self._service_root
        )

        self._albums = None

        self.params.update({"remapEnums": True, "getCurrentSyncToken": True})

        url = f"{self.service_endpoint}/records/query?{urlencode(self.params)}"
        json_data = (
            '{"query":{"recordType":"CheckIndexingState"},'
            '"zoneID":{"zoneName":"PrimarySync"}}'
        )
        request = self.session.post(
            url, data=json_data, headers={"Content-type": "text/plain"}
        )
        response = request.json()
        indexing_state = response["records"][0]["fields"]["state"]["value"]
        if indexing_state != "FINISHED":
            raise PyiCloudServiceNotActivatedException(
                "iCloud Photo Library not finished indexing. "
                "Please try again in a few minutes."
            )

        # TODO: Does syncToken ever change?  # pylint: disable=fixme
        # self.params.update({
        #     'syncToken': response['syncToken'],
        #     'clientInstanceId': self.params.pop('clientId')
        # })

        self._photo_assets = {}

    @property
    def albums(self):
        """Returns photo albums."""
        pass

    def _fetch_folders(self):
        pass

    @property
    def all(self):
        """Returns all photos."""
        pass


class PhotoAlbum:
    """A photo album."""

    def __init__(
        self,
        service,
        name,
        list_type,
        obj_type,
        direction,
        query_filter=None,
        page_size=100,
    ):
        self.name = name
        self.service = service
        self.list_type = list_type
        self.obj_type = obj_type
        self.direction = direction
        self.query_filter = query_filter
        self.page_size = page_size

        self._len = None

    @property
    def title(self):
        """Gets the album name."""
        pass

    def __iter__(self):
        return self.photos

    def __len__(self):
        if self._len is None:
            url = "{}/internal/records/query/batch?{}".format(
                self.service.service_endpoint,
                urlencode(self.service.params),
            )
            request = self.service.session.post(
                url,
                data=json.dumps(
                    {
                        "batch": [
                            {
                                "resultsLimit": 1,
                                "query": {
                                    "filterBy": {
                                        "fieldName": "indexCountID",
                                        "fieldValue": {
                                            "type": "STRING_LIST",
                                            "value": [self.obj_type],
                                        },
                                        "comparator": "IN",
                                    },
                                    "recordType": "HyperionIndexCountLookup",
                                },
                                "zoneWide": True,
                                "zoneID": {"zoneName": "PrimarySync"},
                            }
                        ]
                    }
                ),
                headers={"Content-type": "text/plain"},
            )
            response = request.json()

            self._len = response["batch"][0]["records"][0]["fields"]["itemCount"][
                "value"
            ]

        return self._len

    @property
    def photos(self):
        """Returns the album photos."""
        pass

    def _list_query_gen(self, offset, list_type, direction, query_filter=None):
        pass

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<{type(self).__name__}: '{self}'>"


class PhotoAsset:
    """A photo."""

    def __init__(self, service, master_record, asset_record):
        self._service = service
        self._master_record = master_record
        self._asset_record = asset_record

        self._versions = None

    PHOTO_VERSION_LOOKUP = {
        "original": "resOriginal",
        "medium": "resJPEGMed",
        "thumb": "resJPEGThumb",
    }

    VIDEO_VERSION_LOOKUP = {
        "original": "resOriginal",
        "medium": "resVidMed",
        "thumb": "resVidSmall",
    }

    @property
    def id(self):
        """Gets the photo id."""
        pass

    @property
    def filename(self):
        """Gets the photo file name."""
        pass

    @property
    def size(self):
        """Gets the photo size."""
        pass

    @property
    def created(self):
        """Gets the photo created date."""
        pass

    @property
    def asset_date(self):
        """Gets the photo asset date."""
        pass

    @property
    def added_date(self):
        """Gets the photo added date."""
        pass

    @property
    def dimensions(self):
        """Gets the photo dimensions."""
        pass

    @property
    def versions(self):
        """Gets the photo versions."""
        pass

    def download(self, version="original", **kwargs):
        """Returns the photo file."""
        pass

    def delete(self):
        """Deletes the photo."""
        pass

    def __repr__(self):
        return f"<{type(self).__name__}: id={self.id}>"
