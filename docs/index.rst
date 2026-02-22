.. PyQtHCaptcha documentation master file, created by
   sphinx-quickstart on Sat Feb 21 19:15:19 2026.

PyQtHCaptcha
============

**PyQtHCaptcha** is a Python library that provides a native hCaptcha widget for
desktop applications using PyQt6.

Features
--------

- Supports all configuration parameters of the native mobile SDK, including
  enterprise features like ``rqdata`` and custom endpoints.
- Fully typed with modern Python type hints.
- Works with ``qasync`` for seamless integration into async applications.

Installation
------------

.. code-block:: bash

   pip install pyqt-hcaptcha

Quick Start
-----------

.. code-block:: python

   from PyQtHCaptcha import HCaptchaConfig, HCaptchaWebView

   config = HCaptchaConfig(
       sitekey="10000000-ffff-ffff-ffff-000000000001",
       url="https://accounts.hcaptcha.com/demo",
       theme="dark",
   )

   view = HCaptchaWebView(config)
   view.onSuccess.connect(lambda token: print(f"Token: {token[:40]}..."))
   view.onFailure.connect(lambda err: print(f"Error: {err}"))

   view.setWindowTitle("hCaptcha")
   view.resize(400, 600)
   view.show()

See the ``examples/`` directory for more complete examples.

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api

