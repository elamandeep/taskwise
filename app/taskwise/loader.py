import os
import sys
from importlib import import_module


class ThemeLoader:
    def __init__(self) -> None:
        self.themes = []
        try:
            for i in os.listdir("themes"):
                if not i.startswith("__"):
                    sys.path.append("themes/" + i + "/")
                    self.themes.append(i)

        except ImportError as e:
            print(e)

    def load_specific_theme(self, theme: str):
        try:
            theme_module = import_module(theme)
            print("loading module")
            return theme_module
        except ImportError as e:
            print(e)


if __name__ == "__main__":
    obj = ThemeLoader()
    theme = "vite"
    mod = obj.load_specific_theme(theme)
