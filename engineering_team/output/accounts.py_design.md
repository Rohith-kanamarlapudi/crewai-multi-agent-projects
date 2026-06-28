# Module Design: `accounts.py`

This module implements a simple account management system for a trading simulation platform. It contains a single class `Account` and a helper function `get_share_price` (which includes a test implementation for known symbols).

## 1. Helper Function

### `get_share_price(symbol: str) -> float`  
- **Purpose**: Returns the current market price for a given stock symbol.  
- **Test implementation**:  
  - `"AAPL"` → `150.0`  
  - `"TSLA"` → `700.0`  
  - `"GOOGL"` → `2800.0`  
  - Any other symbol raises `ValueError("Unknown symbol")`.

```python
def get_share_price(symbol: str) -> float:
    prices = {"AAPL": 150.0, "TSLA": 700.0, "GOOGL": 2800.0}
    if symbol not in prices:
        raise ValueError(f"Unknown symbol: {symbol}")
    return prices[symbol]
```

## 2. Class `Account`

Represents a single user account with cash balance, holdings of shares, and a transaction history.

### Attributes (private)
- `_account_id: str` – unique identifier for the account.
- `_cash_balance: float` – current cash amount.
- `_holdings: dict[str, int]` – mapping of stock symbol → number of shares owned.
- `_transactions: list[dict]` – chronological list of transaction records.
- `_initial_deposit: float` – total amount deposited since account creation (used for P&L calculation).

### Methods

#### `__init__(self, account_id: str, initial_deposit: float = 0.0) -> None`
- Creates a new account with the given ID.
- Performs an initial deposit if `initial_deposit > 0`.  
- Raises `ValueError` if `initial_deposit` is negative.

#### `deposit(self, amount: float) -> float`
- Increases cash balance by `amount`.  
- Returns the new cash balance.  
- Raises `ValueError` if `amount <= 0`.

#### `withdraw(self, amount: float) -> float`
- Decreases cash balance by `amount` only if sufficient funds exist (`cash_balance >= amount`).  
- Returns new cash balance.  
- Raises `ValueError` if `amount <= 0` or insufficient funds.

#### `buy(self, symbol: str, quantity: int) -> float`
- Purchases `quantity` shares of `symbol` at the current market price.  
- Deducts `quantity * get_share_price(symbol)` from cash balance.  
- Increases holdings of `symbol` by `quantity`.  
- Records a transaction with type `"BUY"`.  
- Raises `ValueError` if:
  - `symbol` is unknown.
  - `quantity <= 0`.
  - Insufficient cash to afford the total cost.
- Returns the new cash balance.

#### `sell(self, symbol: str, quantity: int) -> float`
- Sells `quantity` shares of `symbol` at current market price.  
- Adds `quantity * get_share_price(symbol)` to cash balance.  
- Decreases holdings of `symbol` by `quantity`.  
- Records a transaction with type `"SELL"`.  
- Raises `ValueError` if:
  - `symbol` is unknown.
  - `quantity <= 0`.
  - Insufficient shares held (`_holdings.get(symbol, 0) < quantity`).
- Returns the new cash balance.

#### `get_portfolio_value(self) -> float`
- Returns `cash_balance + sum(holdings[symbol] * get_share_price(symbol) for symbol in holdings)`.

#### `get_profit_loss(self) -> float`
- Returns `get_portfolio_value() - _initial_deposit`.

#### `get_holdings(self) -> dict[str, int]`
- Returns a **copy** of the current holdings dictionary (to prevent external mutation).

#### `get_transactions(self) -> list[dict]`
- Returns a **copy** of the transaction list. Each transaction record is a dictionary with keys:
  - `"type"` : `"DEPOSIT"`, `"WITHDRAW"`, `"BUY"`, or `"SELL"`.
  - `"symbol"` : stock symbol (only for BUY/SELL, otherwise `None`).
  - `"quantity"` : number of shares (only for BUY/SELL, otherwise `None`).
  - `"amount"` : cash impact (positive for deposits and sells, negative for withdrawals and buys).
  - `"balance_after"` : cash balance after the transaction.
  - `"timestamp"` : a monotonic transaction counter (int) or `datetime` (for simplicity we use a counter).

#### `get_cash_balance(self) -> float`
- Returns the current cash balance.

### Internal Helper Method (private)

#### `_record_transaction(self, tx_type: str, symbol: str | None, quantity: int | None, amount: float, balance_after: float) -> None`
- Appends a transaction dict to `_transactions`. The timestamp is an auto-incrementing integer (starting from 1) stored as an instance counter `_tx_counter`.

---

## Edge Cases & Validation Summary

| Action | Condition | Error |
|--------|-----------|-------|
| Deposit/Withdraw/Buy/Sell | `amount` or `quantity <= 0` | `ValueError` |
| Withdraw | `amount > cash_balance` | `ValueError` ("Insufficient funds") |
| Buy | `total_cost > cash_balance` | `ValueError` ("Insufficient funds to buy shares") |
| Sell | `quantity > held_shares` | `ValueError` ("Insufficient shares to sell") |
| Buy/Sell | unknown `symbol` | `ValueError` (propagated from `get_share_price`) |

All methods modify the internal state only after successful validation.

---

## Example Usage (Sketch)

```python
acc = Account("user1", 10000.0)
acc.deposit(5000)                # cash = 15000
acc.buy("AAPL", 10)              # cost 1500, cash = 13500, holds 10 AAPL
acc.buy("TSLA", 5)               # cost 3500, cash = 10000, holds 5 TSLA
acc.sell("AAPL", 3)              # get 450, cash = 10450, holds 7 AAPL
print(acc.get_portfolio_value()) # 10450 + 7*150 + 5*700 = 10450 + 1050 + 3500 = 15000
print(acc.get_profit_loss())     # 15000 - 10000 = 5000
print(acc.get_holdings())        # {"AAPL": 7, "TSLA": 5}
print(acc.get_transactions())    # list of 4 transactions
```

---

## Complete Python Module Structure (to be implemented)

```python
# accounts.py

def get_share_price(symbol: str) -> float:
    # test implementation
    pass

class Account:
    def __init__(self, account_id: str, initial_deposit: float = 0.0) -> None:
        ...
    def deposit(self, amount: float) -> float: ...
    def withdraw(self, amount: float) -> float: ...
    def buy(self, symbol: str, quantity: int) -> float: ...
    def sell(self, symbol: str, quantity: int) -> float: ...
    def get_portfolio_value(self) -> float: ...
    def get_profit_loss(self) -> float: ...
    def get_holdings(self) -> dict[str, int]: ...
    def get_transactions(self) -> list[dict]: ...
    def get_cash_balance(self) -> float: ...
    # private
    def _record_transaction(self, tx_type, symbol, quantity, amount, balance_after) -> None: ...
```