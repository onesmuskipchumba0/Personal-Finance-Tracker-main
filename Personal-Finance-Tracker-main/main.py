import main_ui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox,QFileDialog
from PyQt5.QtCore import Qt
import sys
from datetime import datetime
import resources_rc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#import the main ui
class Main(QMainWindow):
    def __init__(self):
        #income dataframe
        self.data = pd.DataFrame(columns=['date','income_source','amount'])
        #expences dataframe
        self.expences_df = pd.DataFrame(columns=['date','category','amount'])
        #budget dataframe
        self.budget_df = pd.DataFrame(columns=['amount','category'])

        super().__init__()
        #Load the main window
        self.main_window_ui = main_ui.Ui_MainWindow()
        self.main_window_ui.setupUi(self)
        #Set stacked widget index to zero
        self.main_window_ui.StackedWidget.setCurrentIndex(0)
        #Menu File > New
        self.main_window_ui.actionIncome_Source.triggered.connect(self.income_tracking_func)
        self.main_window_ui.actionExpence_Source.triggered.connect(self.expence_tracking_func)
        self.main_window_ui.actionBudget_Management.triggered.connect(self.budget_management_func)
        #menu Menu
        self.main_window_ui.actionIncome_Tracking.triggered.connect(self.income_tracking_func)
        self.main_window_ui.actionExpence_Tracking.triggered.connect(self.expence_tracking_func)
        self.main_window_ui.actionBudget_Tracking.triggered.connect(self.budget_management_func)
        #menu Import
        self.main_window_ui.actionIncome_Tracking_Data_3.triggered.connect(self.reports_func)
        self.main_window_ui.actionExpence_Tracking_Data_3.triggered.connect(self.reports_func)
        self.main_window_ui.actionBudget_Management_Data_3.triggered.connect(self.reports_func)
        #menu save as CSv
        self.main_window_ui.actionIncome_Tracking_Data.triggered.connect(self.post_income)
        self.main_window_ui.actionExpence_Tracking_Data.triggered.connect(self.expence_tracking_func)
        self.main_window_ui.actionBudget_Management_Data.triggered.connect(self.budget_management_func)
        #menu save as Excel
        self.main_window_ui.actionIncome_Tracking_Data_2.triggered.connect(self.post_income)
        self.main_window_ui.actionExpence_Tracking_Data_2.triggered.connect(self.expence_tracking_func)
        self.main_window_ui.actionBudget_Management_Data_2.triggered.connect(self.budget_management_func)
        #menu open
        self.main_window_ui.actionIncome_Data.triggered.connect(self.budget_management_func)
        self.main_window_ui.actionExpence_Data.triggered.connect(self.budget_management_func)
        self.main_window_ui.actionBudget_Data.triggered.connect(self.budget_management_func)
        #menu about
        self.main_window_ui.actionWebsite.triggered.connect(self.website)
        self.main_window_ui.actionDocumentation.triggered.connect(self.website)
        #sub menu bar buttons
        self.main_window_ui.new_2.clicked.connect(self.income_tracking_func)
        self.main_window_ui.open.clicked.connect(self.budget_management_func)
        self.main_window_ui.save_2.clicked.connect(self.website)
        self.main_window_ui.save_3.clicked.connect(self.website)
        self.main_window_ui.save.clicked.connect(self.income_tracking_func)
        #Add functionality to the buttons
        self.main_window_ui.income_tracking_btn.clicked.connect(self.income_tracking_func)
        self.main_window_ui.expence_tracking_btn.clicked.connect(self.expence_tracking_func)
        self.main_window_ui.budget_management_btn.clicked.connect(self.budget_management_func)
        self.main_window_ui.reports_btn.clicked.connect(self.reports_func)
    #button functions
    def website(self):
        import webbrowser
        webbrowser.open_new_tab('https://onesmusbett.wordpress.com')
    def amount_clear(self):
        self.amount.clear()
    def income_source_clear(self):
        self.income.clear()
        
    def income_tracking_func(self):
        self.main_window_ui.StackedWidget.setCurrentIndex(1)
        #Values for the input fields
        self.amount = self.main_window_ui.amount_income
        self.income = self.main_window_ui.income_source
        self.date = self.main_window_ui.date_income
        #Submit button
        self.post = self.main_window_ui.post_income
        self.clear = self.main_window_ui.clear_income
        self.next = self.main_window_ui.next_income
        #clear the data in the fields
        self.clear.clicked.connect(self.amount_clear)
        self.clear.clicked.connect(self.income_source_clear)
        #Post data to csv or excel
        self.post.clicked.connect(self.post_income)
        self.next.clicked.connect(self.next_income)
    #This function opens a file dialog and asks the user to save a pd Dataframe
    def post_income(self):
                options = QFileDialog.Options()
                file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)
                
                if file_name:
                    if file_name.endswith('.csv'):
                        self.data.to_csv(file_name, index=False)
                        QMessageBox.information(self, "Success", f"Data saved to {file_name}")
                    elif file_name.endswith('.xlsx'):
                        self.data.to_excel(file_name, index=False)
                        QMessageBox.information(self, "Success", f"Data saved to {file_name}")
                    else:
                        QMessageBox.warning(self, "Save Error", "File format not supported. Please save as CSV or Excel.")
                else:
                    QMessageBox.warning(self, "Save Error", "File save operation canceled.")   
    
    def next_income(self):
            if not self.amount.text() or not self.income.text():
                QMessageBox.warning(self,"Input error","Values cannot be null")
            else:
                try:
                    new_row = pd.DataFrame({'date':[self.date.text()],'income_source':[self.income.text()],'amount':[int(self.amount.text())]})
                    self.data = pd.concat([self.data,new_row],ignore_index = True)
                    self.amount.clear()
                    self.income.clear()
                    QMessageBox.information(self, "Successfull",f"Data added succesfully.Press post to save to a file\nData: \n{self.data}")
                    print(self.data)
                except ValueError:
                    QMessageBox.warning(self,"Input Error","Invalid inputs, check and try again!")
    #Fucntion for the expence tracking function
    def expence_tracking_func(self):
        self.main_window_ui.StackedWidget.setCurrentIndex(2)
        #Test inputs
        category = self.main_window_ui.rent_expence
        amount  = self.main_window_ui.amount_expense
        date = self.main_window_ui.date_expence

        #the buttons
        post = self.main_window_ui.post_expence
        clear = self.main_window_ui.clear_expence
        next = self.main_window_ui.next_income_2
        def clear_expence():
            amount.clear()
        def post_expence_func():
                options = QFileDialog.Options()
                file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)
                
                if file_name:
                    if file_name.endswith('.csv'):
                        self.expences_df.to_csv(file_name, index=False)
                        QMessageBox.information(self, "Success", f"Data saved to {file_name}")
                    elif file_name.endswith('.xlsx'):
                        self.expences_df.to_excel(file_name, index=False)
                        QMessageBox.information(self, "Success", f"Data saved to {file_name}")
                    else:
                        QMessageBox.warning(self, "Save Error", "File format not supported. Please save as CSV or Excel.")
                else:
                    QMessageBox.warning(self, "Save Error", "File save operation canceled.")   
        def next_expence():
            print(category.currentText())
            if not amount.text():
                QMessageBox.warning(self,"Input error","Values cannot be null")
            else:
                try:
                    new_row = pd.DataFrame({'date':[date.text()],'category':[category.currentText()],'amount':[int(amount.text())]})
                    self.expences_df = pd.concat([self.expences_df,new_row],ignore_index = True)
                    amount.clear()
                    QMessageBox.information(self, "Successfull",f"Data added succesfully.Press post to save to a file\nData: \n{self.expences_df}")
                    print(self.expences_df)
                except ValueError:
                    QMessageBox.warning(self,"Input Error","Invalid inputs, check and try again!")

        #connect buttons to functionality
        post.clicked.connect(post_expence_func)
        clear.clicked.connect(clear_expence)
        next.clicked.connect(next_expence)
    #Function for the budget management button
    def budget_management_func(self):
        self.main_window_ui.StackedWidget.setCurrentIndex(3)
        #Inputs
        amount = self.main_window_ui.amount_budget
        category = self.main_window_ui.category_budget
        #Buttons
        post = self.main_window_ui.post_budget
        clear = self.main_window_ui.clear_budget
        next = self.main_window_ui.next_income_3
        #functions
        def clear_():
             amount.clear()
        def post_():
                options = QFileDialog.Options()
                file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)
                
                if file_name:
                    if file_name.endswith('.csv'):
                        self.budget_df.to_csv(file_name, index=False)
                        QMessageBox.information(self, "Success", f"Data saved to {file_name}")
                    elif file_name.endswith('.xlsx'):
                        self.budget_df.to_excel(file_name, index=False)
                        QMessageBox.information(self, "Success", f"Data saved to {file_name}")
                    else:
                        QMessageBox.warning(self, "Save Error", "File format not supported. Please save as CSV or Excel.")
                else:
                    QMessageBox.warning(self, "Save Error", "File save operation canceled.")   
        def next_():
            if not amount.text():
                QMessageBox.warning(self,"Input error","Values cannot be null")
            else:
                try:
                    new_row = pd.DataFrame({'amount':[amount.text()],'category':[category.currentText()]})
                    self.budget_df = pd.concat([self.budget_df,new_row],ignore_index = True)
                    amount.clear()
                    QMessageBox.information(self, "Successfull",f"Data added succesfully.Press post to save to a file\nData: \n{self.budget_df}")
                    print(self.data)
                except ValueError:
                    QMessageBox.warning(self,"Input Error","Invalid inputs, check and try again!")
        #Connecting to functions
        post.clicked.connect(post_)
        clear.clicked.connect(clear_)
        next.clicked.connect(next_)
    #Function for the reports function
    '''
    >> Get file from a pyqt5 file dialog
    >> Check the columns:
        amount,category > budget
        date,category,amount >expences
        date, income_source , amount > income
        else(none)
    Reports:
    1)Check at the income and budget
    2)Get total income
    3)Get total budget by category
    4)Get total expences by category.
    5)Subtract total expences from budget and check the overbudget or underbudget.
    6)if overbudget display the additional using a pie chart and image.
    7) if underbudget display the remaining compared to budget.
    8)Send Stats to email adress.

    Extra:
    Display the income sources as pie chart
    Display the expences as bar, line , pie chart
    Display budget as bar,line,pie chart

    Predict the values for the expences

    '''
    def reports_func(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV or Excel File", "", "CSV Files (*.csv);;Excel Files (*.xls *.xlsx);;All Files (*)", options=options)
        if file_name:
                if file_name.endswith('.csv'):
                    df = pd.read_csv(file_name)
                    if df.columns.tolist() == ['date','income_source','amount']:
                        date = df['date']
                        income = df['income_source']
                        amount = df['amount']

                        total_income = amount.sum()
                        #display the graphs
                        
                        fig,axs = plt.subplots(1,2,figsize=(9,4))
                        df.plot.pie(y='amount',ax = axs[0],labels=income.values)
                        df.plot.bar(x='income_source',y='amount',ax = axs[1])
                        axs[1].set_xlabel("Income Source")
                        axs[1].set_ylabel("Amount(ksh)")
                        plt.xticks(rotation=0)
                        plt.tight_layout(pad=3.0)
                        plt.legend(income,loc='best')
                        plt.savefig("income-data.png",dpi=300)
                        #plt.axis('off')  # Turn off axis if not needed
                        plt.show()
                    elif df.columns.tolist() == ['date','category','amount']:
                        date = df['date']
                        category = df['category']
                        amount = df['amount']                       
                        fig,axs = plt.subplots(1,2,figsize=(9,4))
                        df.plot.pie(y='amount',ax = axs[0],labels=category.values)
                        df.plot.bar(x='category',y='amount',ax = axs[1])
                        axs[1].set_xlabel("Category")
                        axs[1].set_ylabel("Amount(ksh)")
                        plt.xticks(rotation=0)
                        plt.tight_layout(pad=3.0)
                        plt.legend(category,loc='best')
                        plt.savefig("expences-data.png",dpi=300)
                        
                        plt.show()
                    elif df.columns.tolist() == ['amount','category']:
                        category = df['category']
                        amount = df['amount']                       
                        fig,axs = plt.subplots(1,2,figsize=(9,4))
                        df.plot.pie(y='amount',ax = axs[0],labels=category.values)
                        df.plot.bar(x='category',y='amount',ax = axs[1])
                        axs[1].set_xlabel("Category")
                        axs[1].set_ylabel("Amount(ksh)")
                        
                        plt.xticks(rotation=0)
                        plt.tight_layout(pad=3.0)
                        plt.legend(category,loc='best')
                        plt.savefig("budget-data.png",dpi=300)
                        plt.show()
                else:  # assuming Excel file
                    df = pd.read_excel(file_name)
                    if df.columns.tolist() == ['date','income_soource','amount']:

                        print("Income data")
                    elif df.columns.tolist() == ['date','category','amount']:
                        print('expences')
                    elif df.columns.tolist() == ['amount','category']:
                        print('budget') 
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())