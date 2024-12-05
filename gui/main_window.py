from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QComboBox, QTableWidget, QTableWidgetItem, QLineEdit
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Optimization Suite")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.combo_box = QComboBox()
        self.combo_box.addItem("Structure Of Fullerenes")
        self.combo_box.addItem("Portfolio Optimization")
        self.combo_box.addItem("Gradient Descent")
        self.combo_box.currentIndexChanged.connect(self.on_scenario_selected)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.combo_box)
        self.layout.addWidget(self.table_widget)
        
        self.text_box = QLineEdit()
        self.layout.addWidget(self.text_box)

    def on_scenario_selected(self):
        # Update view based on the selected scenario
        selected_scenario = self.combo_box.currentText()
        if selected_scenario == "Structure Of Fullerenes":
            pass
            # self.set_fullerenes_view()
        elif selected_scenario == "Portfolio Optimization":
            self.set_portfolio_view()
        elif selected_scenario == "Gradient Descent":
            self.set_gradient_descent_view()
            pass

    def set_portfolio_view(self):
        self.setWindowTitle("Portfolio Optimization")
        self.load_button = QPushButton("Load Data")
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)

    def set_gradient_descent_view(self):
        self.setWindowTitle("Gradient Descent")

        # create table for variables
        self.table_widget.clear()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Variable Name", "Value"])
        self.table_widget.setRowCount(3)

        self.load_button = QPushButton("Save variables")
        self.load_button.clicked.connect(self.save_variables)
        self.layout.addWidget(self.load_button)

    def save_variables(self):
        variables = {}
        try:
            for row in range(self.table_widget.rowCount()):
                var_name_item = self.table_widget.item(row, 0)
                var_value_item = self.table_widget.item(row, 1)

                if not var_name_item or not var_name_item.text():
                    break

                var_name = var_name_item.text()
                var_value = float(var_value_item.text()) if var_value_item else 0.0

                if var_name not in variables:
                    variables[var_name] = var_value
            
            self.text_box.setText(repr(variables))
        except Exception as e:
            print(f"Error saving variables: {e}")


    def load_data(self):
        try:
            data = pd.read_csv("asset_data.csv")
            self.table_widget.setRowCount(len(data))
            self.table_widget.setColumnCount(len(data.columns))
            self.table_widget.setHorizontalHeaderLabels(data.columns)

            for row in range(len(data)):
                for col in range(len(data.columns)):
                    item = QTableWidgetItem(str(data.iloc[row, col]))
                    self.table_widget.setItem(row, col, item)
        except Exception as e:
            print(f"Error loading data: {e}")

        # test code

    #     self.label = QLabel("Initial Text")
    #     self.button = QPushButton("Click Me")
    #     self.button.clicked.connect(self.on_button_click)

    #     self.layout.addWidget(self.label)
    #     self.layout.addWidget(self.button)

    # def on_button_click(self):
    #     self.label.setText("Clicked")
