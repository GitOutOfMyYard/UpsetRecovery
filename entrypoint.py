import sys
import os
from typing import Optional, Iterable

from PyQt5.QtWidgets import QApplication

from upset_recovery.src.main import start_app


def launch_app(app_args: Iterable[str] = ()) -> None:
    app = QApplication(list(app_args))
    start_app(app)


def _launch_for_platform(platform_flag: Optional[str]) -> None:
    if platform_flag:
        os.environ["QT_QPA_PLATFORM"] = platform_flag
    launch_app()


if __name__ == '__main__':
    module_path, *other_args = sys.argv
    qt_platform = None
    if other_args:
        qt_platform, *_ = other_args
    _launch_for_platform(qt_platform)
