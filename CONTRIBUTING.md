# Contributing

Contributions should keep the tool simple for non-programmers.

## Rules

- Keep the default path local-only: `127.0.0.1`.
- Do not add online telemetry, analytics, or background network calls.
- Do not silently modify NVIDIA DRS global profile settings.
- Keep restore behavior manifest-based, not blind deletion.
- Keep Windows paths and non-admin usage clear in the UI.

## Before Submitting

1. Run `python -m py_compile app.py`.
2. Start `run.bat` and open `http://127.0.0.1:22532`.
3. Test path detection with a real game folder or a fake `Client\WindowsNoEditor\HT\Binaries\Win64\HTGame.exe` layout.
4. Test install and restore on a disposable copy before testing on a real game folder.
5. Update `README.md` and `docs/` if behavior changes.
