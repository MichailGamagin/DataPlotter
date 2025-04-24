"""
В этом файле содержатся все стили QSS применяемые в программе для различных виджетов
"""

from src.utils import resources

SPIN_BOX_STYLE = str(
"""
QSpinBox {
        border: 1px solid #ced4da;
        border-radius: 6px;
        padding: 6px 12px; 
		min-width: 4em;
        max-width: 8em;
        background-color: #fff;
        color: #495057;
 }
QSpinBox::down-button {
	image: url(:/resources/arrow-down.png);
    height: 20px;
    width: 20px;
}
QSpinBox::up-button {
	image: url(:/resources/arrow-up.png);
    height: 20px;
    width: 20px;
}
QSpinBox:focus {
       border: 1px solid #80bdff;
       outline: none;
}
QSpinBox:hover {
        border-color: #495057;
}
"""
)
COMBO_STYLE = str(
    "QComboBox {\n"
    "    border: 1px solid #ced4da;\n"
    "    border-radius: 6px;\n"
    "    padding: 6px 12px; \n"
    "    min-width: 4em;\n"
    "    max-width: 8em;\n"
    "    background-color: #fff;\n"
    "    color: #495057;\n"
    "}\n"
    "\n"
    "QComboBox::drop-down {\n"
    "    subcontrol-origin: padding;\n"
    "    subcontrol-position: top right;\n"
    "    width: 25px; /* Увеличим ширину */\n"
    "    border-left-width: 1px;\n"
    "    border-left-color: #ced4da;\n"
    "    border-left-style: solid;\n"
    "    border-top-right-radius: 6px;\n"
    "    border-bottom-right-radius: 6px;\n"
    "}\n"
    "\n"
    "QComboBox::down-arrow {"
    "image: url(:/resources/arrow.png);"
    "height: 20px;"
    "width: 20px;"
    "}\n"
    "\n"
    "QComboBox:hover {\n"
    "    border-color: #495057;\n"
    "}\n"
    "\n"
    "QComboBox:focus {\n"
    "    border: 1px solid #80bdff; /* Синяя рамка при фокусе */\n"
    "    outline: none; /* Убираем обводку */\n"
    "}\n"
    "\n"
    "QComboBox QAbstractItemView {\n"
    "    border: 1px solid #ced4da;\n"
    "    border-radius: 4px;\n"
    "    background-color: #fff;\n"
    "    color: #495057;\n"
    "    outline: none;\n"
    "}\n"
)
COMBO_STYLE_LEFT = str(
    "QComboBox {\n"
    "    border: 1px solid #ced4da;\n"
    "    border-radius: 6px;\n"
    "    padding: 6px 12px; /* Увеличим внутренние отступы */\n"
    "    min-width: 20em;\n"
    "    background-color: #fff;\n"
    "    color: #495057;\n"
    "}\n"
    "\n"
    "QComboBox::drop-down {\n"
    "    subcontrol-origin: padding;\n"
    "    subcontrol-position: top right;\n"
    "    width: 25px; /* Увеличим ширину */\n"
    "    border-left-width: 1px;\n"
    "    border-left-color: #ced4da;\n"
    "    border-left-style: solid;\n"
    "    border-top-right-radius: 6px;\n"
    "    border-bottom-right-radius: 6px;\n"
    "}\n"
    "\n"
    "QComboBox::down-arrow {"
    "image: url(:/resources/arrow.png);"
    "height: 20px;"
    "width: 20px;"
    "}\n"
    "\n"
    "QComboBox:hover {\n"
    "    border-color: #495057;\n"
    "}\n"
    "\n"
    "QComboBox:focus {\n"
    "    border: 1px solid #80bdff; /* Синяя рамка при фокусе */\n"
    "    outline: none; /* Убираем обводку */\n"
    "}\n"
    "\n"
    "QComboBox QAbstractItemView {\n"
    "    border: 1px solid #ced4da;\n"
    "    border-radius: 4px;\n"
    "    background-color: #fff;\n"
    "    color: #495057;\n"
    "    outline: none;\n"
    "}\n"
)
LINE_EDIT_STYLE = str(
    "QLineEdit{\n"
    "    border-radius: 6px; /* Уменьшим скругление */\n"
    "    border: 1px solid #ced4da; /* Светло-серая рамка */\n"
    "    padding: 6px 12px; /* Увеличим внутренние отступы */\n"
    "    background-color: #fff; /* Белый фон */\n"
    "    color: #495057; /* Темнее цвет текста */\n"
    "    min-width: 4em;\n"
    "    max-width: 8em;\n"
    "}\n"
    "\n"
    "QLineEdit:focus {\n"
    "    border: 1px solid #80bdff; /* Синяя рамка при фокусе */\n"
    "    outline: none; /* Убираем обводку */\n"
    "}\n"
    "\n"
    "QLineEdit::placeholder {\n"
    "    color: #6c757d; /* Серый цвет для плейсхолдера */\n"
    "    font-style: italic;\n"
    "}\n"
    "\n"
    "QLineEdit:hover {\n"
    "    border-color: #495057;\n"
    "}"
)
MY_LINE_EDIT_STYLE = str(
    "QLineEdit{\n"
    "    border-radius: 6px; /* Уменьшим скругление */\n"
    "    border: 1px solid #ced4da; /* Светло-серая рамка */\n"
    "    padding: 3px 3px; /* Увеличим внутренние отступы */\n"
    "    background-color: #fff; /* Белый фон */\n"
    "    color: #495057; /* Темнее цвет текста */\n"
    "    min-width: 4em;\n"
    "}\n"
    "\n"
    "QLineEdit:focus {\n"
    "    border: 1px solid #80bdff; /* Синяя рамка при фокусе */\n"
    "    outline: none; /* Убираем обводку */\n"
    "}\n"
    "\n"
    "QLineEdit::placeholder {\n"
    "    color: #6c757d; /* Серый цвет для плейсхолдера */\n"
    "    font-style: italic;\n"
    "}\n"
    "\n"
    "QLineEdit:hover {\n"
    "    border-color: #495057;\n"
    "}"
)
PUSH_BUTTON_STYLE = str(
    "QPushButton {\n"
    "    font-weight: 500;\n"
    "    border-radius: 6px;\n"
    "    border: none; /* Убираем стандартную рамку */\n"
    "    padding: 8px 20px;\n"
    "    margin-top: 10px;\n"
    "    outline: none;\n"
    "    background-color: rgb(165, 165, 165); \n"
    "}\n"
    "\n"
    "QPushButton:hover {\n"
    "    background-color: rgb(236, 236, 236); \n"
    "}\n"
    "\n"
    "QPushButton:focus {\n"
    "    background-color:  rgb(236, 236, 236);\n"
    "    border: solid; /* Убираем рамку при фокусе*/\n"
    "}\n"
)
LABEL_STYLE = str(
    "QLabel {\n"
    "    color: black;\n"
    "    font-family: 'Segoe UI', sans-serif; \n"
    "    font-size: 14px;\n"
    "    font-weight: 400; /* Уменьшаем жирность */\n"
    "    background-color: transparent;\n"
    "    padding: 2px 0; /* Добавляем небольшой отступ */\n"
    "}\n"
    "\n"
    "QLabel#heading {\n"
    "    color: #212529; /* Еще темнее цвет для заголовка */\n"
    "    font-size: 20px; /* Чуть больше размер */\n"
    "    font-weight: 700; /* Жирный */\n"
    "    margin-bottom: 15px;\n"
    "}\n"
    "\n"
    "QLabel#subheading {\n"
    "    color: #343a40;\n"
    "    font-size: 14px;\n"
    "    font-weight: 400; /* Обычный вес */\n"
    "    margin-bottom: 10px;\n"
    "}\n"
    "\n"
)
STACK_WIDGET_STYLE = str(
"""
QStackedWidget {
    border: 1px solid #e0e4e7;
    border-radius: 8px;
    background-image: url(:/resources/background.jpg);
}
QStackedWidget > QWidget {
    background-color: transparent;
}
"""
)
STYLE_PROGRESS_BAR = str(
""" 
 QProgressBar {
     border: 2px solid grey;
     border-radius: 15px;
     text-align: top;
	 font-size: 18px;
	 padding: 4px;
 } 
QProgressBar::chunk {
     background-image:  url(:/resources/cat.png); 
	 width: 7px;
	 border-radius: 7px;   
     margin: 1px;
	 padding: 4px;
	 
 }
"""
)
WORK_SPACE_STYLE = str(
"""
QTreeWidget {
    border: 1px solid rgb(0, 0, 0);
    border-radius: 15px;
    background-color: white;
    }

QTreeWidget > QWidget {
    background-color: transparent;
}

QHeaderView::section {
    background-color: white; 
    color: black; 
    padding: 4px; 
    border-radius: 15px; 
}
QScrollBar:vertical {
    height: 0px; 
    background: transparent;
}

"""
)
ALTERNATIVE_LINES_STACK_STYLE = str(
"""
QTextEdit {
    border-radius: 6px; 
    border: 1px solid #ced4da; 
    padding: 6px 12px; 
    background-color: #fff; 
    min-width: 23em;
    max-width: 25em;
}

QTextEdit:hover {
    border-color: #495057;
}

QTextEdit:focus {
    border: 1px solid #80bdff; 
     outline: none; 
}

QLineEdit{
    border-radius: 6px; 
    border: 1px solid #ced4da; 
    padding: 6px 12px; 
    background-color: #fff; 
    color: #495057; 
    min-width: 23em;
    max-width: 25em;
}
QLineEdit:focus {
    border: 1px solid #80bdff; 
     outline: none; 
}

 QLineEdit::placeholder {
     color: #6c757d; 
     font-style: italic;
}

QLineEdit:hover {
    border-color: #495057;
}

QStackedWidget > QWidget {
        border: 1px solid rgb(0, 0, 0);
        border-radius: 15px;
        background-color: rgb(255, 255, 255)

}
QStackedWidget > QWidget {
    background-color: transparent;

}
"""
)
