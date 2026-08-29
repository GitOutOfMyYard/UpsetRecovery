from typing import NamedTuple


class LoginDataDto(NamedTuple):
    group: str
    last_name: str
    first_name: str
    middle_name: str
