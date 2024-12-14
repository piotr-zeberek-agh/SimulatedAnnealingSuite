from scenario import Scenario
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QDialogButtonBox, QDialog, QTableWidgetItem, QListWidget, QFrame, QLabel, QLineEdit, QTableWidget, QPushButton, QHBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtGui import QFont

class PortfolioOptimizationScenario(Scenario):
    def __init__(self, layout):
        super().__init__(layout)
        
        self.adjust_layout()

        # self.my_run_button.clicked.connect(lambda: self.run(portfolio_table, chart_widget))
        # self.select_assets_button.clicked.connect(self.open_asset_selection_dialog)


    def adjust_layout(self):
        """Adjusts the layout to include elements for portfolio optimization."""

        title_font = QFont("Arial", 16, QFont.Weight.Bold)

        # its because self.layout is a QVBoxLayout
        self.main_window = QHBoxLayout()

        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(10)

        # self.portfolio_table = QTableWidget()
        # self.portfolio_table.setRowCount(5)
        # self.portfolio_table.setColumnCount(3)
        # self.portfolio_table.setHorizontalHeaderLabels(["Asset Name", "Expected Return", "Risk Level"])
        # self.left_layout.addWidget(self.portfolio_table)

        self.row_1 = QHBoxLayout()
        # self.row_1.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.load_data_button = QPushButton()
        self.load_data_button.setText("Load Data")
        self.download_data_button = QPushButton()
        self.download_data_button.setText("Download Data")
        self.row_1.addWidget(self.load_data_button)
        self.row_1.addWidget(self.download_data_button)
        self.left_layout.addLayout(self.row_1)

        self.row_2 = QHBoxLayout()

        self.reset_data_button = QPushButton()
        self.reset_data_button.setText("Reset Data")
        self.save_result_button = QPushButton()
        self.save_result_button.setText("Save Result")
        self.row_2.addWidget(self.reset_data_button)
        self.row_2.addWidget(self.save_result_button)
        self.left_layout.addLayout(self.row_2)

        self.row_3 = QHBoxLayout()

        self.interval_label = QLabel("Enter the interval for the data")
        self.interval_label.setFont(title_font)
        self.row_3.addWidget(self.interval_label)
        self.left_layout.addLayout(self.row_3)

        self.row_4 = QHBoxLayout()

        self.start_date_line = QLineEdit()
        self.start_date_line.setPlaceholderText("Start (YYYY-MM-DD)")
        self.row_4.addWidget(self.start_date_line)

        self.end_date_line = QLineEdit()
        self.end_date_line.setPlaceholderText("End (YYYY-MM-DD)")
        self.row_4.addWidget(self.end_date_line)
        self.left_layout.addLayout(self.row_4)

        self.row_5 = QHBoxLayout()

        self.interval_label = QLabel("")
        self.row_5.addWidget(self.interval_label)
        self.left_layout.addLayout(self.row_5)




        # self.parameters_label = QLabel("Portfolio Parameters")
        # self.parameters_label.setFont(title_font)
        # self.row_5.addWidget(self.parameters_label)
        # self.left_layout.addLayout(self.row_5)

        # self.input_table_1 = QTableWidget()
        # self.input_table_1.setRowCount(2)
        # self.input_table_1.setColumnCount(2)
        # self.input_table_1.setHorizontalHeaderLabels(["Asset Name", "Expected Return"])
        # self.left_layout.addWidget(self.input_table_1)

        # self.parameters_label = QLabel("Algorithm Parameters")
        # self.parameters_label.setFont(title_font)
        # self.row_5.addWidget(self.parameters_label)
        # self.left_layout.addLayout(self.row_5)

        # self.row_6 = QHBoxLayout()
        # self.input_table_2 = QTableWidget()
        # self.input_table_2.setRowCount(6)
        # self.input_table_2.setColumnCount(2)
        # self.input_table_2.setVerticalHeaderLabels(["Name", "input Value"])
        # self.input_table_2.setVerticalHeaderLabels(["Initial Temperature", "Cooling Rate", "Number of Iterations", "Stop Temperature", "Perturbation Function", "Acceptance Criterion"])
        # self.row_6.addWidget(self.input_table_2)
        # self.left_layout.addLayout(self.row_6)







        # self.row_6 = QHBoxLayout()

        # self.select_assets_button = QPushButton("Select Assets")
        # self.row_6.addWidget(self.select_assets_button)


        # # Inicjalizacja listy aktywów
        # self.asset_list = QListWidget(self)
        # self.asset_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        # self.assets = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "SPY", "BABA"]
        # self.asset_list.addItems(self.assets)

        # # Podpięcie przycisku do otwierania okna wyboru aktywów
        # self.select_assets_button.clicked.connect(self.open_asset_selection_dialog)

        # self.left_layout.addLayout(self.row_6)

        self.row_7 = QHBoxLayout()

        self.budget_label = QLabel("Enter your budget")
        self.row_7.addWidget(self.budget_label)
        self.budget_line = QLineEdit()
        self.budget_line.setPlaceholderText("")
        self.row_7.addWidget(self.budget_line)
        self.left_layout.addLayout(self.row_7)


        label = QLabel("Select assets:")
        self.left_layout.addWidget(label)

        self.add_button = QPushButton("Add Selected Assets")
        self.add_button.clicked.connect(self.add_selected_assets)
        self.left_layout.addWidget(self.add_button)

        self.selected_assets_list = QListWidget()  # Tworzymy listę do przechowywania wybranych aktywów
        self.selected_assets_list.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        self.left_layout.addWidget(self.selected_assets_list)


        # Button "Run"
        self.my_run_button = QPushButton()
        self.my_run_button.setText("Run")
        self.left_layout.addWidget(self.my_run_button)
        self.my_run_button.clicked.connect(self.run)

        # Middle line

        self.mid_layout = QVBoxLayout()
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.mid_layout.addWidget(line)

        # Right layout

        self.right_layout = QVBoxLayout()
        self.chart_widget = PortfolioChartWidget()

        self.right_layout.addWidget(self.chart_widget)

        self.assets_label = QLabel("Assets Values")
        self.assets_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.assets_label.setFixedWidth(250)
        self.assets_label.setFont(title_font)
        self.right_layout.addWidget(self.assets_label)

        self.portfolio_table = QTableWidget()
        self.portfolio_table.setRowCount(5)
        self.portfolio_table.setColumnCount(3)
        self.portfolio_table.setHorizontalHeaderLabels(["Asset Name", "Expected Return", "Risk Level"])
        self.right_layout.addWidget(self.portfolio_table)

        self.main_window.addLayout(self.left_layout)
        self.main_window.addLayout(self.mid_layout)
        self.main_window.addLayout(self.right_layout)
        self.layout.addLayout(self.main_window)


        # Sekcja ograniczeń portfela:
        # Tolerancja ryzyka, minimalny/oczekiwany zwrot, maksymalny drawdown, liczba aktywów, budżet.

        



    # def select_assets_layout(self):
    #     """Adjusts the layout to include elements for selecting assets."""
    #     self.clear_layout()
    #     self.asset_list = QListWidget()
    #     self.asset_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

    #     # Lista dostępnych akcji (tickers)
    #     self.assets = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "SPY", "BABA"]
    #     self.asset_list.addItems(self.assets)  # Dodajemy tickery do listy

    #     # Tworzymy przycisk "Run"
    #     self.run_button = QPushButton("Run")
    #     self.run_button.clicked.connect(self.run)

    #     # Tworzymy layout i dodajemy widgety
    #     layout = QVBoxLayout()
    #     layout.addWidget(self.label)
    #     layout.addWidget(self.asset_list)
    #     layout.addWidget(self.run_button)

    #     self.setLayout(layout)


    # def open_asset_selection_dialog(self):
    #     # Otworzenie okna dialogowego do wyboru aktywów
    #     dialog = AssetSelectionDialog(self)
    #     dialog.exec()  # Uruchomienie dialogu

    # def add_selected_assets(self):
    #     # Pobranie zaznaczonych aktywów
    #     selected_items = self.asset_list.selectedItems()
    #     selected_assets = [item.text() for item in selected_items]
    #     print(f"Selected Assets: {selected_assets}")




    def run(self, portfolio_table, chart_widget):
        """Simulates portfolio optimization and updates the chart."""
        self.start_date = self.end_date_line.text()
        self.end_date = self.end_date_line.text()
        self.budget = self.budget_line.text()
        # Sekcja wag kryteriów (jeśli wielokryterialna optymalizacja):
        # Wagi dla ryzyka, zwrotu, drawdown itp.



    def add_selected_assets(self):
        """Add selected assets to the selected assets list."""
        self.selected_items = self.asset_list.selectedItems()

        for item in self.selected_items:
            self.selected_assets_list.addItem(item.text())

        self.asset_list.clearSelection()


class AssetSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Tytuł dialogu
        self.setWindowTitle("Select Assets")

        # Lista aktywów
        self.asset_list = QListWidget(self)
        self.asset_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        assets = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "SPY", "BABA"]
        self.asset_list.addItems(assets)

        # Ustawienia przycisków dialogowych
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Layout dla listy i przycisków
        dialog_layout = QVBoxLayout(self)
        dialog_layout.addWidget(self.asset_list)
        dialog_layout.addWidget(self.button_box)

        self.setLayout(dialog_layout)

    def get_selected_assets(self):
        # Zwracamy listę wybranych elementów
        selected_assets = [item.text() for item in self.asset_list.selectedItems()]
        return selected_assets
    

# zakladki do zmiany wykresu w polu wykresu
class PortfolioChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_chart(self, data):
        """Update the pie chart with new data."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
        ax.set_title("Portfolio Distribution")
        self.canvas.draw()


# # ---------------------- Data ------------------

    def download_data(self):
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "SPY", "BABA"]
        self.start_date = "2022-01-01"
        self.end_date = "2024-10-31"
        self.data = yf.download(self.tickers, start=self.start_date, end=self.end_date)['Adj Close']
        if self.data is not None:
            self.isDataLoaded = True
        else:
            print("Cannot download data!")

    def save_csv(self, data, file_name: str):
        data.to_csv(file_name)
        print(f"Data saved in {file_name}")

    def load_csv(self, window, file_name: str):
        try:
            self.data = pd.read_csv(file_name)
            if self.data is not None:
                self.isDataLoaded = True
            else:
                print("Cannot load data!")
            window.table_widget.setRowCount(len(self.data))
            window.table_widget.setColumnCount(len(self.data.columns))
            window.table_widget.setHorizontalHeaderLabels(self.data.columns)

            for row in range(len(self.data)):
                for col in range(len(self.data.columns)):
                    item = QTableWidgetItem(str(self.data.iloc[row, col]))
                    window.table_widget.setItem(row, col, item)
        except Exception as e:
            print(f"Error loading data: {e}")
