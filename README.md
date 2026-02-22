# PyQtHCaptcha

**PyQtHCaptcha** is a Python library that provides a native hCaptcha widget for desktop applications using PyQt6.

![PyQtHCaptcha Demo](/assets/demo.gif)

## Features

- Supports all configuration parameters of the native mobile SDK, including enterprise features like `rqdata` and custom endpoints
- Fully typed with modern Python type hints
- Works with `qasync` for seamless integration into async applications

## Installation

```bash
pip install pyqt-hcaptcha
```

## Usage

Injecting a hCaptcha widget into your PyQt application is straightforward. Below is a minimal example demonstrating how to set up the widget and connect to its signals:

```python
from PyQtHCaptcha import HCaptchaConfig, HCaptchaWebView

# Define your callbacks
def on_success(token: str):
    print(f"Solution received: {token[:40]}...")

def on_failure(error: str):
    print(f"hCaptcha Error: {error}")

def on_close():
    print("hCaptcha widget closed by user")

def on_expired():
    print("hCaptcha challenge expired before completion")

# Create a configuration for the hCaptcha widget
config = HCaptchaConfig(
    sitekey="10000000-ffff-ffff-ffff-000000000001",
    url="https://accounts.hcaptcha.com/demo",
    theme="dark",
)

# Initialize the hCaptcha widget with the configuration
view = HCaptchaWebView(config)

# Connect signals to your callbacks
view.onSuccess.connect(on_success)
view.onFailure.connect(on_failure)
view.onClose.connect(on_close)
view.onExpired.connect(on_expired)

# Show the widget
view.setWindowTitle("hCaptcha Example")
view.resize(400, 600)
view.show()
```

See the `examples/` directory for more complete examples.

## Documentation

The documentation is available [here](https://pyqt-hcaptcha.rtfd.io/).
