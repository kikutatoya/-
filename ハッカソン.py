from PySide6 import QtCore, QtWidgets, QtGui
import sys
from itertools import combinations

from qt_material import apply_stylesheet

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # self.icon = QtGui.QIcon(umn_config.PATH_ICON)
        # self.setWindowIcon(self.icon)
        self.setWindowTitle("割り勘計算")
        self.setFixedSize(400,500)
        self.init_ui()

    def init_ui(self):
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.main_layout =  QtWidgets.QVBoxLayout(self.widget)  # 全体のレイアウト

        self.input_layout = QtWidgets.QHBoxLayout()

        self.scroll_area = QtWidgets.QScrollArea(self)  # スクロールエリアを作成
        self.scroll_widget = QtWidgets.QWidget()  # スクロール内に配置するウィジェット
        self.grid_layout = QtWidgets.QGridLayout(self.scroll_widget)
        self.lines = []
        number_label = QtWidgets.QLabel("番号")
        radio_label = QtWidgets.QLabel("幹事")
        rate_label = QtWidgets.QLabel("負担率")
        radio_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        rate_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        n_init_line = 5

        self.grid_layout.addWidget(number_label, 0, 0) 
        self.grid_layout.addWidget(radio_label, 0, 1) 
        self.grid_layout.addWidget(rate_label, 0, 2) 
        
        self.scroll_area.setWidgetResizable(True)  # サイズ変更可能に
        self.scroll_area.setWidget(self.scroll_widget)  # スクロール内のウィジェットを設定
        
        for i in range(n_init_line):
            number_label = QtWidgets.QLabel(str(i))
            number_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            radio_button = QtWidgets.QRadioButton()
            rate_input = QtWidgets.QLineEdit()
            if i < 3:
                rate_input.setText("1")
            self.lines.append([number_label, radio_button, rate_input])
            self.grid_layout.addWidget(number_label, i+1, 0) 
            self.grid_layout.addWidget(radio_button, i+1, 1) 
            self.grid_layout.addWidget(rate_input, i+1, 2) 
        
        # 0番目のラジオボタンにチェックを入れる
        # self.lines[0][1].setChecked(True)

        # 行を追加するためのボタン
        self.add_line_button = self.new_add_line_button(self.add_line)
        self.grid_layout.addWidget(self.add_line_button, n_init_line, 5)

        # 負担額
        n_min_amount_line = 1
        self.amount_scroll_area = QtWidgets.QScrollArea(self)  # スクロールエリアを作成
        self.amount_scroll_widget = QtWidgets.QWidget()  # スクロール内に配置するウィジェット
        self.amount_grid_layout = QtWidgets.QGridLayout(self.amount_scroll_widget)
        self.amount_lines = []
        self.amount_label =  QtWidgets.QLabel("支払い")
        self.amount_human_label =  QtWidgets.QLabel("番号")
        self.amount_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.amount_human_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.amount_grid_layout.addWidget(self.amount_human_label, 0, 1)
        self.amount_grid_layout.addWidget(self.amount_label, 0, 2)
        for i in range(n_min_amount_line):
            amount_combobox = QtWidgets.QComboBox()
            amount_input =  QtWidgets.QLineEdit()
            amount_combobox.addItems([str(item) for item in range(len(self.lines)) ])
            self.amount_lines.append([amount_combobox, amount_input])
            self.amount_grid_layout.addWidget(amount_combobox, i+1, 1)
            self.amount_grid_layout.addWidget(amount_input, i+1, 2)
        self.amount_scroll_area.setWidgetResizable(True)
        self.amount_scroll_area.setWidget(self.amount_scroll_widget)
        self.add_amount_line_button = self.new_add_line_button(self.add_amount_line)
        self.amount_grid_layout.addWidget(self.add_amount_line_button, n_min_amount_line, 3)
        amount_spacer_index = len(self.amount_lines) + 1  # +1 は追加ボタンの行、+1 はスペーサーのため
        self.add_spacer_to_layout(self.amount_grid_layout, amount_spacer_index)

        
        self.input_layout.addWidget(self.scroll_area)
        self.input_layout.addWidget(self.amount_scroll_area)

        self.minimum_unit_layout = QtWidgets.QHBoxLayout()
        self.minimum_unit_label = QtWidgets.QLabel("最小単位")
        self.minimum_unit_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        # self.minimum_unit_input = QtWidgets.QLineEdit()
        self.minimum_unit_combobox = QtWidgets.QComboBox()
        self.minimum_unit_combobox.addItems(["1", "5", "10", "50", "100", "500", "1000"])
        self.minimum_unit_combobox.setFixedSize(60, 25)
        self.minimum_unit_layout.addWidget(self.minimum_unit_label)
        # self.minimum_unit_layout.addWidget(self.minimum_unit_input)
        self.minimum_unit_layout.addWidget(self.minimum_unit_combobox)      
        
        self.calc_button = QtWidgets.QPushButton("計算")
        self.calc_button.clicked.connect(self.calc)
        self.calc_button.setFixedSize(100, 30) 
        self.calc_button_layout = QtWidgets.QHBoxLayout()
        self.calc_button_layout.addWidget(QtWidgets.QLabel("sss"))
        self.calc_button_layout.addWidget(self.calc_button)
        self.calc_button_layout.addStretch()

        self.result_label = QtWidgets.QLabel("清算結果")
        self.result_textbox = QtWidgets.QTextEdit()

        # self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.minimum_unit_layout)
        self.main_layout.addWidget(self.calc_button)
        self.main_layout.addWidget(self.result_label)
        self.main_layout.addWidget(self.result_textbox)
        
        self.setLayout(self.main_layout)

    def scroll_to_bottom(self, scroll_area):
        # 遅延を入れる
        # スクロールバーの最大値が再計算された後に、一番下までスクロールさせる
        QtCore.QTimer.singleShot(10, lambda: scroll_area.verticalScrollBar().setValue(scroll_area.verticalScrollBar().maximum()))

    def add_line(self):
        n_row = len(self.lines)
        number_label = QtWidgets.QLabel(str(n_row))
        number_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        radio_button = QtWidgets.QRadioButton()
        rate_input = QtWidgets.QLineEdit()
        
        self.grid_layout.addWidget(number_label, n_row + 1, 0)
        self.grid_layout.addWidget(radio_button, n_row + 1, 1)
        self.grid_layout.addWidget(rate_input, n_row + 1, 2)
        self.lines.append([number_label, radio_button, rate_input])

        self.add_line_button.hide()
        self.add_line_button = self.new_add_line_button(self.add_line)
        self.grid_layout.addWidget(self.add_line_button, n_row + 1, 3)
        self.add_line_button.setFocus()

        for line in self.amount_lines:
            amount_combobox, amount_input = line
            amount_combobox.addItem(str(n_row))

        self.scroll_to_bottom(self.scroll_area)
        self.adjustSize()
    
    def add_amount_line(self):
        n_amount_row = len(self.amount_lines)
        amount_combobox = QtWidgets.QComboBox()
        amount_combobox.addItems([str(item) for item in range(len(self.lines)) ])
        amount_input =  QtWidgets.QLineEdit()
        self.amount_lines.append([amount_combobox, amount_input])
        self.amount_grid_layout.addWidget(amount_combobox, n_amount_row+1, 1)
        self.amount_grid_layout.addWidget(amount_input, n_amount_row+1, 2)
        self.amount_scroll_area.setWidgetResizable(True)
        self.amount_scroll_area.setWidget(self.amount_scroll_widget)
        self.add_amount_line_button.hide()
        self.add_amount_line_button = self.new_add_line_button(self.add_amount_line)
        self.amount_grid_layout.addWidget(self.add_amount_line_button, n_amount_row+1, 3)
        self.add_amount_line_button.setFocus()
        # 新しいスペーサーを追加する前に古いスペーサーを削除
        if hasattr(self, 'vertical_spacer'):
            self.amount_grid_layout.removeItem(self.vertical_spacer)

        # 新しいスペーサーの行インデックスを更新
        amount_spacer_index = len(self.amount_lines) + 2  # 新しい行数に基づいて更新
        self.add_spacer_to_layout(self.amount_grid_layout, amount_spacer_index)

        self.adjustSize()
        self.scroll_to_bottom(self.amount_scroll_area)
    
    def new_add_line_button(self, func):
        button = QtWidgets.QPushButton("+")
        button.clicked.connect(func)
        button.setFixedSize(25, 25)
        return button

    def add_spacer_to_layout(self, layout, row):
        # スペーサーを作成してレイアウトに追加
        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addItem(spacer, row, 0, 1, layout.columnCount())
        self.vertical_spacer = spacer  # スペーサーを参照として保持

    def calc(self):
        money = []
        grade = []
        kannji = None
        for index, line in enumerate(self.lines):
            _, radio_button, rate_input = line
            if rate_input.text() == "":
                break
            money.append(0)
            if not rate_input.text().isdecimal():
                self.result_textbox.setText("エラー: \n負担率には、割合を入力してください")
                return
            grade.append(float(rate_input.text()))
            if radio_button.isChecked():
                kannji = index
        
        for line in self.amount_lines:
            amount_combobox, amount_input = line
            if amount_input.text() == "":
                break
            money[int(amount_combobox.currentText())] += int(amount_input.text())

        minimum_unit = int(self.minimum_unit_combobox.currentText())

        n = len(money)

        if kannji is None:
            output = warikan_no_kannji(n, money, grade, minimum_unit)
        else :
            output = warikann(n,money,grade,minimum_unit,kannji)

        if output == "":
            output = "やり取りなし\n"

        self.result_textbox.setText(output)

        # if selected_index is not None:
        #     print(f"選択されたラジオボタン: {selected_index}")
        #     self.result_textbox.setText(f"{selected_index}番のラジオボタンが選択されています。"
# else:
        #     print("選択されたラジオボタンはありません。")
        #     self.result_textbox.setText("選択されたラジオボタンはありません。")
def warikan_no_kannji(n, money, grade, min_):
    def sagaku(m,M):
        L=[]
        for i in range(len(m)):
            l=m[i]-M[i]
            L.append(l)
        return L

    def groupindex(nums):
        index = list(range(len(nums)))

        indexset = []
        while index:
            flg = False
            for i in range(len(index)):
                for selection in combinations(index, i + 1):
                    if sum([nums[j] for j in selection]) == 0:
                        index = [j for j in index if j not in selection]
                        indexset.append(selection)
                        flg = True
                    
                    if flg: break
                if flg: break

        return indexset


    def yaritori(index, nums, min_):
        output = ""
        for l in index:
            if len(l)==1:
                continue
            else:
                for i in range(1,len(l)):
                    s, t = l[0], l[i]
                    ans=round(nums[t]/min_)*min_
                    if ans<0:
                        output += f"{s}が{t}に{abs(ans)}円払う\n"
                    elif ans>0:
                        output += f"{s}が{t}から{abs(ans)}円もらう\n"
                    else:
                        continue
        return output

    total=0
    G=0
    for m in money:
        total+=m
    for g in grade:
        G+=g
    L=[]
    for i in range(n):
        l=total*grade[i]/G
        L.append(l)
    
    # money = [600, 380, 500, 120, 85, 70, 145, 100]
    # L = [500, 500, 500, 100, 100, 100, 100, 100]
    _sagaku = sagaku(L, money)
    index = groupindex(_sagaku)

    output = yaritori(index, _sagaku, min_)
    return output    

def warikann(n,money,grade,min,kannji):
    total=0
    G=0
    for m in money:
        total+=m
    for g in grade:
        G+=g
    L=[]
    for i in range(n):
        l=total*grade[i]/G
        L.append(l)
    
    output = ""
    for i in range(n):
        if i==kannji:
            continue
        else:
            ans=round((money[i]-L[i])/min)*min
            if ans<0:
                output += f"{i} が幹事に {abs(ans)} 円払う\n"
            elif ans>0:
                output += f"{i} が幹事から {abs(ans)} 円もらう\n"
            else:
                continue
    
    return output


def main():
    app = QtWidgets.QApplication([])
    # setup stylesheet
    # apply_stylesheet(app, theme='dark_teal.xml')
    main_window = MainWindow()
    main_window.show()
    app.exec()

if __name__ == "__main__":
    main()