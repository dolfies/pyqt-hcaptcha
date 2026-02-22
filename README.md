# PyQtHCaptcha

**PyQtHCaptcha** is a Python library that provides a native hCaptcha widget for desktop applications using PyQt6.

![PyQtHCaptcha Demo](/assets/demo.gif)

## Features

- Supports all configuration parameters of the native mobile SDK, including enterprise features like `rqdata` and custom endpoints
- Supports passive mode captchas with invisibles challenges
- Fully typed with modern Python type hints
- Works with `qasync` for seamless integration into async applications

## Installation

```bash
pip install pyqt-hcaptcha
```

## Usage

Injecting a hCaptcha widget into your PyQt application is straightforward. Below is a minimal example demonstrating how to set up the widget and connect to its signals:

```python
from PyQtHCaptcha import HCaptchaConfig, HCaptchaError, HCaptchaWebView

# Define your callbacks
def on_loaded():
    print("hCaptcha widget loaded successfully")

def on_success(token: str):
    print(f"Solution received: {token[:40]}...")

def on_failure(error: HCaptchaError):
    print(f"hCaptcha Error: {error.name}")

def on_expired():
    print("hCaptcha token expired")

# Create a configuration for the hCaptcha widget
config = HCaptchaConfig(
    sitekey="10000000-ffff-ffff-ffff-000000000001",
    url="https://accounts.hcaptcha.com/demo",
    theme="dark",
)

# Initialize the hCaptcha widget with the configuration
view = HCaptchaWebView(config)

# Connect signals to your callbacks
view.onLoaded.connect(on_loaded)
view.onSuccess.connect(on_success)
view.onFailure.connect(on_failure)
view.onExpired.connect(on_expired)

# Show the widget
view.setWindowTitle("hCaptcha Example")
view.resize(400, 600)
view.show()
```

See the `examples/` directory for more complete examples.

## Documentation

The documentation is available [here](https://pyqt-hcaptcha.rtfd.io/).
