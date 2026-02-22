from __future__ import annotations

from enum import Enum
from urllib.parse import urlencode, urlparse, urlunparse

from .types import HCaptchaCustomTheme


class HCaptchaSize(Enum):
    """
    Specifies the visual size of the hCaptcha widget.

    :cvar invisible: For passive or background validation.
    :cvar compact: A smaller, space-saving version of the checkbox.
    :cvar normal: The standard hCaptcha checkbox size.
    """

    invisible = "invisible"
    compact = "compact"
    normal = "normal"


class HCaptchaOrientation(Enum):
    """
    Specifies the orientation of the hCaptcha widget.

    :cvar portrait: Vertical orientation.
    :cvar landscape: Horizontal orientation.
    """

    portrait = "portrait"
    landscape = "landscape"


class HCaptchaConfig:
    """
    Configuration object for customizing the behavior and appearance of the hCaptcha widget.

    :param sitekey: The Site Key sent to the hCaptcha API.
    :param url: The URL to be used to resolve Origin/Referer headers in the webview.
    :param passive_api_key: Whether the key stays invisible and requires no user interaction.
    :param size: The :class:`HCaptchaSize` of the visible area.
    :param orientation: The :class:`HCaptchaOrientation` of the widget.
    :param js_src: The URL of the hCaptcha ``api.js`` script.
    :param rqdata: Custom supplied challenge data (for Enterprise customers).
    :param sentry: Whether to enable Sentry error reporting.
    :param endpoint: Point hCaptcha JS Ajax requests to an alternative API endpoint.
    :param reportapi: Point hCaptcha bug reporting to an alternative API endpoint.
    :param assethost: Points loaded hCaptcha assets to an alternative location.
    :param imghost: Points loaded hCaptcha images to an alternative location.
    :param host: SDK's host identifier. If None, it will be generated using the sitekey.
    :param theme: The color theme of the widget (e.g., "light", "dark").
    :param custom_theme: A dictionary representing a custom theme object.
    :param page_theme: CSS styles to apply to the entire page (for custom themes).
    :param locale: A locale code (e.g., "en", "fr") to translate the widget.
    :param loading_timeout: Time (in seconds) to wait before throwing a load error..
    :param disable_pat: Whether to disable Private Access Tokens.
    """

    def __init__(
        self,
        *,
        sitekey: str,
        url: str,
        passive_sitekey: bool = False,
        size: HCaptchaSize = HCaptchaSize.normal,
        orientation: HCaptchaOrientation = HCaptchaOrientation.landscape,
        js_src: str = "https://hcaptcha.com/1/api.js",
        rqdata: str | None = None,
        sentry: bool = False,
        endpoint: str | None = None,
        reportapi: str | None = None,
        assethost: str | None = None,
        imghost: str | None = None,
        host: str | None = None,
        theme: str = "light",
        custom_theme: HCaptchaCustomTheme | None = None,
        page_theme: str | None = None,
        locale: str | None = None,
        loading_timeout: float = 5.0,
        disable_pat: bool = False,
    ):
        self.sitekey = sitekey
        self.passive_sitekey = passive_sitekey
        self.size = size
        self.orientation = orientation
        self.url = self._ensure_domain(url)
        self.js_src = js_src
        self.rqdata = rqdata
        self.sentry = sentry
        self.endpoint = endpoint
        self.reportapi = reportapi
        self.assethost = assethost
        self.imghost = imghost
        self.host = host
        self.theme = theme
        self.custom_theme = custom_theme
        self.page_theme = page_theme
        self.locale = locale
        self.loading_timeout = loading_timeout
        self.disable_pat = disable_pat

    @staticmethod
    def _ensure_domain(url: str) -> str:
        parsed = urlparse(url)
        if not parsed.scheme:
            return f"http://{url}"
        return url

    @property
    def actual_endpoint(self) -> str:
        parsed_js_src = urlparse(self.js_src)
        query_params = {
            "onload": "onloadCallback",
            "render": "explicit",
            "recaptchacompat": "off",
            # Is this suspicious? I hope not
            "host": self.host or f"{self.sitekey}.ios-sdk.hcaptcha.com",
            "sentry": str(self.sentry).lower(),
        }

        if self.endpoint:
            query_params["endpoint"] = self.endpoint
        if self.assethost:
            query_params["assethost"] = self.assethost
        if self.imghost:
            query_params["imghost"] = self.imghost
        if self.reportapi:
            query_params["reportapi"] = self.reportapi
        if self.locale:
            query_params["hl"] = self.locale
        if self.custom_theme is not None:
            query_params["custom"] = "true"
        if self.disable_pat:
            query_params["pat"] = "off"

        query_string = urlencode(query_params)
        return urlunparse(
            (
                parsed_js_src.scheme,
                parsed_js_src.netloc,
                parsed_js_src.path,
                parsed_js_src.params,
                query_string,
                parsed_js_src.fragment,
            )
        )
