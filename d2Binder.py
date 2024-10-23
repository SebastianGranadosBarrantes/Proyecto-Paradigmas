from PyQt6.QtCore import pyqtSignal, QObject


class TextModel(QObject):
    # Declare the pyqtSignal
    text_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._text = ""

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text):
        if self._text != new_text:
            self._text = new_text
            # Emit the signal
            self.text_changed.textEdited(self._text)


