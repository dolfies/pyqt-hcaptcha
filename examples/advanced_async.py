from __future__ import annotations

import asyncio
import sys

import qasync
from PyQt6.QtWidgets import QApplication, QWidget

from PyQtHCaptcha import HCaptchaConfig, HCaptchaSize, HCaptchaWebView
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

    def on_success(token: str):
        if not future.done():
            future.set_result(token)
        webview.close()

    def on_failure(error: str):
        if not future.done():
            future.set_exception(Exception(f"hCaptcha Error: {error}"))
        webview.close()

    def on_close():
        if not future.done():
            future.set_exception(asyncio.CancelledError("hCaptcha widget closed by user"))

    def on_expired():
        if not future.done():
            future.set_exception(Exception("hCaptcha challenge expired before completion"))
        webview.close()

    webview.onSuccess.connect(on_success)
    webview.onFailure.connect(on_failure)
    webview.onClose.connect(on_close)
    webview.onExpired.connect(on_expired)

    webview.show()

    return await future


async def main():
    try:
        config = HCaptchaConfig(
            sitekey="10000000-ffff-ffff-ffff-000000000001",
            url="https://accounts.hcaptcha.com/demo",
            custom_theme=BRAND_THEME,
            size=HCaptchaSize.normal,
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
