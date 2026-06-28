import gradio as gr
from accounts import Account

# Global account instance for single user
account = None

def create_account(initial_deposit: float):
    global account
    try:
        account = Account("user1", initial_deposit)
        return f"Account created with deposit ${initial_deposit:.2f}. Cash balance: ${account.get_cash_balance():.2f}"
    except ValueError as e:
        return f"Error: {e}"

def deposit(amount: float):
    if account is None:
        return "Please create an account first"
    try:
        account.deposit(amount)
        return f"Deposited ${amount:.2f}. Cash balance: ${account.get_cash_balance():.2f}"
    except ValueError as e:
        return f"Error: {e}"

def withdraw(amount: float):
    if account is None:
        return "Please create an account first"
    try:
        account.withdraw(amount)
        return f"Withdrew ${amount:.2f}. Cash balance: ${account.get_cash_balance():.2f}"
    except ValueError as e:
        return f"Error: {e}"

def buy_stock(symbol: str, quantity: int):
    if account is None:
        return "Please create an account first"
    try:
        account.buy(symbol, quantity)
        return f"Bought {quantity} shares of {symbol}. Cash balance: ${account.get_cash_balance():.2f}"
    except ValueError as e:
        return f"Error: {e}"

def sell_stock(symbol: str, quantity: int):
    if account is None:
        return "Please create an account first"
    try:
        account.sell(symbol, quantity)
        return f"Sold {quantity} shares of {symbol}. Cash balance: ${account.get_cash_balance():.2f}"
    except ValueError as e:
        return f"Error: {e}"

def get_portfolio_summary():
    if account is None:
        return "Please create an account first", 0, 0
    holdings = account.get_holdings()
    portfolio_value = account.get_portfolio_value()
    pnl = account.get_profit_loss()
    cash = account.get_cash_balance()
    summary = f"Cash: ${cash:.2f} | Portfolio Value: ${portfolio_value:.2f} | P&L: ${pnl:.2f}"
    holdings_str = "\n".join([f"{sym}: {qty} shares" for sym, qty in holdings.items()]) or "No holdings"
    return holdings_str, portfolio_value, pnl

def get_transactions():
    if account is None:
        return []
    txns = account.get_transactions()
    rows = []
    for t in txns:
        row = [t["type"], t.get("symbol", ""), t.get("quantity", ""), f"${t['amount']:.2f}", f"${t['balance_after']:.2f}"]
        rows.append(row)
    return rows

# Build Gradio UI
with gr.Blocks(title="Trading Account Simulator") as demo:
    gr.Markdown("# Trading Account Simulator")
    gr.Markdown("Manage a single trading account. Create an account first, then perform actions.")

    with gr.Row():
        initial_deposit_input = gr.Number(label="Initial Deposit ($)", value=0, precision=2)
        create_btn = gr.Button("Create Account")
    create_output = gr.Textbox(label="Result", interactive=False)

    with gr.Row():
        with gr.Column():
            gr.Markdown("## Cash Operations")
            dep_amount = gr.Number(label="Deposit Amount ($)", value=100, precision=2)
            dep_btn = gr.Button("Deposit")
            dep_output = gr.Textbox(label="Result", interactive=False)
        with gr.Column():
            withdraw_amount = gr.Number(label="Withdraw Amount ($)", value=50, precision=2)
            withdraw_btn = gr.Button("Withdraw")
            withdraw_output = gr.Textbox(label="Result", interactive=False)

    with gr.Row():
        with gr.Column():
            gr.Markdown("## Trade Stocks")
            symbol_input = gr.Dropdown(choices=["AAPL", "TSLA", "GOOGL"], label="Symbol", value="AAPL")
            qty_buy = gr.Number(label="Quantity to Buy", value=1, precision=0)
            buy_btn = gr.Button("Buy")
            buy_output = gr.Textbox(label="Result", interactive=False)
        with gr.Column():
            qty_sell = gr.Number(label="Quantity to Sell", value=1, precision=0)
            sell_btn = gr.Button("Sell")
            sell_output = gr.Textbox(label="Result", interactive=False)

    with gr.Row():
        with gr.Column():
            gr.Markdown("## Portfolio Overview")
            refresh_btn = gr.Button("Refresh")
            holdings_display = gr.Textbox(label="Holdings", interactive=False)
            portfolio_value_display = gr.Number(label="Total Portfolio Value ($)", interactive=False)
            pnl_display = gr.Number(label="Profit/Loss ($)", interactive=False)
        with gr.Column():
            gr.Markdown("## Transaction History")
            txn_df = gr.Dataframe(headers=["Type", "Symbol", "Quantity", "Amount", "Balance After"], label="Transactions")

    # Wire events
    create_btn.click(fn=create_account, inputs=initial_deposit_input, outputs=create_output)
    dep_btn.click(fn=deposit, inputs=dep_amount, outputs=dep_output)
    withdraw_btn.click(fn=withdraw, inputs=withdraw_amount, outputs=withdraw_output)
    buy_btn.click(fn=buy_stock, inputs=[symbol_input, qty_buy], outputs=buy_output)
    sell_btn.click(fn=sell_stock, inputs=[symbol_input, qty_sell], outputs=sell_output)
    refresh_btn.click(fn=get_portfolio_summary, outputs=[holdings_display, portfolio_value_display, pnl_display])
    # Also update transactions on refresh
    refresh_btn.click(fn=get_transactions, outputs=txn_df)

    # Initial load: nothing
    # Provide a way to see transactions after any action? Could also auto-refresh but we keep simple with Refresh button.

if __name__ == "__main__":
    demo.launch()