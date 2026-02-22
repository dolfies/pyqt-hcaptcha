from __future__ import annotations

import asyncio
import sys

import qasync
from PyQt6.QtWidgets import QApplication, QWidget

from PyQtHCaptcha import HCaptchaConfig, HCaptchaError, HCaptchaSize, HCaptchaWebView
from PyQtHCaptcha.types import HCaptchaCustomTheme

BRAND_THEME: HCaptchaCustomTheme = {
    "palette": {"primary": {"main": "#00FF00"}, "text": {"heading": "#0A6A6A", "body": "#438D55"}},
}


async def solve_hcaptcha(config: HCaptchaConfig, parent: QWidget | None = None, title: str = "hCaptcha Example") -> str:
    """Asynchronously launches the hCaptcha widget and waits for the user to solve it."""
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    webview = HCaptchaWebView(config, parent)
    webview.setWindowTitle(title)
    webview.resize(400, 600)

    def on_loaded():
        print("hCaptcha widget loaded successfully")

    def on_success(token: str):
        print("hCaptcha solution received")
        if not future.done():
            future.set_result(token)
        webview.hide()

    def on_failure(error: HCaptchaError):
        print(f"hCaptcha error: {error.name}")
        if not future.done():
            future.set_exception(Exception(f"hCaptcha Error: {error.name}"))
        webview.hide()

    def on_expired():
        print("hCaptcha token expired")

    def on_show():
        print("hCaptcha challenge required")
        webview.show()

    def on_open():
        print("hCaptcha challenge opened")

    def on_challenge_expired():
        if not future.done():
            future.set_exception(Exception("hCaptcha challenge timed out"))
        webview.close()

    def on_close(irreversible: bool):
        if irreversible and not future.done():
            future.set_exception(asyncio.CancelledError("hCaptcha window was closed"))
            return
        print("hCaptcha challenge dismissed by user")
        webview.hide()
        webview.execute()

    webview.onLoaded.connect(on_loaded)
    webview.onSuccess.connect(on_success)
    webview.onFailure.connect(on_failure)
    webview.onExpired.connect(on_expired)
    webview.onShow.connect(on_show)
    webview.onOpen.connect(on_open)
    webview.onChallengeExpired.connect(on_challenge_expired)
    webview.onClose.connect(on_close)

    return await future


async def main():
    try:
        config = HCaptchaConfig(
            sitekey="10000000-ffff-ffff-ffff-000000000001",
            url="https://accounts.hcaptcha.com/demo",
            custom_theme=BRAND_THEME,
            # Invisible captcha
            size=HCaptchaSize.invisible,
        )
        token = await solve_hcaptcha(config)

        # Proceed with backend requests...
        print(f"Solution received: {token[:40]}...")
    except asyncio.CancelledError:
        print("Challenge was cancelled by the user")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    with loop:
        loop.run_until_complete(main())
