Changelog
=========

All notable changes to this project will be documented in this file.

1.1.0 - 2026-02-21
------------------

- Fixed an issue where ``rqdata`` was not passed to the widget for non-invisible configurations.
- Added error handling for malformed ``verify_params`` that would previously cause the widget to fail silently.
- Added support for MFA flows (``phone_prefix`` and ``phone_number`` config parameters).

1.0.1 - 2026-02-21
------------------

- First stable release.
