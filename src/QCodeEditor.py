from PyQt5.QtCore import Qt, QRect, QSize, QPoint
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PyQt5.QtGui import QColor, QPainter, QTextFormat, QKeyEvent, QWheelEvent, QMouseEvent, QTextCursor

class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor


    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

class QCodeEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.document().blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.verticalScrollBar().sliderMoved.connect(self.on_scroll)
        self.verticalScrollBar().sliderReleased.connect(self.on_scroll)
        self.updateLineNumberAreaWidth(0)
        self.currentLineNumber = 0

    def wheelEvent(self, d: 'QWheelEvent') -> None:
        self.on_scroll(d)
        super(QCodeEditor, self).wheelEvent(d)

    def on_scroll(self, event: QWheelEvent = None):
        self.lineNumberArea.update()  # scroll(0, None)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        super(QCodeEditor, self).keyPressEvent(e)
        self.updateLineNumberArea(QRect(100, 100, 100, 100), None)
        self.lineNumberArea.update()

    def mousePressEvent(self, e: 'QMouseEvent') -> None:
        block_number = self.cursorForPosition(self.cursor().pos()).blockNumber()
        super().mousePressEvent(e)
        self.update()

    def lineNumberAreaWidth(self):
        digits = 1
        block_count = self.document().blockCount()
        max_value = max(1, block_count)
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, e):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        # if dy:
        #     self.lineNumberArea.scroll(0, dy)
        # else:
        #     self.lineNumberArea.update(0, self.geometry().x(), 10, self.height())
        # if rect.contains(self.viewport().rect()):
        #     self.updateLineNumberAreaWidth(0)
        _ = rect

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        newCurrentLineNumber = self.textCursor().blockNumber()
        if newCurrentLineNumber != self.currentLineNumber:
            lineColor = QColor(Qt.yellow).lighter(160)
            self.currentLineNumber = newCurrentLineNumber
            hi_selection = QTextEdit.ExtraSelection()
            hi_selection.format.setBackground(lineColor)
            hi_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            hi_selection.cursor = self.textCursor()
            hi_selection.cursor.clearSelection()
            self.setExtraSelections([hi_selection])

    def lineNumberAreaPaintEvent(self, event):
        cursor = QTextCursor(self.document())
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)
        line_height = self.fontMetrics().height()
        block_number = self.cursorForPosition(QPoint(0, int(line_height / 2))).blockNumber()
        first_visible_block = self.document().findBlock(block_number)
        blockNumber = block_number
        cursor.setPosition(self.cursorForPosition(QPoint(0, int(line_height / 2))).position())
        rect = self.cursorRect()
        last_block_number = self.cursorForPosition(QPoint(0, self.height() - 1)).blockNumber()
        last_visible_block = self.document().findBlock(last_block_number)
        mergin = 4
        small_mergin = 0.998
        top = mergin
        height = self.fontMetrics().height()
        bottom = mergin + line_height + small_mergin
        block = first_visible_block
        while block.isValid() and (top <= event.rect().bottom()) and blockNumber <= last_block_number:
            if block.isVisible():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + height + small_mergin
            blockNumber += 1

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    codeEditor = QCodeEditor()
    codeEditor.show()
    sys.exit(app.exec_())
