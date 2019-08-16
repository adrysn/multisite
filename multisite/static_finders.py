import os
from collections import OrderedDict

from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import BaseFinder
# To keep track on which directories the finder has searched the static files.
from django.contrib.staticfiles.finders import searched_locations
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import (
    FileSystemStorage,
)
from django.utils._os import safe_join

from multisite.settings import BASE_DIR


class MultiSiteFinder(BaseFinder):
    """
    A static files finder that is located in overload directories.
    """
    def __init__(self, app_names=None, *args, **kwargs):
        # List of locations with static files
        self.locations = []
        # Maps dir paths to an appropriate storage instance
        self.storages = OrderedDict()
        self.overload_base_directory = os.path.join(BASE_DIR, 'overload')
        if not os.path.exists(self.overload_base_directory):
            raise ImproperlyConfigured('There is no overload static directory.')

        for overload_dir_info in next(os.walk(self.overload_base_directory))[1]:
            static_dir = os.path.join(BASE_DIR, 'overload', overload_dir_info, 'static')
            if os.path.isdir(static_dir):
                root = static_dir
                prefix = ''
                if (prefix, root) not in self.locations:
                    self.locations.append((prefix, root))

        for prefix, root in self.locations:
            filesystem_storage = FileSystemStorage(location=root)
            filesystem_storage.prefix = prefix
            self.storages[root] = filesystem_storage

        super().__init__(*args, **kwargs)

    def find(self, path, all=False):
        """
        Looks for files in the overload directories.
        """
        matches = []
        for prefix, root in self.locations:
            if root not in searched_locations:
                searched_locations.append(root)
            matched_path = self.find_location(root, path, prefix)
            if matched_path:
                if not all:
                    return matched_path
                matches.append(matched_path)
        return matches

    def find_location(self, root, path, prefix=None):
        """
        Finds a requested static file in a location, returning the found
        absolute path (or `None` if no match).
        """
        if prefix:
            prefix = '%s%s' % (prefix, os.sep)
            if not path.startswith(prefix):
                return None
            path = path[len(prefix):]
        path = safe_join(root, path)
        if os.path.exists(path):
            return path

    def list(self, ignore_patterns):
        """
        List all files in all locations.
        """
        for prefix, root in self.locations:
            storage = self.storages[root]
            for path in utils.get_files(storage, ignore_patterns):
                yield path, storage
