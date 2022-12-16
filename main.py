import pymorphy2
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QWidget, QTableView, QApplication

global vvod
global sv
vvod = 'abc'
sv = ''


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(250, 250, 850, 700)
        self.setWindowTitle('Статистический анализ текста')
        self.ii = 0
        self.second_form = SecondForm(self, "Результаты анализа")
        self.second_form.setUpdatesEnabled(True)
        self.second_form.hide()
        self.sql_form = Example1()
        self.sql_form.setUpdatesEnabled(True)
        self.sql_form.show()

        self.win = QPlainTextEdit(self)
        self.win.move(20, 20)
        self.win.resize(500, 600)
        self.win.setEnabled(True)

        self.btn = QPushButton('Начать анализ', self)
        self.btn.resize(150, 30)
        self.btn.move(520, 60)
        self.btn.clicked.connect(self.open_second_form)

        self.btn2 = QPushButton('Обновить текст', self)
        self.btn2.resize(150, 30)
        self.btn2.move(520, 25)
        self.btn2.clicked.connect(self.run)

        self.btn3 = QPushButton('Открыть файл', self)
        self.btn3.resize(150, 30)
        self.btn3.move(520, 95)
        self.btn3.clicked.connect(self.open)

    def open(self):
        global vvod
        if os.path.exists(self.win.toPlainText()):
            f = open(self.win.toPlainText(), mode="rt", encoding='utf8')
            s = f.readlines()
            if s:
                self.win.setPlainText('\n'.join(s))
            f.close()
        else:
            self.win.setPlainText("Такого файла не существует")

    def open_second_form(self):
        if self.second_form.isHidden() and self.ii == 0:
            self.second_form.show()
        else:
            self.second_form.hide()

    def run(self):
        self.ii = 0
        try:
            global sv
            global vvod
            vvod = self.win.toPlainText()
            ss = []
            ss.append(len_and_lenw(vvod))
            ss.append(volums(vvod))
            sv = []
            for i in ss:
                if type(i) == list:
                    for y in i:
                        sv.append(str(y))
                else:
                    sv.append(str(i))
            sv = '\n'.join(sv)
        except Exception:
            self.win.setPlainText('Неверный формат')
            self.ii = 1
        if self.ii == 0:
            self.second_form.update()


class SecondForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        global sv
        global vvod
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Результаты анализа')
        self.res = QPlainTextEdit(self)
        self.res.resize(300, 300)
        self.res.move(20, 20)
        self.res.setEnabled(False)
        if vvod == 'abc':
            self.res.setPlainText('Нажмите кнопку "Обновить текст" перед началом анализа')

    def update(self):
        self.res.setPlainText(sv)


def len_and_lenw(n):  # n - str
    vv = []
    morph = pymorphy2.MorphAnalyzer()
    s = []
    ss = strip_punctuation_ru(n.lower())
    a = len(ss.split())
    for i in ss.split():
        if [i, ss.count(i)] not in s:
            s.append([i, ss.count(i)])
    s = sorted(s, key=lambda x: (int(x[1]), x[0]), reverse=True)
    vv.append(f'Общее количество слов: {a}')  # 1 общ колво слов
    vv.append(f'Словарный запас текста: {len(s)}')  # 2 слов запас текста
    svv = []
    svv2 = [morph.parse(i)[0].normal_form for i in ss.split()]
    for i in svv2:
        if [i, svv2.count(i)] not in svv:
            svv.append([i, svv2.count(i)])
    svv = sorted(svv, key=lambda x: (int(x[1]), x[0]), reverse=True)
    vv.append(f'Словарный запас текста(инф): {len(svv)}')
    vv.append(f'Топ-5 самых употребляемых слов:')
    # топ 5 самых употребляемых слов
    cou = 0
    sss = []
    while cou < 5:
        if len(svv) > 5:
            sss.append(svv[cou][0])
            cou += 1
        else:
            sss.append(svv[cou][0])
            cou += 1
    sss = ', '.join(sss)
    vv.append(sss)  # топ 5 в той же форме
    return vv


# - пунктуация
def strip_punctuation_ru(data):
    fl = 0
    s = '''«»~!?@#$%^&*_-()[]{}:;'"/\<>.,—|'''
    s0 = ' - '
    ss = ''
    for i in data:
        if i not in s:
            ss += i
        else:
            fl += 1
            ss += ' '
    if s0 in ss:
        ss = ss.replace(s0, ' ')
    if '–' in ss:
        ss = ss.replace('–', '')
    if fl != len(data):
        ss = ss.split()
        return ' '.join(ss)
    else:
        return ''


def volums(n):
    vv = []
    s = []
    ss = strip_punctuation_ru(n)
    v = 'уеэоаыяиюё'
    ss.replace('ё', 'е')
    for i in ss:
        if i in v:
            s.append([i, ss.count(i)])
    s = sorted(s, key=lambda x: (int(x[1]), x[0]), reverse=True)
    vv.append(f'Самая часто употрбляемая гласная - {s[0][0]} ({s[0][1]} р)')
    fl = 0
    fl1 = 0
    fl2 = 0
    fl3 = 0
    fl4 = 0
    aa = 0
    oo = 0
    for i in s:
        if i[0] == 'а' and fl == 0:
            vv.append(f'Гласная а встречается {i[1]} р')
            aa = int(i[1])
            fl = 1
        if i[0] == 'о' and fl1 == 0:
            vv.append(f'Гласная о встречается {i[1]} р')
            oo = int(i[1])
            fl1 = 1
        if i[0] == 'и' and fl2 == 0:
            vv.append(f'Гласная и встречается {i[1]} р')
            fl2 = 1
        if i[0] == 'е' and fl3 == 0:
            vv.append(f'Гласная е встречается {i[1]} р')
            fl3 = 1
        if i[0] == 'я' and fl4 == 0:
            vv.append(f'Гласная я встречается {i[1]} р')
            fl4 = 1
    if aa > oo:
        vv.append('Акает, поэтому с некоторой вероятностью автор из Южных регионов России')
    elif oo > aa:
        vv.append('Окает, поэтому с некоторой вероятностью автор из Северных регионов России')
    else:
        vv.append('И Акает и Окает, поэтому с некоторой вероятностью автор из России')
    return vv


class Example1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('statistic.db')
        db.open()

        view = QTableView(self)
        model = QSqlTableModel(self, db)
        model.setTable('analyz')
        model.select()

        view.setModel(model)
        view.move(10, 10)
        view.resize(900, 550)

        self.setGeometry(200, 100, 1000, 600)
        self.setWindowTitle('База готовых анализов')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
