from pydantic import BaseModel, Field
from langchain.tools import tool
import pandas as pd

from memory.session_store import get_dataframe
from utils.context import session_id_context

class ExpenseInput(BaseModel):
    # file_path: str = Field(description="Path to the CSV file containing expenses with columns: date, category, amount, description")
    query: str = Field(description="The user query or natural language request for analyzing expenses.")

@tool("analyze_expenses", args_schema=ExpenseInput)
def analyze_expenses(query: str) -> str:
    """Use this to analyze the user's uploaded expense data. The data is already available in the session — no file path needed. Call this whenever the user asks about their expenses, spending, categories, or transactions."""
    try:
        session_id = session_id_context.get(None)
        if not session_id:
            return "Error: Active session ID not found."

        # 2. Fetch the DataFrame from the session store
        df = get_dataframe(session_id)

        # 3. Handle the no-file / no-dataframe case gracefully
        if df is None:
            return "No expense file has been uploaded or processed yet for this session. Please upload a file first."

        # df = pd.read_csv(file_path)
        df = df.dropna(how='all')

        if df.empty:
            return "No data found in the file."

        # Normalize column names (strip whitespace and convert to lowercase)
        df.columns = [str(c).strip().lower() for c in df.columns]

        if 'amount' not in df.columns or 'category' not in df.columns:
            return "CSV must have 'amount' and 'category' columns."

        working_df = df.copy()

        # Robust numeric parsing: remove currency symbols, commas, whitespace
        if not pd.api.types.is_numeric_dtype(working_df['amount']):
            cleaned = (
                working_df['amount']
                .astype(str)
                .str.replace(r'[\$,₹,€,£,\s]', '', regex=True)
                .str.replace(',', '', regex=False)
            )
            working_df['amount'] = pd.to_numeric(cleaned, errors='coerce')

        working_df = working_df.dropna(subset=['amount', 'category'])

        if working_df.empty:
            return "No valid numeric expense records found in the file."

        total_expenses = round(float(working_df['amount'].sum()), 2)
        category_breakdown = working_df.groupby('category')['amount'].sum().round(2)

        if not category_breakdown.empty:
            biggest_category = category_breakdown.idxmax()
            biggest_category_amount = category_breakdown.max()
        else:
            biggest_category, biggest_category_amount = "None", 0

        top_df = working_df.sort_values(by='amount', ascending=False).head(3)
        top_three_list = []
        for _, row in top_df.iterrows():
            desc = row.get("description", row["category"]) if "description" in working_df.columns else row["category"]
            top_three_list.append(f"- {desc}: {row['amount']}")
        top_three_str = "\n".join(top_three_list) if top_three_list else "- No transactions found"

        lines = [
            f"Total Expenses: {total_expenses}",
            "\nBreakdown by Category:"
        ]
        for category, amount in category_breakdown.items():
            lines.append(f"- {category}: {amount}")

        lines += [
            f"\nBiggest Spending Category: {biggest_category} ({biggest_category_amount})",
            "\nTop 3 Largest Transactions:",
            top_three_str
        ]

        return "\n".join(lines)

    except Exception as e:
        return f"Error analyzing expenses: {str(e)}"