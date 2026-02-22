from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from PyQtHCaptcha import HCaptchaConfig, HCaptchaError, HCaptchaSize, HCaptchaWebView


def on_loaded():
    print("hCaptcha widget loaded successfully")


def on_success(token: str):
    print(f"Solution received: {token[:40]}...")

    # Proceed with backend requests...
    view.reset()


def on_failure(error: HCaptchaError):
    print(f"hCaptcha Error: {error.name}")


def on_expired():
    print("hCaptcha token expired")


def on_open():
    print("hCaptcha challenge opened")


def on_challenge_expired():
    print("hCaptcha challenge timed out")


def on_close(irreversible: bool):
    if irreversible:
        print("hCaptcha window was closed")
    else:
        print("hCaptcha challenge dismissed by user")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    config = HCaptchaConfig(
        sitekey="10000000-ffff-ffff-ffff-000000000001",
        url="https://accounts.hcaptcha.com/demo",
        theme="dark",
        size=HCaptchaSize.normal,
    )

    view = HCaptchaWebView(config)
    view.onLoaded.connect(on_loaded)
    view.onSuccess.connect(on_success)
    view.onFailure.connect(on_failure)
    view.onExpired.connect(on_expired)
    view.onOpen.connect(on_open)
    view.onChallengeExpired.connect(on_challenge_expired)
    view.onClose.connect(on_close)

    view.setWindowTitle("hCaptcha Example")
    view.resize(400, 600)
    view.show()

    sys.exit(app.exec())
