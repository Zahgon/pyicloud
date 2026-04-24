"""File service."""
from datetime import datetime


class UbiquityService:
    """The 'Ubiquity' iCloud service."""

    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params

        self._root = None
        self._node_url = service_root + "/ws/%s/%s/%s"

    @property
    def root(self):
        """Gets the root node."""
        pass

    def get_node_url(self, node_id, variant="item"):
        """Returns a node URL."""
        pass

    def get_node(self, node_id):
        """Returns a node."""
        pass

    def get_children(self, node_id):
        """Returns a node children."""
        pass

    def get_file(self, node_id, **kwargs):
        """Returns a node file."""
        pass

    def __getattr__(self, attr):
        return getattr(self.root, attr)

    def __getitem__(self, key):
        return self.root[key]


class UbiquityNode:
    """Ubiquity node."""

    def __init__(self, conn, data):
        self.data = data
        self.connection = conn

        self._children = None

    @property
    def item_id(self):
        """Gets the node id."""
        pass

    @property
    def name(self):
        """Gets the node name."""
        pass

    @property
    def type(self):
        """Gets the node type."""
        pass

    @property
    def size(self):
        """Gets the node size."""
        pass

    @property
    def modified(self):
        """Gets the node modified date."""
        pass

    def open(self, **kwargs):
        """Returns the node file."""
        pass

    def get_children(self):
        """Returns the node children."""
        pass

    def dir(self):
        """Returns children node directories by their names."""
        pass

    def get(self, name):
        """Returns a child node by its name."""
        pass

    def __getitem__(self, key):
        try:
            return self.get(key)
        except IndexError as i:
            raise KeyError(f"No child named {key} exists") from i

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.type.capitalize()}: '{self}'>"
