from PyQt6.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout
from PyQt6.QtGui import QColor, QPainter, QTextFormat
from PyQt6.QtCore import QRect, QSize, Qt


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.lineNumberArea = LineNumberArea(self)

        # Ajusta el margen izquierdo para el área de los números de línea
        self.update_line_number_area_width(0)
        self.textChanged.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.update_line_number_area)

    def line_number_area_width(self):
        # Calcula el ancho del área de los números de línea
        digits = len(str(self.blockCount()))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        # Ajusta el ancho del margen izquierdo
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self):
        # Refresca el área de los números de línea
        self.viewport().update()
        self.lineNumberArea.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(230, 230, 230))  # Fondo gris claro

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(50, 50, 50))  # Color del texto del número de línea
                painter.drawText(0, top, self.lineNumberArea.width(), height,
                                 Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    editor = CodeEditor()
    editor.setPlainText("Escribe aquí...\nNueva línea.")

    layout = QVBoxLayout()
    layout.addWidget(editor)

    window = QWidget()
    window.setLayout(layout)
    window.setGeometry(200, 200, 600, 400)
    window.setWindowTitle("Editor de Código con Números de Línea")
    window.show()

    sys.exit(app.exec())
