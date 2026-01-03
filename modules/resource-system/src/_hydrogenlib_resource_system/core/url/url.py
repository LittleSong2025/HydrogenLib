import dataclasses
from pathlib import PurePosixPath


@dataclasses.dataclass
class URLInfo:
    scheme: str
    path: PurePosixPath


def parse_url(url: str) -> URLInfo:
    sep_index = url.find(":")
    if sep_index == -1:
        scheme = url
        path = '/'
    else:
        scheme = url[:sep_index]
        path = url[sep_index + 1:]

    return URLInfo(
        scheme,
        PurePosixPath(path)
    )
