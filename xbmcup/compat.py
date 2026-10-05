# -*- coding: utf-8 -*-

import base64
import copy
import sys

PY2 = sys.version_info[0] == 2
PY3 = not PY2

if PY2:
    text_type = unicode  # noqa: F821
    binary_type = str
    string_types = (str, unicode)  # noqa: F821

    from urllib import quote, quote_plus, unquote, unquote_plus, urlencode, pathname2url
    from urlparse import parse_qs, parse_qsl, urljoin, urlparse, urlsplit, urlunparse, urldefrag
    from urllib2 import (
        BaseHandler,
        build_opener,
        install_opener,
        HTTPCookieProcessor,
        HTTPError,
        HTTPHandler,
        HTTPRedirectHandler,
        ProxyBasicAuthHandler,
        ProxyHandler,
        Request,
        urlopen,
    )
    from httplib import HTTPConnection, HTTPMessage
    from cookielib import Cookie, MozillaCookieJar
    from htmlentitydefs import name2codepoint
    import xmlrpclib
else:
    text_type = str
    binary_type = bytes
    string_types = (str,)

    from urllib.parse import (
        parse_qs,
        parse_qsl,
        quote,
        quote_plus,
        unquote,
        unquote_plus,
        urlencode,
        urljoin,
        urlparse,
        urlsplit,
        urlunparse,
        urldefrag,
    )
    from urllib.request import (
        BaseHandler,
        build_opener,
        install_opener,
        HTTPCookieProcessor,
        HTTPHandler,
        HTTPRedirectHandler,
        pathname2url,
        ProxyBasicAuthHandler,
        ProxyHandler,
        Request,
        urlopen,
    )
    from urllib.error import HTTPError
    from http.client import HTTPConnection, HTTPMessage
    from http.cookiejar import Cookie, MozillaCookieJar
    from html.entities import name2codepoint
    from xmlrpc import client as xmlrpclib


SENSITIVE_KEYS = (
    "authorization",
    "auth_password",
    "cookie",
    "login_password",
    "password",
    "proxy_password",
    "rutracker_password",
    "set-cookie",
)


def ensure_text(value, encoding="utf-8", errors="replace"):
    if value is None:
        return u""
    if isinstance(value, text_type):
        return value
    if isinstance(value, binary_type):
        return value.decode(encoding, errors)
    return text_type(value)


def ensure_binary(value, encoding="utf-8", errors="strict"):
    if value is None:
        return b""
    if isinstance(value, binary_type):
        return value
    if isinstance(value, text_type):
        return value.encode(encoding, errors)
    return text_type(value).encode(encoding, errors)


def to_cp1251(value, errors="replace"):
    return ensure_text(value).encode("windows-1251", errors)


def b64encode_text(value):
    encoded = base64.b64encode(ensure_binary(value))
    if isinstance(encoded, binary_type):
        return encoded.decode("ascii")
    return encoded


def translate_path(path):
    try:
        import xbmc
        return xbmc.translatePath(path)
    except (AttributeError, ImportError):
        import xbmcvfs
        return xbmcvfs.translatePath(path)


def _is_sensitive_key(key):
    key = ensure_text(key).lower()
    for token in SENSITIVE_KEYS:
        if token in key:
            return True
    return False


def redact(value):
    try:
        if isinstance(value, dict):
            result = {}
            for key, item in value.items():
                result[key] = "***" if _is_sensitive_key(key) else redact(item)
            return result
        if isinstance(value, (list, tuple)):
            result = []
            for item in value:
                if (
                    isinstance(item, (list, tuple))
                    and len(item) == 2
                    and _is_sensitive_key(item[0])
                ):
                    result.append((item[0], "***"))
                else:
                    result.append(redact(item))
            return tuple(result) if isinstance(value, tuple) else result
        if hasattr(value, "__dict__"):
            obj = copy.copy(value)
            for key, item in obj.__dict__.items():
                setattr(obj, key, "***" if _is_sensitive_key(key) else redact(item))
            return obj
    except Exception:
        pass
    return value
