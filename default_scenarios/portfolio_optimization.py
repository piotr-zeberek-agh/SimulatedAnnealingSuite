from scenario import Scenario
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QVBoxLayout, QDialog, QMessageBox, QListWidget, QLabel, QDialogButtonBox, QListWidgetItem, QTableWidgetItem, QAbstractItemView, QFrame, QLineEdit, QTableWidget, QPushButton, QHBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import json
from portfolio_data import fetch_data
from annealing import accept_move
import numpy as np
import pandas as pd
import random
import re

class PortfolioOptimizationScenario(Scenario):
    def __init__(self, layout):
        super().__init__(layout)
        # self.is_data = False
        self.selected_options = None
        self.data = None

        self.adjust_layout()

    def adjust_layout(self):
        """Adjusts the layout to include elements for portfolio optimization."""

        title_font = QFont("Arial", 16, QFont.Weight.Bold)

        # its because self.layout is a QVBoxLayout
        self.main_window = QHBoxLayout()

        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(10)

        # self.interval_label.setFont(title_font)
        self.left_layout.addWidget(QLabel("Enter the interval for the data"))

        self.row_4 = QHBoxLayout()
        self.start_date_line = QLineEdit()
        self.start_date_line.setPlaceholderText("Start (YYYY-MM-DD)")
        self.row_4.addWidget(self.start_date_line)
        self.start_date_line.textChanged.connect(self.check_date_input)
        self.end_date_line = QLineEdit()
        self.end_date_line.setPlaceholderText("End (YYYY-MM-DD)")
        self.row_4.addWidget(self.end_date_line)
        self.end_date_line.textChanged.connect(self.check_date_input)
        self.left_layout.addLayout(self.row_4)

        self.download_layout = QHBoxLayout()
        self.download_data_button = QPushButton()
        self.download_data_button.setText("Download Data")
        self.download_data_button.setEnabled(False)
        self.download_data_button.clicked.connect(self.download_data)
        self.download_layout.addWidget(self.download_data_button)
        self.filename_line = QLineEdit()
        self.filename_line.setPlaceholderText("Enter filename")
        self.download_layout.addWidget(self.filename_line)
        self.filename_line.textChanged.connect(self.check_filename_input)
        self.save_data_button = QPushButton()
        self.save_data_button.setText("Save Data")
        self.save_data_button.setEnabled(False)
        self.save_data_button.clicked.connect(self.save_data)
        self.download_layout.addWidget(self.save_data_button)
        self.left_layout.addLayout(self.download_layout)

        self.row_5 = QHBoxLayout()
        self.row_5.addWidget(QLabel("Enter your budget"))
        self.budget_line = QLineEdit()
        self.budget_line.setPlaceholderText("")
        self.row_5.addWidget(self.budget_line)
        self.left_layout.addLayout(self.row_5)
        
        self.selected_table = QTableWidget()
        self.left_layout.addWidget(self.selected_table)

        self.assets_buttons_layout = QHBoxLayout()
        self.open_dialog_button = QPushButton("Choose Assets")
        self.open_dialog_button.clicked.connect(self.open_selection_window)
        self.assets_buttons_layout.addWidget(self.open_dialog_button)
        self.clear_data_button = QPushButton("Clear Assets")
        self.clear_data_button.clicked.connect(self.clear_data)
        self.assets_buttons_layout.addWidget(self.clear_data_button)
        self.left_layout.addLayout(self.assets_buttons_layout)

        self.run_button = QPushButton("Run")
        self.run_button.setEnabled(False)
        self.run_button.clicked.connect(self.run)
        self.left_layout.addWidget(self.run_button)

        # Middle line

        self.mid_layout = QVBoxLayout()
        self.middle_line = QFrame()
        self.middle_line.setFrameShape(QFrame.Shape.VLine)
        self.middle_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.mid_layout.addWidget(self.middle_line)

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

    def check_date_input(self):
        date_format_start = r"^\d{4}-\d{2}-\d{2}$"  # Format: YYYY-MM-DD
        date_text_start = self.start_date_line.text()
        date_format_end = r"^\d{4}-\d{2}-\d{2}$"
        date_text_end = self.end_date_line.text()

        if re.match(date_format_start, date_text_start) and re.match(date_format_end, date_text_end) \
                                                        and date_text_start <= date_text_end:
            if self.selected_options is not None:
                self.download_data_button.setEnabled(True)
            else:
                self.download_data_button.setEnabled(False)
        else:
            self.download_data_button.setEnabled(False)

    def download_data(self):
        start_date = self.start_date_line.text()
        end_date = self.end_date_line.text()
        self.data = fetch_data(self.selected_options, start_date, end_date)
        self.run_button.setEnabled(True)
        
    def check_filename_input(self):
        # filename = self.filename_line.text().strip()
        filename = self.filename_line.text().strip()

        if filename == '':
            self.save_data_button.setEnabled(False)
        elif not filename[0] in ['.', ' '] or not re.search(r'[<>:"/\\|?*]', filename):
            if self.data is not None:
                self.save_data_button.setEnabled(True)
            else:
                self.save_data_button.setEnabled(False)
        else:
            self.save_data_button.setEnabled(False)

    def check_run_button(self):
        if self.data is not None:
            self.run_button.setEnabled(True)
        else:
            self.run_button.setEnabled(False)

    def save_data(self):
        filename="data/" + self.filename_line.text()
        if not filename.endswith('.csv'):
            filename += '.csv'
        self.data.to_csv(filename)

    def clear_data(self):
        self.selected_table.setColumnCount(0)
        self.selected_table.setRowCount(0)
        self.selected_table.clear()
        self.download_data_button.setEnabled(False)
        self.save_data_button.setEnabled(False) 
        self.selected_options = None
        self.data = None

    def load_data(self):
        pass


    def open_selection_window(self):
        """Function to open a dialog for selecting assets"""
        try:
            dialog = SelectionDialog()
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.selected_options = dialog.get_selected_options()
                self.selected_table.setColumnCount(len(self.selected_options.keys()))
                self.selected_table.setHorizontalHeaderLabels(self.selected_options.keys())
                self.selected_table.setRowCount(max([len(v) for v in self.selected_options.values()]))
                for i, category in enumerate(self.selected_options.keys()):
                    for j, item in enumerate(self.selected_options[category]):
                        q_item = QTableWidgetItem(item)
                        q_item.setFlags(q_item.flags() & ~Qt.ItemFlag.ItemIsEditable)   # blokowanie komorek
                        self.selected_table.setItem(j, i, q_item) 
                if self.selected_options:
                    # self.are_options = True
                    self.check_date_input()
                    
        except Exception as e:
            print(f"Error opening selection window: {e}")

# # ---------------------- Annealing ------------------
    def run(self):
        """Simulates portfolio optimization and updates the chart."""
        # self.budget = self.budget_line.text()

        # Load data
        # filename = "data/stocks.csv"
        # print(f"Loading data from file: {filename}")
        # data = pd.read_csv(filename, index_col=0, parse_dates=True)

        self.num_days = len(self.data)

        self.returns = self.data.pct_change().dropna()
        expected_returns = self.returns.mean() * self.num_days
        covariance_matrix = self.returns.cov() * self.num_days

        # print("\nExpected annual returns:\n", expected_returns)
        # print("\nAnnual covariance matrix:\n", covariance_matrix)

        tickers = self.data.columns

        # Perform optimization
        optimal_portfolio, optimal_sharpe = self.simulated_annealing_portfolio(
            assets=tickers,
            expected_returns=expected_returns.values,
            covariance_matrix=covariance_matrix.values,
            risk_free_rate=0.02,
            max_iter=20000,
            initial_temperature=100,
            cooling_rate=0.95,
            max_allocation=0.25,
            min_allocation=0.0
        )

        # # Print optimal portfolio allocation
        # print("\nOptimal portfolio:")
        # for ticker, allocation in zip(tickers, optimal_portfolio):
        #     print(f"{ticker}: {allocation:.2%}")
        # print(f"\nOptimal Sharpe ratio: {optimal_sharpe:.4f}")

        # Plot portfolio allocation as a pie chart
        # plt.figure(figsize=(8, 8))
        # plt.pie(
        #     optimal_portfolio,
        #     labels=tickers,
        #     autopct='%1.1f%%',
        #     startangle=140,
        #     colors=plt.cm.tab20.colors
        # )
        # plt.title("Optimal Portfolio Allocation")
        # plt.show()

        self.chart_widget.update_chart(optimal_portfolio, tickers)


    def simulated_annealing_portfolio(self, assets, expected_returns, covariance_matrix, 
        risk_free_rate=0, max_iter=10000, initial_temperature=100, 
        cooling_rate=0.99, max_allocation=0.5, min_allocation=0.0):
        """Function to optimize a portfolio using simulated annealing."""
        num_assets = len(assets)
        # current_portfolio = np.random.dirichlet(np.ones(num_assets))
        current_portfolio = np.ones(num_assets) / num_assets
        current_portfolio = self.enforce_constraints(current_portfolio, min_allocation, max_allocation)
        current_sharpe = self.calculate_sharpe(current_portfolio, expected_returns, covariance_matrix, risk_free_rate)
        best_portfolio = current_portfolio
        best_sharpe = current_sharpe
        temperature = initial_temperature

        for _ in range(max_iter):
            new_portfolio = self.make_move(current_portfolio, min_allocation, max_allocation)
            new_portfolio = self.enforce_constraints(new_portfolio, min_allocation, max_allocation)
            new_sharpe = self.calculate_sharpe(new_portfolio, expected_returns, covariance_matrix, risk_free_rate)
            if accept_move(current_sharpe, new_sharpe, temperature):
                current_portfolio = new_portfolio
                current_sharpe = new_sharpe
            if new_sharpe > best_sharpe:
                best_portfolio = new_portfolio
                best_sharpe = new_sharpe
            temperature *= cooling_rate

        return best_portfolio, best_sharpe

    def calculate_sharpe(self, weights, expected_returns, covariance_matrix, risk_free_rate=0):
        """Function to calculate the Sharpe ratio of a portfolio."""
        portfolio_return = np.dot(weights, expected_returns)
        portfolio_risk = np.sqrt(np.dot(weights, np.dot(covariance_matrix, weights)))
        return (portfolio_return - risk_free_rate) / portfolio_risk
    
    def make_move(self, weights, min_weight=0.0, max_weight=1.0):
        """Function to make a random move in the search space."""
        new_weights = np.copy(weights)
        random_idx = random.randint(0, len(weights) - 1)
        change = np.random.uniform(-0.01, 0.01)
        new_weights[random_idx] += change
        # Zapewniamy, że suma wag jest równa 1 (portfel jest zrównoważony)
        new_weights = np.clip(new_weights, min_weight, max_weight)
        new_weights /= np.sum(new_weights)  # Normalizacja wag
        return new_weights
    
    def enforce_constraints(self, portfolio, min_allocation, max_allocation):
        """Function to enforce constraints on portfolio weights."""
        portfolio = np.clip(portfolio, min_allocation, max_allocation)
        epsilon = 1e-6
        weights_sum = np.sum(portfolio)
        if weights_sum < 1 - epsilon or weights_sum > 1 + epsilon:
            portfolio /= weights_sum    
        return portfolio

## ---------------------- Dialog for selecting assets ------------------
class SelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Select Options")
        self.setGeometry(150, 150, 800, 400)
        self.dialog_layout = QHBoxLayout()
        self.categories = self.load_categories_from_json('config/tickers.json')

        for category, items in self.categories.items():
            new_layout = QVBoxLayout()
            category_label = QLabel(category)
            new_layout.addWidget(category_label)
            option_list = QListWidget()
            option_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
            option_list.addItems(items)
            new_layout.addWidget(option_list)
            self.dialog_layout.addLayout(new_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.dialog_layout.addWidget(self.button_box)

        self.setLayout(self.dialog_layout)

    def load_categories_from_json(self, file_path):
        """Function to load categories and options from a JSON file."""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except Exception as e:
            print(f"Error loading Assets from JSON file: {e}")
            return {}
        
    def get_selected_options(self):
        """Function to get selected options from the dialog."""
        selected_options = {}

        for layout_index in range(self.dialog_layout.count() - 1):  # Ostatni element to przyciski
            category_layout = self.dialog_layout.itemAt(layout_index).layout()
            if not category_layout:
                continue
            category_label = category_layout.itemAt(0).widget() # QLabel
            category = category_label.text()

            option_list = category_layout.itemAt(1).widget()  #  QListWidget
            if not option_list:
                continue
            selected_items = [item.text() for item in option_list.selectedItems()]
            if selected_items:
                selected_options[category] = selected_items
        return selected_options

## ---------------------- Chart Widget ------------------
class PortfolioChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_chart(self, weights, tickers):
        """Aktualizuje wykres kołowy na podstawie nowych danych."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.pie(
            weights, 
            labels=tickers, 
            autopct='%1.1f%%', 
            startangle=90
        )
        ax.set_title("Portfolio Distribution")
        self.canvas.draw()


# # ---------------------- Data ------------------

    # def download_data(self):
    #     self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "SPY", "BABA"]
    #     self.start_date = "2022-01-01"
    #     self.end_date = "2024-10-31"
    #     self.data = yf.download(self.tickers, start=self.start_date, end=self.end_date)['Adj Close']
    #     if self.data is not None:
    #         self.isDataLoaded = True
    #     else:
    #         print("Cannot download data!")

    # def save_csv(self, data, file_name: str):
    #     data.to_csv(file_name)
    #     print(f"Data saved in {file_name}")

    # def load_csv(self, window, file_name: str):
    #     try:
    #         self.data = pd.read_csv(file_name)
    #         if self.data is not None:
    #             self.isDataLoaded = True
    #         else:
    #             print("Cannot load data!")
    #         window.table_widget.setRowCount(len(self.data))
    #         window.table_widget.setColumnCount(len(self.data.columns))
    #         window.table_widget.setHorizontalHeaderLabels(self.data.columns)

    #         for row in range(len(self.data)):
    #             for col in range(len(self.data.columns)):
    #                 item = QTableWidgetItem(str(self.data.iloc[row, col]))
    #                 window.table_widget.setItem(row, col, item)
    #     except Exception as e:
    #         print(f"Error loading data: {e}")
