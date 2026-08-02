# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Support for, and documentation of, named "axis conventions".

### Fixed

- Add `read_latest()` since `read()` alone will return old data if not called quickly enough.
- Add `open_by_path`/`get_connected_devices_by_path` to more clearly handle multiple devices of different types [#47](https://github.com/JakubAndrysek/PySpaceMouse/pull/47).

### Changed

- Deprication warning in `open()` when `AxisConvention.LEGACY` is provided.

## [2.0.0](https://pypi.org/project/pyspacemouse/2.0.0) - 2026-01-17

### Added

### Fixed

### Changed

- Almost completely rewritten, potentially largely untested and unreviewed vibe-coding changes.

### Removed
