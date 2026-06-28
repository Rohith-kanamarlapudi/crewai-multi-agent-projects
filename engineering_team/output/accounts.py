def get_share_price(symbol: str) -> float:
    prices = {"AAPL": 150.0, "TSLA": 700.0, "GOOGL": 2800.0}
    if symbol not in prices:
        raise ValueError(f"Unknown symbol: {symbol}")
    return prices[symbol]


class Account:
    def __init__(self, account_id: str, initial_deposit: float = 0.0) -> None:
        self._account_id = account_id
        self._cash_balance = 0.0
        self._holdings: dict[str, int] = {}
        self._transactions: list[dict] = []
        self._initial_deposit = 0.0
        self._tx_counter = 0
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative")
        if initial_deposit > 0:
            self.deposit(initial_deposit)
            self._initial_deposit = initial_deposit

    def _record_transaction(self, tx_type: str, symbol: str | None, quantity: int | None, amount: float, balance_after: float) -> None:
        self._tx_counter += 1
        self._transactions.append({
            "type": tx_type,
            "symbol": symbol,
            "quantity": quantity,
            "amount": amount,
            "balance_after": balance_after,
            "timestamp": self._tx_counter
        })

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._cash_balance += amount
        self._initial_deposit += amount
        self._record_transaction("DEPOSIT", None, None, amount, self._cash_balance)
        return self._cash_balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._cash_balance:
            raise ValueError("Insufficient funds")
        self._cash_balance -= amount
        self._record_transaction("WITHDRAW", None, None, -amount, self._cash_balance)
        return self._cash_balance

    def buy(self, symbol: str, quantity: int) -> float:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        price = get_share_price(symbol)
        total_cost = price * quantity
        if total_cost > self._cash_balance:
            raise ValueError("Insufficient funds to buy shares")
        self._cash_balance -= total_cost
        self._holdings[symbol] = self._holdings.get(symbol, 0) + quantity
        self._record_transaction("BUY", symbol, quantity, -total_cost, self._cash_balance)
        return self._cash_balance

    def sell(self, symbol: str, quantity: int) -> float:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        price = get_share_price(symbol)
        held = self._holdings.get(symbol, 0)
        if quantity > held:
            raise ValueError("Insufficient shares to sell")
        total_revenue = price * quantity
        self._cash_balance += total_revenue
        self._holdings[symbol] = held - quantity
        if self._holdings[symbol] == 0:
            del self._holdings[symbol]
        self._record_transaction("SELL", symbol, quantity, total_revenue, self._cash_balance)
        return self._cash_balance

    def get_portfolio_value(self) -> float:
        total = self._cash_balance
        for symbol, qty in self._holdings.items():
            total += qty * get_share_price(symbol)
        return total

    def get_profit_loss(self) -> float:
        return self.get_portfolio_value() - self._initial_deposit

    def get_holdings(self) -> dict[str, int]:
        return self._holdings.copy()

    def get_transactions(self) -> list[dict]:
        return self._transactions.copy()

    def get_cash_balance(self) -> float:
        return self._cash_balance