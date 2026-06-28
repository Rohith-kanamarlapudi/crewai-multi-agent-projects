import unittest
from accounts import get_share_price, Account

class TestGetSharePrice(unittest.TestCase):
    def test_known_symbols(self):
        self.assertEqual(get_share_price("AAPL"), 150.0)
        self.assertEqual(get_share_price("TSLA"), 700.0)
        self.assertEqual(get_share_price("GOOGL"), 2800.0)

    def test_unknown_symbol(self):
        with self.assertRaises(ValueError):
            get_share_price("UNKNOWN")

    def test_empty_symbol(self):
        with self.assertRaises(ValueError):
            get_share_price("")

class TestAccountCreation(unittest.TestCase):
    def test_default_initialization(self):
        acc = Account("test1")
        self.assertEqual(acc.get_cash_balance(), 0.0)
        self.assertEqual(acc.get_holdings(), {})
        self.assertEqual(acc.get_transactions(), [])

    def test_positive_initial_deposit(self):
        acc = Account("test2", 1000.0)
        self.assertEqual(acc.get_cash_balance(), 1000.0)

    def test_zero_initial_deposit(self):
        acc = Account("test3", 0.0)
        self.assertEqual(acc.get_cash_balance(), 0.0)

    def test_negative_initial_deposit(self):
        with self.assertRaises(ValueError) as ctx:
            Account("test4", -100.0)
        self.assertEqual(str(ctx.exception), "Initial deposit cannot be negative")

class TestDeposit(unittest.TestCase):
    def setUp(self):
        self.acc = Account("deposit_test", 500.0)

    def test_deposit_positive(self):
        new_balance = self.acc.deposit(200.0)
        self.assertEqual(new_balance, 700.0)
        self.assertEqual(self.acc.get_cash_balance(), 700.0)

    def test_deposit_zero(self):
        with self.assertRaises(ValueError) as ctx:
            self.acc.deposit(0.0)
        self.assertEqual(str(ctx.exception), "Deposit amount must be positive")

    def test_deposit_negative(self):
        with self.assertRaises(ValueError) as ctx:
            self.acc.deposit(-10.0)
        self.assertEqual(str(ctx.exception), "Deposit amount must be positive")

class TestWithdraw(unittest.TestCase):
    def setUp(self):
        self.acc = Account("withdraw_test", 1000.0)

    def test_withdraw_success(self):
        new_balance = self.acc.withdraw(400.0)
        self.assertEqual(new_balance, 600.0)
        self.assertEqual(self.acc.get_cash_balance(), 600.0)

    def test_withdraw_exact_balance(self):
        new_balance = self.acc.withdraw(1000.0)
        self.assertEqual(new_balance, 0.0)

    def test_withdraw_insufficient(self):
        with self.assertRaises(ValueError) as ctx:
            self.acc.withdraw(1500.0)
        self.assertEqual(str(ctx.exception), "Insufficient funds")

    def test_withdraw_zero(self):
        with self.assertRaises(ValueError) as ctx:
            self.acc.withdraw(0.0)
        self.assertEqual(str(ctx.exception), "Withdrawal amount must be positive")

    def test_withdraw_negative(self):
        with self.assertRaises(ValueError) as ctx:
            self.acc.withdraw(-50.0)
        self.assertEqual(str(ctx.exception), "Withdrawal amount must be positive")

class TestBuy(unittest.TestCase):
    def setUp(self):
        self.acc = Account("buy_test", 2000.0)

    def test_buy_success(self):
        new_balance = self.acc.buy("AAPL", 10)
        self.assertEqual(new_balance, 2000.0 - 150.0 * 10)
        self.assertEqual(self.acc.get_holdings(), {"AAPL": 10})

    def test_buy_zero_quantity(self):
        with self.assertRaises(ValueError) as ctx:
            self.acc.buy("TSLA", 0)
        self.assertEqual(str(ctx.exception), "Quantity must be positive")

    def test_buy_negative_quantity(self):
        with self.assertRaises(ValueError) as ctx:
            self.acc.buy("GOOGL", -1)
        self.assertEqual(str(ctx.exception), "Quantity must be positive")

    def test_buy_insufficient_funds(self):
        with self.assertRaises(ValueError) as ctx:
            self.acc.buy("TSLA", 3)  # 3 * 700 = 2100 > 2000
        self.assertEqual(str(ctx.exception), "Insufficient funds to buy shares")

    def test_buy_unknown_symbol(self):
        with self.assertRaises(ValueError):
            self.acc.buy("UNKNOWN", 1)

class TestSell(unittest.TestCase):
    def setUp(self):
        self.acc = Account("sell_test", 5000.0)
        self.acc.buy("AAPL", 10)
        self.acc.buy("TSLA", 2)

    def test_sell_partial(self):
        new_balance = self.acc.sell("AAPL", 4)
        self.assertAlmostEqual(new_balance, 5000.0 - 1500.0 + 4 * 150.0)
        self.assertEqual(self.acc.get_holdings(), {"AAPL": 6, "TSLA": 2})

    def test_sell_all(self):
        new_balance = self.acc.sell("AAPL", 10)
        self.assertAlmostEqual(new_balance, 5000.0 - 1500.0 + 10 * 150.0)
        self.assertNotIn("AAPL", self.acc.get_holdings())
        self.assertEqual(self.acc.get_holdings(), {"TSLA": 2})

    def test_sell_more_than_held(self):
        with self.assertRaises(ValueError) as ctx:
            self.acc.sell("AAPL", 20)
        self.assertEqual(str(ctx.exception), "Insufficient shares to sell")

    def test_sell_nonexistent_holding(self):
        with self.assertRaises(ValueError) as ctx:
            self.acc.sell("GOOGL", 1)
        self.assertEqual(str(ctx.exception), "Insufficient shares to sell")

    def test_sell_zero_quantity(self):
        with self.assertRaises(ValueError) as ctx:
            self.acc.sell("AAPL", 0)
        self.assertEqual(str(ctx.exception), "Quantity must be positive")

    def test_sell_negative_quantity(self):
        with self.assertRaises(ValueError) as ctx:
            self.acc.sell("AAPL", -3)
        self.assertEqual(str(ctx.exception), "Quantity must be positive")

    def test_sell_unknown_symbol(self):
        with self.assertRaises(ValueError):
            self.acc.sell("UNKNOWN", 1)

class TestPortfolioValue(unittest.TestCase):
    def setUp(self):
        self.acc = Account("port_test", 10000.0)
        self.acc.buy("AAPL", 20)
        self.acc.buy("TSLA", 5)

    def test_portfolio_value(self):
        expected = self.acc.get_cash_balance() + 20 * 150.0 + 5 * 700.0
        self.assertEqual(self.acc.get_portfolio_value(), expected)

class TestProfitLoss(unittest.TestCase):
    def setUp(self):
        self.acc = Account("pl_test", 5000.0)
        self.acc.deposit(3000.0)  # initial_deposit = 8000.0 now
        self.acc.buy("AAPL", 10)

    def test_profit_loss_positive(self):
        # Starting cash: 8000 - 1500 = 6500 + 10*150 = 8000 -> zero profit initially
        self.assertAlmostEqual(self.acc.get_profit_loss(), 0.0)

    def test_profit_loss_after_buy(self):
        # After buying at market price, value = cash + holdings = (8000-1500) + 10*150 = 8000
        # profit/loss = 0
        self.acc.buy("GOOGL", 1)  # cost 2800, cash becomes 8000-1500-2800 = 3700, holdings value = 10*150 + 1*2800 = 1500+2800=4300, total=8000
        self.assertAlmostEqual(self.acc.get_profit_loss(), 0.0)

class TestTransactions(unittest.TestCase):
    def setUp(self):
        self.acc = Account("tx_test", 1000.0)

    def test_initial_deposit_transaction(self):
        txs = self.acc.get_transactions()
        self.assertEqual(len(txs), 1)
        self.assertEqual(txs[0]["type"], "DEPOSIT")
        self.assertEqual(txs[0]["amount"], 1000.0)
        self.assertEqual(txs[0]["balance_after"], 1000.0)

    def test_multiple_transactions(self):
        self.acc.deposit(500.0)
        self.acc.withdraw(200.0)
        self.acc.buy("AAPL", 2)
        txs = self.acc.get_transactions()
        self.assertEqual(len(txs), 4)  # initial + 3 more
        self.assertEqual(txs[1]["type"], "DEPOSIT")
        self.assertEqual(txs[2]["type"], "WITHDRAW")
        self.assertEqual(txs[3]["type"], "BUY")
        self.assertEqual(txs[3]["symbol"], "AAPL")
        self.assertEqual(txs[3]["quantity"], 2)

class TestHoldings(unittest.TestCase):
    def setUp(self):
        self.acc = Account("hold_test", 10000.0)

    def test_holdings_copy(self):
        holdings = self.acc.get_holdings()
        holdings["TEST"] = 100  # modify copy
        self.assertEqual(self.acc.get_holdings(), {})

    def test_holdings_after_buy(self):
        self.acc.buy("GOOGL", 3)
        self.assertEqual(self.acc.get_holdings(), {"GOOGL": 3})

class TestEdgeCases(unittest.TestCase):
    def test_deposit_after_withdrawal(self):
        acc = Account("edge1", 500.0)
        acc.withdraw(200.0)
        acc.deposit(100.0)
        self.assertEqual(acc.get_cash_balance(), 400.0)

    def test_sell_removes_holding_entry(self):
        acc = Account("edge2", 2000.0)
        acc.buy("AAPL", 5)
        acc.sell("AAPL", 5)
        self.assertEqual(acc.get_holdings(), {})

    def test_get_portfolio_value_after_sell(self):
        acc = Account("edge3", 3000.0)
        acc.buy("TSLA", 2)  # cost 1400, cash 1600
        acc.sell("TSLA", 1) # revenue 700, cash 2300, holdings 1
        expected = 2300 + 1 * 700.0
        self.assertEqual(acc.get_portfolio_value(), expected)

    def test_profit_loss_after_deposit(self):
        acc = Account("edge4", 1000.0)
        # initial_deposit = 1000, cash = 1000, no holdings, portfolio value = 1000
        self.assertEqual(acc.get_profit_loss(), 0.0)
        acc.deposit(500.0)  # initial_deposit becomes 1500, cash becomes 1500
        # still no holdings, portfolio value = 1500, profit/loss = 0
        self.assertEqual(acc.get_profit_loss(), 0.0)

    def test_transaction_timestamps(self):
        acc = Account("edge5", 100.0)
        txs = acc.get_transactions()
        self.assertEqual(txs[0]["timestamp"], 1)
        acc.deposit(50.0)
        txs2 = acc.get_transactions()
        self.assertEqual(txs2[1]["timestamp"], 2)
        acc.withdraw(30.0)
        txs3 = acc.get_transactions()
        self.assertEqual(txs3[2]["timestamp"], 3)

if __name__ == "__main__":
    unittest.main()