from pydantic import BaseModel, Field
from typing import Dict
from langchain.tools import tool

class BudgetInput(BaseModel):
    income: float = Field(description = "Total monthly income in INR or USD")
    expenses: Dict[str, float] = Field(description = "Dictionary of expense categories and amounts e.g. {'rent': 15000, 'food': 5000}")

@tool("budget_calculator", args_schema=BudgetInput)
def budget_calculator(income: float, expenses: Dict[str, float]) -> str:
    """Use this to calculate budget and expense breakdown. Requires income as a number and expenses as a dictionary of categories and amounts. If the user only provides a total spending figure without categories, ask them to provide a breakdown by category first."""
    if income <= 0:
        return "Income must be greater than zero."
    total_expenses = sum(expenses.values())
    remaining_budget = income - total_expenses
    lines = [
        "Budget Summary:",
        f"Income: {income}",
        f"Total Expenses: {total_expenses}",
        f"Remaining Budget: {remaining_budget}",
        "Breakdown of Expenses:"
    ]

    for expense, amount in expenses.items():
        percentage = round((amount / income) * 100, 2)
        amount_str = f"{amount}"
        lines.append(f"{expense}: {amount_str} ({percentage}% of income)")

    return "\n".join(lines)