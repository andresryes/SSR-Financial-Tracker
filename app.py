from flask import Flask, render_template, request, redirect, url_for
import plotly.graph_objs as go
from collections import defaultdict
import pandas as pd
import csv

app = Flask(__name__)

class Transaction:
    def __init__(self, amount, category, description):
        self.amount = amount
        self.category = category
        self.description = description

class Category:
    def __init__(self, name):
        self.name = name

class Income(Transaction):
    pass

class Expense(Transaction):
    pass

# Sample data
categories = [Category("Food"), Category("Transport"), Category("Utilities"), Category("Rent"), Category("Entertainment"), Category("Salary"), Category("Other")]

# Load transactions from CSV
def load_transactions():
    transactions = []
    df = pd.read_csv('data/financial_data.csv')
    for index, row in df.iterrows():
        if row['Amount'] >= 0:
            transaction = Income(row['Amount'], row['Category'], row['Description'])
        else:
            transaction = Expense(-row['Amount'], row['Category'], row['Description'])
        transactions.append(transaction)
    return transactions

transactions = load_transactions()

def dump_transactions(filename='data/financial_data.csv'):
    # Define the CSV file headers
    headers = ['Amount', 'Category', 'Description']
    
    # Open the file in write mode
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write the headers
        
        # Iterate over transactions and write each one to the file
        for transaction in transactions:
            # Prepare the row data depending on the type of transaction
            if isinstance(transaction, Income):
                row = [transaction.amount, transaction.category, transaction.description]
            else:
                row = [-transaction.amount, transaction.category, transaction.description]
            writer.writerow(row)

# Routes
@app.route('/')
def index():
    return render_template('index.html', categories=categories, transactions=transactions)

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        transaction_type = request.form['transaction_type']
        
        if transaction_type == 'Income':
            transaction = Income(amount, category, description)
        else:
            transaction = Expense(amount, category, description)
        
        transactions.append(transaction)
        dump_transactions()  # Update CSV after adding a transaction
        return redirect(url_for('index'))
    return render_template('add_transaction.html', categories=categories)

@app.route('/view_transactions')
def view_transactions():
    return render_template('view_transactions.html', transactions=transactions)

@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        transaction_type = request.form['transaction_type']
        
        if transaction_type == 'Income':
            transactions[transaction_id] = Income(amount, category, description)
        else:
            transactions[transaction_id] = Expense(amount, category, description)
        dump_transactions()  # Update CSV after adding a transaction
        return redirect(url_for('view_transactions'))
    transaction = transactions[transaction_id]
    return render_template('edit_transaction.html', transaction=transaction, categories=categories, transaction_id=transaction_id)

@app.route('/delete_transaction/<int:transaction_id>')
def delete_transaction(transaction_id):
    del transactions[transaction_id]
    dump_transactions()  # Update CSV after adding a transaction
    return redirect(url_for('view_transactions'))

@app.route('/dashboard')
def dashboard():
    # Separate and aggregate income and expenses
    income_sums = defaultdict(float)
    expense_sums = defaultdict(float)
    for transaction in transactions:
        if isinstance(transaction, Income):
            income_sums[transaction.category] += transaction.amount
        elif isinstance(transaction, Expense):
            expense_sums[transaction.category] += transaction.amount

    # Prepare data for the bar chart
    categories = list(set(income_sums.keys()) | set(expense_sums.keys()))  # Union of keys
    income_values = [income_sums[category] for category in categories]
    expense_values = [-expense_sums[category] for category in categories]  # Negate for visual distinction

    # Creating a bar chart with separate colors
    fig = go.Figure(data=[
        go.Bar(name='Income', x=categories, y=income_values, marker_color='green'),
        go.Bar(name='Expenses', x=categories, y=expense_values, marker_color='red')
    ])
    fig.update_layout(title='Financial Summary by Category', barmode='group', xaxis=dict(title='Category'), yaxis=dict(title='Amount'))

    # Ensure that both income and expenses are represented
    net_sums = defaultdict(float)
    for transaction in transactions:
        if isinstance(transaction, Income):
            net_sums[transaction.category] += transaction.amount
        elif isinstance(transaction, Expense):
            net_sums[transaction.category] += abs(transaction.amount)

    # This will ensure that only categories with actual values are displayed
    net_sums = {k: v for k, v in net_sums.items() if v != 0}

    labels = list(net_sums.keys())
    values = list(net_sums.values())

    # Check the values before passing to the pie chart
    print("Pie Chart Data:", labels, values)  # This should print to your Flask console

    # Creating a pie chart
    pie_fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    pie_fig.update_layout(title='Income/Expenses by Category')

    # Converting figures to JSON
    bar_graphJSON = fig.to_json()
    pie_graphJSON = pie_fig.to_json()

    # Rendering dashboard template with both graphs JSON
    return render_template('dashboard.html', bar_graphJSON=bar_graphJSON, pie_graphJSON=pie_graphJSON)

@app.route('/dump_transactions')
def dump_transactions_route():
    try:
        dump_transactions()  # Call the dump function
        return "Transactions successfully saved to CSV.", 200
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True)
