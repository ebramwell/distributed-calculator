import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
import requests
from calcconfig import CalcConfig 

class Calculator(QWidget):
    def __init__(self):
        """
        Constructor for the Calculator class.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the main layout
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # Create a display widget
        self.display = QLineEdit()
        self.display.setStyleSheet('font-size: 20px; height: 50px;')
        vbox.addWidget(self.display)

        # Create a grid layout for the buttons
        grid = QGridLayout()
        vbox.addLayout(grid)

        # Button labels
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', 'M+', 'M-', 'MR', 
            'MC'
        ]

        # Add buttons to the grid layout
        row, col = 0, 0
        for button in buttons:
            btn = QPushButton(button)
            btn.setStyleSheet('font-size: 20px; width: 50px; height: 50px;')
            btn.clicked.connect(self.on_click)
            grid.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Set window properties
        self.setWindowTitle("Peanut's Stupid Calculator")
        self.setGeometry(300, 300, 300, 400)
        self.show()

    # Shows the result
    def on_click(self):
        """
        This function is called when a button is clicked.
        """
        character_pressed = self.sender().text()
        config = CalcConfig()
       
        if character_pressed == '=':
            try:
                #result = str(eval(self.display.text()))
                response = requests.get(f'{config.api_host}/eval', params={'exp': self.display.text()})
                
                if response.status_code == 200:
                    result = response.json()['result']
                else:
                    result = 'Something in there'
                
                self.display.setText(str(result))
            except Exception as e:
                self.display.setText(str(e))
        elif character_pressed == 'C':
            self.display.clear()
        elif character_pressed == 'M+':
            try:
                #result = str(eval(self.display.text()))
                response = requests.get(f'{config.api_host}/ma', params={'value': self.display.text()})

            except Exception as e:
                self.display.setText(str(e))
        elif character_pressed == 'MR':
            try:
                #result = str(eval(self.display.text()))
                response = requests.get(f'{config.api_host}/mr')
                
                if response.status_code == 200:
                    result = response.json()['result']
                else:
                    result = 'Something in there'
                
                self.display.setText(str(result))
            except Exception as e:
                self.display.setText(str(e))
        elif character_pressed == 'M-':
            try:
                #result = str(eval(self.display.text()))
                response = requests.get(f'{config.api_host}/mm', params={'value': self.display.text()})
                self.display.setText(str(result))
            except Exception as e:
                self.display.setText(str(e))

        elif character_pressed == 'MC':
            try:
                #result = str(eval(self.display.text()))
                response = requests.get(f'{config.api_host}/mc')
                
                if response.status_code == 200:
                    result = response.json()['result']
                else:
                    result = 'Something in there'
                
            except Exception as e:
                self.display.setText(str(e))
        else:
            self.display.setText(self.display.text() + character_pressed)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()

    sys.exit(app.exec_())