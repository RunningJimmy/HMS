from widgets.bwidget import *

class RichTextWidget(QWidget):

    def __init__(self,parent=None):
        super(RichTextWidget,self).__init__(parent)
        self.initUI()
        # 添加信号槽

    #选择的文字自适应 格式
    def mergeFormatOnWordOrSelection(self, format):
        cursor = self.textEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)

        cursor.mergeCharFormat(format)
        self.textEdit.mergeCurrentCharFormat(format)

    def text(self):
        return self.textEdit.toHtml()

    def setPlaceholderText(self,p_str):
        self.textEdit.setPlaceholderText(p_str)

    # 设置加粗
    def setTextBold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(self.btn_text_bold.isChecked() and QFont.Bold or QFont.Normal)
        self.mergeFormatOnWordOrSelection(fmt)

    # 设置斜体
    def setTextItalic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.btn_text_italic.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    # 设置下划线
    def setTextUnderline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.btn_text_under.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def currentCharFormatChanged(self, format):
        self.fontChanged(format.font())
        self.colorChanged(format.foreground().color())

    # 光标变化
    def cursorPositionChanged(self):
        self.alignmentChanged(self.textEdit.alignment())

    # 设置文本对齐
    def setTextAlign(self, action):
        if action == self.btn_text_left:
            self.textEdit.setAlignment(Qt.AlignLeft | Qt.AlignAbsolute)
        elif action == self.btn_text_center:
            self.textEdit.setAlignment(Qt.AlignHCenter)
        elif action == self.btn_text_right:
            self.textEdit.setAlignment(Qt.AlignRight | Qt.AlignAbsolute)
        elif action == self.btn_text_justify:
            self.textEdit.setAlignment(Qt.AlignJustify)

    # 设置文本颜色
    def setTextColor(self):
        col = QColorDialog.getColor(self.textEdit.textColor(), self)
        if not col.isValid():
            return

        fmt = QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatOnWordOrSelection(fmt)
        self.colorChanged(col)

    # 颜色图标更新
    def colorChanged(self, color):
        pix = QPixmap(32, 32)
        pix.fill(color)
        self.btn_text_color.setIcon(QIcon(pix))

    # 设置文本字体
    def setTextFamily(self, family):
        fmt = QTextCharFormat()
        fmt.setFontFamily(family)
        self.mergeFormatOnWordOrSelection(fmt)

    # 设置文本字体大小
    def setTextSize(self, pointSize):
        pointSize = float(pointSize)
        if pointSize > 0:
            fmt = QTextCharFormat()
            fmt.setFontPointSize(pointSize)
            self.mergeFormatOnWordOrSelection(fmt)

    # 设置文本序号样式
    def setTextStyle(self, styleIndex):
        cursor = self.textEdit.textCursor()
        if styleIndex:
            styleDict = {
                1: QTextListFormat.ListDisc,
                2: QTextListFormat.ListCircle,
                3: QTextListFormat.ListSquare,
                4: QTextListFormat.ListDecimal,
                5: QTextListFormat.ListLowerAlpha,
                6: QTextListFormat.ListUpperAlpha,
                7: QTextListFormat.ListLowerRoman,
                8: QTextListFormat.ListUpperRoman,
            }

            style = styleDict.get(styleIndex, QTextListFormat.ListDisc)
            cursor.beginEditBlock()
            blockFmt = cursor.blockFormat()
            listFmt = QTextListFormat()

            if cursor.currentList():
                listFmt = cursor.currentList().format()
            else:
                listFmt.setIndent(blockFmt.indent() + 1)
                blockFmt.setIndent(0)
                cursor.setBlockFormat(blockFmt)

            listFmt.setStyle(style)
            cursor.createList(listFmt)
            cursor.endEditBlock()
        else:
            bfmt = QTextBlockFormat()
            bfmt.setObjectIndex(-1)
            cursor.mergeBlockFormat(bfmt)

    # 打印
    def filePrint(self):
        printer = QPrinter(QPrinter.HighResolution)
        dlg = QPrintDialog(printer, self)

        if self.textEdit.textCursor().hasSelection():
            dlg.addEnabledOption(QPrintDialog.PrintSelection)

        dlg.setWindowTitle("Print Document")

        if dlg.exec_() == QPrintDialog.Accepted:
            self.textEdit.print_(printer)

        del dlg

    # 打印预览
    def filePrintPreview(self):
        printer = QPrinter(QPrinter.HighResolution)
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self.printPreview)
        preview.exec_()

    def printPreview(self, printer):
        self.textEdit.print_(printer)

    def filePrintPdf(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Export PDF", None,
                "PDF files (*.pdf);;All Files (*)")

        if fn:
            if QFileInfo(fn).suffix().isEmpty():
                fn += '.pdf'

            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print_(printer)

    def initUI(self):
        lt_main = QVBoxLayout()
        self.lt_top = QHBoxLayout()
        # 功能区
        self.tb_file = QToolBar()
        self.tb_file.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
        self.btn_save = QAction(Icon('filesave'),'保存')
        self.btn_print = QAction(Icon('fileprint'), '打印')
        # self.tb_file.addAction(self.btn_save)
        # self.tb_file.addAction(self.btn_print)
        # 文本编辑
        self.tb_text_edit = QToolBar()

        self.btn_text_edit_undo = QAction(Icon('editundo'), '撤销')
        self.btn_text_edit_undo.setShortcut(QKeySequence.Undo)
        self.btn_text_edit_redo = QAction(Icon('editredo'), '前进')
        self.btn_text_edit_redo.setShortcut(QKeySequence.Redo)
        self.btn_text_edit_redo.setPriority(QAction.LowPriority)
        self.btn_text_edit_cut = QAction(Icon('editcut'),'剪切')
        self.btn_text_edit_copy = QAction(Icon('editcopy'), '复制')
        self.btn_text_edit_paste = QAction(Icon('editpaste'),'粘贴')
        # self.tb_text_edit.addAction(self.btn_text_edit_undo)
        # self.tb_text_edit.addAction(self.btn_text_edit_redo)
        # self.tb_text_edit.addAction(self.btn_text_edit_cut)
        # self.tb_text_edit.addAction(self.btn_text_edit_copy)
        # self.tb_text_edit.addAction(self.btn_text_edit_paste)
        # 文本样式
        self.tb_text_style = QToolBar()
        ################ 设置文本加粗 #####################
        self.btn_text_bold =QAction(
            QIcon.fromTheme('format-text-bold',
            Icon('textbold')),
            "加粗",
            self,
            priority=QAction.LowPriority,
            shortcut=Qt.CTRL + Qt.Key_B,
            triggered=self.setTextBold,
            checkable=True
        )
        bold = QFont()
        bold.setBold(True)
        self.btn_text_bold.setFont(bold)
        ################ 设置文本斜体 ######################
        self.btn_text_italic = QAction(
            QIcon.fromTheme('format-text-italic',
            Icon('textitalic')),
            "斜体",
            self,
            priority=QAction.LowPriority,
            shortcut=Qt.CTRL + Qt.Key_I,
            triggered=self.setTextItalic,
            checkable=True
        )
        italic = QFont()
        italic.setItalic(True)
        self.btn_text_italic.setFont(italic)
        ################### 设置文本下划线 ####################
        self.btn_text_under = QAction(
            QIcon.fromTheme('format-text-underline',
            Icon('textunder')),
            "下划线",
            self,
            priority=QAction.LowPriority,
            shortcut=Qt.CTRL + Qt.Key_U,
            triggered=self.setTextUnderline,
            checkable=True
        )
        underline = QFont()
        underline.setUnderline(True)
        self.btn_text_under.setFont(underline)
        ################### 设置文本对齐方式 ####################
        textAlignGroup = QActionGroup(self, triggered=self.setTextAlign)
        # Make sure the alignLeft is always left of the alignRight.
        if QApplication.isLeftToRight():
            self.btn_text_left = QAction(
                QIcon.fromTheme('format-justify-left',
                Icon('textleft')),
                "靠左对齐",
                textAlignGroup
            )
            self.btn_text_center = QAction(
                QIcon.fromTheme('format-justify-center',
                Icon('textcenter')),
                "居中对齐",
                textAlignGroup
            )
            self.btn_text_right = QAction(
                QIcon.fromTheme('format-justify-right',
                Icon('textright')),
                "靠右对齐",
                textAlignGroup
            )
        else:
            self.btn_text_right = QAction(
                QIcon.fromTheme('format-justify-right',
                Icon('textright')),
                "靠右对齐",
                textAlignGroup
            )
            self.btn_text_center = QAction(
                QIcon.fromTheme('format-justify-center',
                Icon('textcenter')),
                "居中对齐",
                textAlignGroup
            )
            self.btn_text_left = QAction(
                QIcon.fromTheme('format-justify-left',
                Icon('textleft')),
                "靠右对齐",
                textAlignGroup
            )
        # 双端对齐
        self.btn_text_justify = QAction(
            QIcon.fromTheme('format-justify-fill',
            Icon('textjustify')),
            "两端对齐",
            textAlignGroup
        )

        self.btn_text_left.setShortcut(Qt.CTRL + Qt.Key_L)
        self.btn_text_left.setCheckable(True)
        self.btn_text_left.setPriority(QAction.LowPriority)

        self.btn_text_center.setShortcut(Qt.CTRL + Qt.Key_E)
        self.btn_text_center.setCheckable(True)
        self.btn_text_center.setPriority(QAction.LowPriority)

        self.btn_text_right.setShortcut(Qt.CTRL + Qt.Key_R)
        self.btn_text_right.setCheckable(True)
        self.btn_text_right.setPriority(QAction.LowPriority)

        self.btn_text_justify.setShortcut(Qt.CTRL + Qt.Key_J)
        self.btn_text_justify.setCheckable(True)
        self.btn_text_justify.setPriority(QAction.LowPriority)
        # 添加布局
        self.tb_text_style.addAction(self.btn_text_bold)
        self.tb_text_style.addAction(self.btn_text_italic)
        self.tb_text_style.addAction(self.btn_text_under)
        self.tb_text_style.addAction(self.btn_text_left)
        self.tb_text_style.addAction(self.btn_text_center)
        self.tb_text_style.addAction(self.btn_text_right)
        self.tb_text_style.addAction(self.btn_text_justify)
        ################### 设置文本样式2 ####################
        self.tb_text_famly = QToolBar()
        pix = QPixmap(24, 24)
        pix.fill(Qt.red)
        self.btn_text_color = QAction(QIcon(pix), "颜色", self,triggered=self.setTextColor)

        self.cb_style = QComboBox(self)
        self.cb_style.addItems([
            "Standard","Bullet List (Disc)","Bullet List (Circle)",
            "Bullet List (Square)","Ordered List (Decimal)",
            "Ordered List (Alpha lower)","Ordered List (Alpha upper)",
            "Ordered List (Roman lower)","Ordered List (Roman upper)"
        ])
        self.cb_style.activated.connect(self.setTextStyle)

        self.cb_font = QFontComboBox(self)
        self.cb_font.activated[str].connect(self.setTextFamily)

        self.cb_font_size = QComboBox(self)
        self.cb_font_size.setObjectName("comboSize")
        self.cb_font_size.setEditable(True)
        db = QFontDatabase()
        for size in db.standardSizes():
            self.cb_font_size.addItem("%s" % (size))
        # self.cb_font_size.setCurrentIndex(6)
        self.cb_font_size.activated[str].connect(self.setTextSize)

        # 设置系统默认大小字体
        self.cb_font_size.setCurrentIndex(
            self.cb_font_size.findText(
                "%s" % (QApplication.font().pointSize()
                        )
            )
        )
        # 添加
        self.tb_text_famly.addAction(self.btn_text_color)
        self.tb_text_famly.addWidget(self.cb_style)
        self.tb_text_famly.addWidget(self.cb_font)
        self.tb_text_famly.addWidget(self.cb_font_size)
        # 内容编辑器
        self.textEdit = QTextEdit()
        # self.textEdit.currentCharFormatChanged.connect(self.currentCharFormatChanged)
        # self.textEdit.cursorPositionChanged.connect(self.cursorPositionChanged)
        # 功能区布局
        # self.lt_top.addWidget(self.tb_file)
        # self.lt_top.addWidget(Line())
        # self.lt_top.addWidget(self.tb_text_edit)
        # self.lt_top.addWidget(Line())
        self.lt_top.addWidget(self.tb_text_style)
        self.lt_top.addWidget(Line())
        self.lt_top.addWidget(self.tb_text_famly)
        self.lt_top.addStretch()
        # 添加主布局
        lt_main.addLayout(self.lt_top)
        lt_main.addWidget(self.textEdit)
        self.setLayout(lt_main)