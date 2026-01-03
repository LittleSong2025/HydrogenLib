from pathlib import PurePosixPath
from typing import NamedTuple

from . import errors
from .provider import ResourceProvider
from .provider.builtin_providers import URLProvider
from .url import parse_url, URLInfo


class MountInfo(NamedTuple):
    path: PurePosixPath
    provider: ResourceProvider

    def get(self, path, query, rs):
        return self.provider.get(path, query, rs)

    def remove(self, path, query, rs):
        return self.provider.remove(path, query, rs)

    def list(self, path, query, rs):
        return self.provider.list(path, query, rs)

    def set(self, path, data, query, rs):
        return self.provider.set(path, data, query, rs)

    def exists(self, path, query, rs):
        return self.provider.exists(path, query, rs)


class CoreResourceSystem:

    def __init__(self):
        self._mounttab = {}  # type: dict[str, list[MountInfo]]

    def mount(self, prefix: str, provider: ResourceProvider | type[ResourceProvider] = URLProvider):
        URLInfo = parse_url(prefix)
        scheme, path = URLInfo.scheme, URLInfo.path

        if scheme not in self._mounttab:
            self._mounttab[scheme] = []

        if isinstance(provider, type):
            provider = provider()

        self._mounttab[scheme].append(MountInfo(path, provider))

    def find_mount(self, url: str) -> tuple[MountInfo | None, URLInfo]:
        url_info = parse_url(url)
        scheme, path = url_info.scheme, url_info.path

        if scheme in self._mounttab:
            for mountinfo in self._mounttab[scheme]:
                mpath = mountinfo.path
                if path.is_relative_to(mpath):
                    return mountinfo, url_info

        return None, url_info

    def get_mount(self, url: str) -> tuple[MountInfo, URLInfo]:
        minfo, url_info = self.find_mount(url)
        if minfo is None:
            raise errors.ResourceNotFound(url)
        return minfo, url_info

    def get(self, url: str, **query):
        minfo, url_info = self.get_mount(url)
        return minfo.get(url_info.path, query, self)

    def remove(self, url: str, **query):
        minfo, url_info = self.get_mount(url)
        return minfo.remove(url_info.path, query, self)

    def set(self, url: str, data, **query):
        minfo, url_info = self.get_mount(url)
        return minfo.set(url_info.path, data, query, self)

    def list(self, url: str, **query):
        minfo, url_info = self.get_mount(url)
        return minfo.list(url_info.path, query, self)

    def exists(self, url: str, **query):
        minfo, url_info = self.get_mount(url)
        return minfo.exists(url_info.path, query, self)

    def close(self):
        for ls in self._mounttab.values():
            for minfo in ls:
                provider = minfo.provider
                provider.close()
