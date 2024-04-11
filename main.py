import sys
from random import shuffle
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QRadioButton
from PyQt5.uic import loadUi


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = loadUi('1.ui', self)
        self.ui.nextButton.clicked.connect(self.next)

    def next(self):
        for radio in self.groupBox.findChildren(QRadioButton):
            if radio.isChecked():
                self.theme = radio.text()

        for radio in self.groupBox_2.findChildren(QRadioButton):
            if radio.isChecked():
                self.mode = radio.text()


        self.fill_dict()
        if (self.mode == 'Тренировка'):
            self.train()
        else:
            self.test()

    def train(self):
        self.ui = loadUi('2.ui', self)
        self.ui.backButton.clicked.connect(self.back)
        self.ui.leftButton.clicked.connect(self.left)
        self.ui.rightButton.clicked.connect(self.right)

        self.n = 1
        self.words = list(self.dict_ru.keys())
        self.ui.num_label.setText(str(self.n) + '/' + str(len(self.words)))
        self.ui.ru.setText(self.words[self.n - 1])
        self.ui.en.setText(self.dict_ru[self.words[self.n - 1]])

    def test(self):
        self.ui = loadUi('3.ui', self)
        self.ui.backButton.clicked.connect(self.back)
        self.ui.nextTaskButton.clicked.connect(self.next_task)
        self.ui.hintButton.clicked.connect(self.hint)

        task_part_1 = list(self.dict_ru.keys())
        shuffle(task_part_1)
        task_part_2 = list(self.dict_en.keys())
        shuffle(task_part_2)
        self.tasks = task_part_1[:5] + task_part_2[:5]
        self.n = 0
        self.ui.task_label.setText(self.tasks[self.n])
        self.good = 0
        self.bad = 0

    def hint(self):
        if 0 <= self.n <= 4: # русское слово (проверяем в dict_ru)
            answer = self.dict_ru[self.tasks[self.n]]
        elif 5 <= self.n <= 9: # английское слово (проверяем в dict_en)
            answer = self.dict_en[self.tasks[self.n]]

        self.ui.hint_label.setText(answer)

    def next_task(self):
        self.ui.hint_label.setText('')
        if 0 <= self.n <= 4: # русское слово (проверяем в dict_ru)
            answer = self.dict_ru[self.tasks[self.n]]
        elif 5 <= self.n <= 9: # английское слово (проверяем в dict_en)
            answer = self.dict_en[self.tasks[self.n]]

        if self.ui.lineEdit.text().lower() == answer.lower():  # сравниваем без учета регистра
            self.good += 1
            q = QSound.play('good.wav')
            self.ui.good_label.setText(str(self.good))
        else:
            self.bad += 1
            q = QSound.play('bad.wav')
            self.ui.bad_label.setText(str(self.bad))

        self.n += 1
        if self.n <= 9:
            self.ui.task_label.setText(self.tasks[self.n])
        else:
            self.ui.task_label.setText('Вы прошли тест!')
            self.ui.nextTaskButton.setEnabled(False)
            self.ui.lineEdit.setEnabled(False)
        self.ui.lineEdit.setText('')





    def fill_dict(self):
        self.dict_ru = {}
        self.dict_en = {}
        if self.theme == 'Животные':
            f = open('animals.txt', 'r')
        elif self.theme == 'Еда':
            f = open('food.txt', 'r')
        elif self.theme == 'Мебель':
            f = open('furniture.txt', 'r')
        for line in f:
            line = line.split(':')
            self.dict_ru[line[0].strip()] = line[1].strip()
            self.dict_en[line[1].strip()] = line[0].strip()
        f.close()

    def back(self):
        self.ui = loadUi('1.ui', self)
        self.ui.nextButton.clicked.connect(self.next)

    def left(self):
        if self.n > 1:
            self.n -= 1
            self.ui.num_label.setText(str(self.n) + '/' + str(len(self.words)))
            self.ui.ru.setText(self.words[self.n - 1])
            self.ui.en.setText(self.dict_ru[self.words[self.n - 1]])


    def right(self):
        if self.n < len(self.words):
            self.n += 1
            self.ui.num_label.setText(str(self.n) + '/' + str(len(self.words)))
            self.ui.ru.setText(self.words[self.n - 1])
            self.ui.en.setText(self.dict_ru[self.words[self.n - 1]])






app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
