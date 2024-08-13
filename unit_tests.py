import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from main import freeze_symbol, is_symbol_frozen, moving_average, calculate_quantity, create_buy_order

class TestTradingBot(unittest.TestCase):

    @patch('main.sqlite3.connect')
    def test_freeze_symbol(self, mock_sqlite3_connect):
        mock_cursor = MagicMock()
        mock_sqlite3_connect.return_value.cursor.return_value = mock_cursor
        freeze_symbol('AAPL', datetime.now())
        mock_cursor.execute.assert_called_once()
        mock_sqlite3_connect.return_value.commit.assert_called_once()
        mock_sqlite3_connect.return_value.close.assert_called_once()

    @patch('main.sqlite3.connect')
    def test_is_symbol_frozen(self, mock_sqlite3_connect):
        mock_cursor = MagicMock()
        mock_sqlite3_connect.return_value.cursor.return_value = mock_cursor
        is_symbol_frozen('AAPL')
        mock_cursor.execute.assert_called_once()
        mock_sqlite3_connect.return_value.close.assert_called_once()

    def test_moving_average(self):
        lst = [1, 2, 3, 4, 5]
        window_size = 3
        result = moving_average(lst, window_size)
        self.assertEqual(result, [2.0, 3.0, 4.0])

    def test_calculate_quantity(self):
        current_buying_power = 1000
        open_price = 200
        result = calculate_quantity(current_buying_power, open_price)
        self.assertEqual(result, 5)

    def test_create_buy_order(self):
        symbol = 'AAPL'
        quantity = 5
        result = create_buy_order(symbol, quantity)
        self.assertEqual(result.symbol, 'AAPL')
        self.assertEqual(result.qty, 5)
        self.assertEqual(result.side, 'buy')
        self.assertEqual(result.type, 'market')
        self.assertEqual(result.time_in_force, 'gtc')

if __name__ == '__main__':
    unittest.main()