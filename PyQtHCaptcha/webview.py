from __future__ import annotations

import json
from typing import TYPE_CHECKING
from urllib.parse import parse_qs

from PyQt6.QtCore import QTimer, QUrl, pyqtSignal
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWebEngineWidgets import QWebEngineView

if TYPE_CHECKING:
    from PyQt6.QtCore import pyqtBoundSignal
    from PyQt6.QtGui import QCloseEvent
    from PyQt6.QtWidgets import QWidget

    from .config import HCaptchaConfig

__all__ = ("HCaptchaPage", "HCaptchaWebView")


class HCaptchaPage(QWebEnginePage):
    """
    A specialized WebEnginePage that intercepts custom URI schemes.
    Acts as the delegate for handling hCaptcha bridge events.
    """

    onSuccess = pyqtSignal(str)
    onFailure = pyqtSignal(str)
    onClose = pyqtSignal()
    onExpired = pyqtSignal()
    onLoaded = pyqtSignal()

    def acceptNavigationRequest(self, url: QUrl, type, isMainFrame: bool) -> bool:
        if url.scheme() == "hcaptcha":
            action = url.host()
            if action == "success":
                query = parse_qs(url.query())
                token = query.get("token", [""])[0]
                self.onSuccess.emit(token)
            elif action == "error":
                self.onFailure.emit("hCaptcha error occurred")
            elif action == "close":
                self.onClose.emit()
            elif action == "expired":
                self.onExpired.emit()
            elif action == "loaded":
                self.onLoaded.emit()
            return False
        return super().acceptNavigationRequest(url, type, isMainFrame)


class HCaptchaWebView(QWebEngineView):
    """
    A customized QWebEngineView for rendering hCaptcha widgets.
    Uses the native 'loadHTMLString' trick with a spoofed base URL.
    """

    def __init__(self, config: HCaptchaConfig, parent: QWidget | None = None):
        super().__init__(parent)
        self.config: HCaptchaConfig = config
        self._is_loaded: bool = False

        self._page: HCaptchaPage = HCaptchaPage(self)
        self.setPage(self._page)
        self._page.onLoaded.connect(self._handle_loaded)

        self.timeout: QTimer = QTimer(self)
        self.timeout.setSingleShot(True)
        self.timeout.timeout.connect(self._handle_timeout)

        self._load_captcha()

    # Forward property references

    @property
    def onSuccess(self) -> pyqtBoundSignal:
        """Signal emitted when the hCaptcha is successfully solved. Carries the token string."""
        return self._page.onSuccess

    @property
    def onFailure(self) -> pyqtBoundSignal:
        """Signal emitted when an error occurs during the hCaptcha process. Carries an error message."""
        return self._page.onFailure

    @property
    def onClose(self) -> pyqtBoundSignal:
        """Signal emitted when the hCaptcha widget is closed by the user."""
        return self._page.onClose

    @property
    def onExpired(self) -> pyqtBoundSignal:
        """Signal emitted when the hCaptcha token expires before being used."""
        return self._page.onExpired

    @property
    def onLoaded(self) -> pyqtBoundSignal:
        """Signal emitted when the hCaptcha widget has fully loaded and is ready for interaction."""
        return self._page.onLoaded

    def _load_captcha(self):
        self.timeout.start(int(self.config.loading_timeout * 1000))

        rqdata_js = json.dumps(self.config.rqdata) if self.config.rqdata else "null"
        theme_js = json.dumps(self.config.custom_theme) if self.config.custom_theme else f"'{self.config.theme}'"
        page_theme_css = self.config.page_theme or ""

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0">
            <script src="{self.config.actual_endpoint}" async defer></script>
            <style>
                html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; display: flex;
                             justify-content: center; align-items: center; background-color: transparent; }}
                {page_theme_css}
            </style>
        </head>
        <body>
            <div id="hcaptcha-container"></div>
            <script>
                function onCaptchaSuccess(token) {{ window.location.href = 'hcaptcha://success?token=' + encodeURIComponent(token); }}
                function onCaptchaError() {{ window.location.href = 'hcaptcha://error'; }}
                function onCaptchaClose() {{ window.location.href = 'hcaptcha://close'; }}
                function onCaptchaExpired() {{ window.location.href = 'hcaptcha://expired'; }}

                var onloadCallback = function() {{
                    window.location.href = 'hcaptcha://loaded';
                    var opt = {{
                        sitekey: '{self.config.sitekey}',
                        theme: {theme_js},
                        size: '{self.config.size.value}',
                        callback: onCaptchaSuccess,
                        'error-callback': onCaptchaError,
                        'close-callback': onCaptchaClose,
                        'expired-callback': onCaptchaExpired
                    }};
                    var rqdata = {rqdata_js};
                    if (rqdata) {{ opt.rqdata = rqdata; }}
                    hcaptcha.render('hcaptcha-container', opt);
                }};
            </script>
        </body>
        </html>
        """
        self.setHtml(html, QUrl(self.config.url))

    def _handle_loaded(self):
        self._is_loaded = True
        self.timeout.stop()

    def _handle_timeout(self):
        if not self._is_loaded:
            self._page.onFailure.emit("Timeout")

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        # Ensure we don't strand async futures
        self._page.onClose.emit()
        super().closeEvent(a0)
