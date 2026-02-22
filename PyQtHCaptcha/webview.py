from __future__ import annotations

import json
from enum import IntEnum
from typing import TYPE_CHECKING

from PyQt6.QtCore import QTimer, QUrl, pyqtSignal
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWebEngineWidgets import QWebEngineView

if TYPE_CHECKING:
    from PyQt6.QtCore import pyqtBoundSignal
    from PyQt6.QtGui import QCloseEvent
    from PyQt6.QtWidgets import QWidget

    from .config import HCaptchaConfig

__all__ = ("HCaptchaError", "HCaptchaPage", "HCaptchaWebView")


class HCaptchaError(IntEnum):
    """
    Error codes returned by the hCaptcha widget.

    :cvar htmlLoadError: The HTML failed to load.
    :cvar networkError: A network error occurred loading the hCaptcha script.
    :cvar sessionTimeout: The captcha session or token timed out.
    :cvar failedSetup: The hCaptcha widget failed to render.
    :cvar challengeClosed: The user dismissed the challenge.
    :cvar rateLimit: The request was rate limited.
    :cvar wrongMessageFormat: An unrecognized message was received from the webview.
    """

    htmlLoadError = 1
    networkError = 7
    sessionTimeout = 15
    failedSetup = 29
    challengeClosed = 30
    rateLimit = 31
    wrongMessageFormat = -1


class HCaptchaPage(QWebEnginePage):
    """
    A specialized WebEnginePage that intercepts custom URI schemes.
    Acts as the delegate for handling hCaptcha bridge events.
    """

    onLoaded = pyqtSignal()
    onSuccess = pyqtSignal(str)
    onFailure = pyqtSignal(object)
    onExpired = pyqtSignal()
    onShow = pyqtSignal()
    onOpen = pyqtSignal()
    onChallengeExpired = pyqtSignal()
    onClose = pyqtSignal(bool)

    _MSG_PREFIX = "__hcaptcha__:"

    def javaScriptConsoleMessage(
        self, level: QWebEnginePage.JavaScriptConsoleMessageLevel, message: str | None, lineNumber: int, sourceID: str | None
    ) -> None:
        if not message or not message.startswith(self._MSG_PREFIX):
            return
        try:
            data = json.loads(message[len(self._MSG_PREFIX) :])
        except json.JSONDecodeError:
            return
        if "token" in data:
            self.onSuccess.emit(data["token"])
        elif "error" in data:
            try:
                self.onFailure.emit(HCaptchaError(data["error"]))
            except ValueError:
                self.onFailure.emit(HCaptchaError.wrongMessageFormat)
        elif "action" in data:
            action = data["action"]
            if action == "didLoad":
                self.onLoaded.emit()
            elif action == "showHCaptcha":
                self.onShow.emit()
            elif action == "onOpen":
                self.onOpen.emit()
            elif action == "onExpired":
                self.onExpired.emit()
            elif action == "onChallengeExpired":
                self.onChallengeExpired.emit()
            elif action == "onClose":
                self.onClose.emit(False)


class HCaptchaWebView(QWebEngineView):
    """
    A customized QWebEngineView for rendering hCaptcha widgets.

    :param config: An instance of :class:`HCaptchaConfig` containing the widget configuration.
    :param parent: An optional parent widget.
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

    def isLoaded(self) -> bool:
        """Returns whether the hCaptcha widget has loaded successfully."""
        return self._is_loaded

    @property
    def onLoaded(self) -> pyqtBoundSignal:
        """Signal emitted when the hCaptcha widget has fully loaded and is ready for interaction."""
        return self._page.onLoaded

    @property
    def onSuccess(self) -> pyqtBoundSignal:
        """Signal emitted when the hCaptcha is successfully solved. Carries the token string."""
        return self._page.onSuccess

    @property
    def onFailure(self) -> pyqtBoundSignal:
        """Signal emitted when an error occurs. Carries an :class:`~PyQtHCaptcha.HCaptchaError` value."""
        return self._page.onFailure

    @property
    def onShow(self) -> pyqtBoundSignal:
        """Signal emitted when the hCaptcha widget requests to be made visible (e.g., for invisible captchas)."""
        return self._page.onShow

    @property
    def onOpen(self) -> pyqtBoundSignal:
        """Signal emitted when the hCaptcha challenge modal is opened."""
        return self._page.onOpen

    @property
    def onChallengeExpired(self) -> pyqtBoundSignal:
        """Signal emitted when the active challenge expires before the user completes it."""
        return self._page.onChallengeExpired

    @property
    def onClose(self) -> pyqtBoundSignal:
        """Signal emitted when the user dismisses the hCaptcha challenge. Carries a boolean indicating whether the close is irreversible (i.e. window was closed)."""
        return self._page.onClose

    @property
    def onExpired(self) -> pyqtBoundSignal:
        """Signal emitted when the hCaptcha token expires before being used."""
        return self._page.onExpired

    def execute(self) -> None:
        """Programmatically trigger the challenge for invisible captchas. Only necessary to trigger again if the challenge was dismissed or expired without a solution."""
        self._page.runJavaScript("if (window.hcaptcha) { hcaptcha.execute(window._hcaptchaOpts); }")

    def reset(self) -> None:
        """Reset the hCaptcha widget back to its initial state."""
        self._page.runJavaScript("if (window.hcaptcha) { hcaptcha.reset(); }")

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
            <style>
                html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; display: flex;
                             justify-content: center; align-items: center; background-color: transparent; }}
                {page_theme_css}
            </style>
            <script>
                var post = function(data) {{ console.log('__hcaptcha__:' + JSON.stringify(data)); }};

                var onPass = function(token) {{ post({{ token: token }}); }};
                var expiredCallback = function(action) {{
                    return function() {{
                        post({{ error: 15 }});
                        post({{ action: action }});
                    }};
                }};
                var errorCallback = function(error) {{ post({{ error: 31 }}); }};
                var closeCallback = function() {{
                    post({{ error: 30 }});
                    post({{ action: 'onClose' }});
                }};
                var openCallback = function(e) {{
                    post({{ action: 'showHCaptcha' }});
                    post({{ action: 'onOpen' }});
                }};

                var onloadCallback = function() {{
                    try {{
                        var rqdata = {rqdata_js};
                        var opt = {{
                            sitekey: '{self.config.sitekey}',
                            theme: {theme_js},
                            size: '{self.config.size.value}',
                            orientation: '{self.config.orientation.value}',
                            callback: onPass,
                            'error-callback': errorCallback,
                            'close-callback': closeCallback,
                            'expired-callback': expiredCallback('onExpired'),
                            'chalexpired-callback': expiredCallback('onChallengeExpired'),
                            'open-callback': openCallback
                        }};
                        if (rqdata) {{ opt.rqdata = rqdata; }}
                        window._hcaptchaOpts = rqdata ? {{ rqdata: rqdata }} : undefined;
                        hcaptcha.render('hcaptcha-container', opt);
                        if ('{self.config.size.value}' === 'invisible') {{
                            hcaptcha.execute(window._hcaptchaOpts);
                        }}
                        setTimeout(function() {{ post({{ action: 'didLoad' }}); }}, 0);
                    }} catch (e) {{
                        post({{ error: 29 }});
                    }}
                }};

                document.addEventListener('DOMContentLoaded', function() {{
                    var container = document.getElementById('hcaptcha-container');
                    container.addEventListener('click', function() {{
                        if (window.hcaptcha) {{
                            hcaptcha.close();
                        }} else {{
                            post({{ error: 30 }});
                            post({{ action: 'onClose' }});
                        }}
                    }});
                }});

                var script = document.createElement('script');
                script.src = '{self.config.actual_endpoint}';
                script.onerror = function() {{ post({{ error: 7 }}); }};
                document.head.appendChild(script);
            </script>
        </head>
        <body>
            <div id="hcaptcha-container"></div>
        </body>
        </html>
        """
        self.setHtml(html, QUrl(self.config.url))

    def _handle_loaded(self):
        self._is_loaded = True
        self.timeout.stop()

    def _handle_timeout(self):
        if not self._is_loaded:
            self._page.onFailure.emit(HCaptchaError.htmlLoadError)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        # Ensure we don't strand async futures
        self._page.onClose.emit(True)
        super().closeEvent(a0)
