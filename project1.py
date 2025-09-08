import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# 1. Functions
# -------------------------------

def load_file():
    """Load CSV file and display summary"""
    global df
    file_path = filedialog.askopenfilename(filetypes=[("sample_expenses.csv", "*.csv")])

    if not file_path:
        return

    try:
        df = pd.read_csv('sample_expenses.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        messagebox.showinfo("Success", "File loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not load file:\n{e}")

def show_category_chart():
    """Plot pie chart of expenses by category"""
    if df is None:
        messagebox.showwarning("Warning", "Load a file first!")
        return
    category_summary = df.groupby("Category")["Amount"].sum()
    plt.figure(figsize=(6, 6))
    plt.pie(category_summary, labels=category_summary.index, autopct='%1.1f%%')
    plt.title("Expense Distribution by Category")
    plt.show()

def show_monthly_chart():
    """Plot bar chart of monthly expenses"""
    if df is None:
        messagebox.showwarning("Warning", "Load a file first!")
        return
    monthly_summary = df.groupby(df['Date'].dt.to_period("M"))["Amount"].sum()
    plt.figure(figsize=(8, 5))
    monthly_summary.plot(kind="bar", color="skyblue")
    plt.title("Monthly Expenses")
    plt.ylabel("Amount")
    plt.show()

def check_budget():
    """Check if monthly expenses exceed budget"""
    if df is None:
        messagebox.showwarning("Warning", "Load a file first!")
        return
    try:
        budget = float(budget_entry.get())
        monthly_summary = df.groupby(df['Date'].dt.to_period("M"))["Amount"].sum()
        latest_month_expense = monthly_summary.iloc[-1]
        if latest_month_expense > budget:
            messagebox.showerror("Budget Alert", f"⚠ Budget exceeded!\nSpent: {latest_month_expense}, Limit: {budget}")
        else:
            messagebox.showinfo("Budget Check", f"✅ Within budget.\nSpent: {latest_month_expense}, Limit: {budget}")
    except ValueError:
        messagebox.showerror("Error", "Enter a valid budget amount.")

def export_report():
    """Export full expense data to Excel"""
    if df is None:
        messagebox.showwarning("Warning", "Load a file first!")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if save_path:
        df.to_excel(save_path, index=False)
        messagebox.showinfo("Export", "Report exported successfully!")

# -------------------------------
# 2. Tkinter UI Setup
# -------------------------------
df = None  # global dataframe

root = tk.Tk()
root.title("Expense Tracker with Visuals")
root.geometry("400x300")

# Buttons
load_btn = tk.Button(root, text="📂 Load CSV", command=load_file)
load_btn.pack(pady=5)

cat_btn = tk.Button(root, text="📊 Show Category Chart", command=show_category_chart)
cat_btn.pack(pady=5)

month_btn = tk.Button(root, text="📅 Show Monthly Chart", command=show_monthly_chart)
month_btn.pack(pady=5)

# Budget check
budget_label = tk.Label(root, text="Enter Monthly Budget:")
budget_label.pack()
budget_entry = tk.Entry(root)
budget_entry.pack(pady=5)

budget_btn = tk.Button(root, text="💰 Check Budget", command=check_budget)
budget_btn.pack(pady=5)

# Export report
export_btn = tk.Button(root, text="📤 Export Report", command=export_report)
export_btn.pack(pady=10)

root.mainloop()

 