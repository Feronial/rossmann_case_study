import unittest
import pandas as pd
from utils.data_processing import DateProcessor  # Import the DateProcessor class from your module

class TestDateProcessor(unittest.TestCase):
    """
    Test suite for the DateProcessor class.

    This class contains various test cases to ensure the correctness of the rolling statistics
    calculations for sales and customers in the DateProcessor class.
    """
    
    def setUp(self):
        """
        Set up function to prepare data and instance of DateProcessor for each test.

        Creates a DataFrame with sample data including 'Store', 'Month', 'Sales', 'Customers', and 'Date' columns.
        This setup is used to test the rolling statistics methods of the DateProcessor class.
        """
        data = {
            'Store': [1, 1, 1, 1, 1, 1, 1, 1],
            'Month': [1, 1, 1, 1, 1, 1, 1, 1],
            'Sales': [100, 200, 300, 400, 500, 600, 700, 800],
            'Customers': [10, 20, 30, 40, 50, 60, 70, 80],
            'Date': pd.date_range(start='1/1/2020', periods=8)
        }
        self.df = pd.DataFrame(data)
        self.processor = DateProcessor(self.df)

    def test_process_rolling_sales_statistics(self):
        """
        Test the process_rolling_sales_statistics method.

        Ensures that the method correctly calculates the total sales for the last week,
        including handling of the rolling window and the shift operation.
        """
        processed_df = self.processor.process_rolling_sales_statistics()
        expected_sales_last_week = [None, None, None, None, None, None, 2100, 2800]  # Sum of the first 7 days, shifted by 1
        self.assertTrue((processed_df['TotalSales_LastWeek'].fillna(0).values == expected_sales_last_week).all())

    def test_process_rolling_customers_statistics(self):
        """
        Test the process_rolling_customers_statistics method.

        Verifies that the method accurately computes the total customers for the last week,
        correctly applying the rolling window and shift operations.
        """
        processed_df = self.processor.process_rolling_customers_statistics()
        expected_customers_last_week = [None, None, None, None, None, None, 210, 280]  # Sum of the first 7 customers, shifted by 1
        self.assertTrue((processed_df['TotalCustomers_LastWeek'].fillna(0).values == expected_customers_last_week).all())

if __name__ == '__main__':
    unittest.main()