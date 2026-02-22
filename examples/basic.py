from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from PyQtHCaptcha import HCaptchaConfig, HCaptchaSize, HCaptchaWebView


def on_success(token: str):
    print(f"Solution received: {token[:40]}...")

    # Proceed with backend requests...
    view.reload()


def on_failure(error: str):
    print(f"hCaptcha Error: {error}")


def on_close():
    print("hCaptcha widget closed by user")


def on_expired():
    print("hCaptcha challenge expired before completion")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    config = HCaptchaConfig(
        sitekey="10000000-ffff-ffff-ffff-000000000001",
        url="https://accounts.hcaptcha.com/demo",
        theme="dark",
        size=HCaptchaSize.normal,
    )

    view = HCaptchaWebView(config)
    view.onSuccess.connect(on_success)
    view.onFailure.connect(on_failure)
    view.onClose.connect(on_close)
    view.onExpired.connect(on_expired)

    view.setWindowTitle("hCaptcha Example")
    view.resize(400, 600)
    view.show()

    sys.exit(app.exec())
