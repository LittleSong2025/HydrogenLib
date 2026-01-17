"""
Use:
    import ...
    user32 = Dll('user32')

    @user32
    def MessageBoxW(hwnd: int, text: str, caption: str, uType: int) -> int: ...
"""

from ._dll import DLL
from ._func import c_function
from ._types import *
