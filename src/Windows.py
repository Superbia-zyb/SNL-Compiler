import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, \
    QApplication, QLineEdit, QInputDialog, QTextEdit, QTextBrowser, QLabel, QComboBox, QScrollBar, QFileDialog
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from main import work

class Stream(QtCore.QObject):
    """Redirects console output to text widget."""
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        sys.stdout = Stream(newText=self.console)
        self.setGeometry(200, 200, 1300, 800)
        self.setWindowTitle("SNL-Complier")

        font = QtGui.QFont("Monaco", 15)
        label_font = QtGui.QFont("Monaco", 14)

        self.Program = QTextEdit(self)
        self.Program.setAcceptRichText(False)
        self.Program.setFont(font)

        self.TokenList = QTextBrowser(self)
        self.TokenList.setFont(font)
        self.TokenList.setMaximumSize(300, 100000)

        self.SyntaxTree = QTextBrowser(self)
        self.SyntaxTree.setFont(font)

        self.SemanticTables = QTextBrowser(self)
        self.SemanticTables.setFont(font)

        self.Console = QTextBrowser(self)
        self.Console.setFont(font)
        self.ConsoleLabel = QLabel('Console', self)
        self.ProgramLabel = QLabel('Program', self)
        self.TokenListLabel = QLabel('Token List', self)
        self.SyntaxTreeLabel = QLabel("Syntax Tree", self)
        self.SemanticTablesLabel = QLabel("Semantic Tables", self)
        self.ConsoleLabel.setFont(label_font)
        self.ProgramLabel.setFont(label_font)
        self.TokenListLabel.setFont(label_font)
        self.SyntaxTreeLabel.setFont(label_font)
        self.SemanticTablesLabel.setFont(label_font)
        self.SyntaxTreeLabel.setOpenExternalLinks(True)

        self.ChooseButton = QComboBox()
        self.ChooseButton.addItem('递归下降分析')
        self.ChooseButton.addItem('LL1分析')

        self.FormatButton = QPushButton("Format")
        self.ResetButton = QPushButton("Reset")
        self.StartButton = QPushButton("Start")
        self.OpenButton = QPushButton("Open File")

        self.FormatButton.clicked.connect(self.format)
        self.ResetButton.clicked.connect(self.reset)
        self.StartButton.clicked.connect(self.start)
        self.OpenButton.clicked.connect(self.open)

        self.ProgramLayout = QVBoxLayout()
        self.TokenListLayout = QVBoxLayout()
        self.SyntaxTreeLayout = QVBoxLayout()
        self.SemanticTablesLayout = QVBoxLayout()
        self.OptionLayout = QVBoxLayout()
        self.ConsoleLayout = QVBoxLayout()
        self.first_layout = QHBoxLayout()
        self.all_h_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()
        self.layout_init()

    def open(self):
        filename = QFileDialog.getOpenFileName(self, '选择文件')
        print("choose file: \n", filename[0])
        if os.path.exists(filename[0]) is False:
            return
        with open(filename[0], "r") as f:
            txt = f.read()
            self.Program.setText(txt)

    def format(self):
        self.Program.setText("")

    def reset(self):
        self.Program.setText("")
        self.Console.setText("")
        self.SemanticTables.setText("")
        self.TokenList.setText("")
        self.SyntaxTree.setText("")

    def start(self):
        print("\n---------analysis---------")
        self.SemanticTables.setText("")
        self.TokenList.setText("")
        self.SyntaxTree.setText("")
        self.SyntaxTreeLabel.setText('Syntax Tree')

        text = self.Program.toPlainText()
        with open('../data/program.txt', 'w') as f:
            f.write(text)
        f.close()

        with open('../data/token.txt', 'w') as f:
            f.write("")
        f.close()

        with open('../data/syntax_tree.txt', 'w') as f:
            f.write("")
        f.close()

        with open('../data/semanticTables.txt', 'w') as f:
            f.write("")
        f.close()

        result = work(self.ChooseButton.currentIndex())
        if result:
            url = os.getcwd()
            url = url.split('/')[:-1]
            url = "file://" + '/'.join(url) + '/data/语法树可视化图.html'
            url = f'<a href="{url}">Syntax Tree'
            self.SyntaxTreeLabel.setText(url)

        with open('../data/token.txt', 'r') as f:
            tokenList = f.read()

        f.close()
        self.TokenList.setText(tokenList)

        with open('../data/syntax_tree.txt', 'r') as f:
            tree = f.read()
        f.close()
        self.SyntaxTree.setText(tree)

        with open('../data/semanticTables.txt', 'r') as f:
            semanticTables = f.read()
        f.close()
        self.SemanticTables.setText(semanticTables)

    def console(self, text):
        text = f"<font color='red'><red>{text}/font>"
        t = self.Console.toPlainText()
        self.Console.setText(t + text)
        self.Console.verticalScrollBar().setValue(self.Console.verticalScrollBar().maximum())

    def layout_init(self):
        self.ConsoleLayout.addWidget(self.ConsoleLabel)
        self.ConsoleLayout.addWidget(self.Console)

        self.ProgramLayout.addWidget(self.ProgramLabel)
        self.ProgramLayout.addWidget(self.Program)

        self.TokenListLayout.addWidget(self.TokenListLabel)
        self.TokenListLayout.addWidget(self.TokenList)

        self.SyntaxTreeLayout.addWidget(self.SyntaxTreeLabel)
        self.SyntaxTreeLayout.addWidget(self.SyntaxTree)

        self.SemanticTablesLayout.addWidget(self.SemanticTablesLabel)
        self.SemanticTablesLayout.addWidget(self.SemanticTables)

        self.OptionLayout.addStretch(1)
        self.OptionLayout.addWidget(self.ChooseButton)
        self.OptionLayout.addStretch(0.5)
        self.OptionLayout.addWidget(self.FormatButton)
        self.OptionLayout.addStretch(0.5)
        self.OptionLayout.addWidget(self.ResetButton)
        self.OptionLayout.addStretch(0.5)
        self.OptionLayout.addWidget(self.StartButton)
        self.OptionLayout.addStretch(0.5)
        self.OptionLayout.addWidget(self.OpenButton)

        self.all_h_layout.addLayout(self.TokenListLayout)
        self.all_h_layout.addLayout(self.SyntaxTreeLayout)
        self.all_h_layout.addLayout(self.SemanticTablesLayout)

        self.first_layout.addLayout(self.ProgramLayout)
        self.first_layout.addLayout(self.ConsoleLayout)
        self.first_layout.addLayout(self.OptionLayout)

        self.all_v_layout.addLayout(self.first_layout)
        self.all_v_layout.addLayout(self.all_h_layout)

        self.setLayout(self.all_v_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
