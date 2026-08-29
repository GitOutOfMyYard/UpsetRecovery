from abc import ABC, abstractmethod
from typing import Callable, Optional

from upset_recovery.src.dtos import LoginDataDto


class IWelcomingView(ABC):
    @abstractmethod
    def set_prepare_test_callback(self, callback: Callable[[], None]) -> None:
        pass

    @abstractmethod
    def login_user(self) -> None:
        pass

    @abstractmethod
    def set_start_test_callback(self, callback: Callable[[], None]) -> None:
        pass

    @abstractmethod
    def set_start_train_callback(self, callback: Callable[[], None]) -> None:
        pass

    @abstractmethod
    def get_login_data(self) -> Optional[LoginDataDto]:
        pass


class IUpsetRecoveryLoopView(ABC):

    @abstractmethod
    def __init__(self, test=True, presenter=None) -> None:
        pass