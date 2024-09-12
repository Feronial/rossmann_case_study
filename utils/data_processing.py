import pandas as pd
import  numpy as np

class DateProcessor:
    """
    A class to process date columns in a pandas DataFrame.

    Attributes:
    -----------
    df : pd.DataFrame
        A pandas DataFrame containing a 'Date' column.

    Methods:
    --------
    process_date():
        Converts the 'Date' column to datetime format and extracts 'Day', 'Month', and 'Quarter'.
    """
 
    def __init__(self, dataframe):
        """
        Constructs all the necessary attributes for the DateProcessor object.

        Parameters:
        -----------
        dataframe : pd.DataFrame
            A pandas DataFrame containing a 'Date' column.
        """
        self.df = dataframe


    def process_date(self):
        """
        Processes the 'Date' column in the DataFrame: converts it to datetime format,
        and extracts 'Day', 'Month', and 'Quarter' as separate columns.

        Returns:
        --------
        pd.DataFrame
            The updated DataFrame with new columns for 'Day', 'Month', and 'Quarter'.
        """
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df['Day'] = self.df['Date'].dt.day
        self.df['Month'] = self.df['Date'].dt.month
        self.df['Quarter'] = self.df['Date'].dt.quarter
        return self.df


    def process_state_holiday(self):
        """
        Processes the 'StateHoliday' column by creating binary columns for each holiday type
        and then drops the original 'StateHoliday' column.

        Returns:
        --------
        pd.DataFrame
            The updated DataFrame with new binary columns for each state holiday type and without the original 'StateHoliday' column.
        """
        self.df['StateHoliday_0'] = np.where((self.df['StateHoliday'] == 0) | (self.df['StateHoliday'] == '0'), 1, 0)
        self.df['StateHoliday_a'] = np.where(self.df['StateHoliday'] == 'a', 1, 0)
        self.df['StateHoliday_b'] = np.where(self.df['StateHoliday'] == 'b', 1, 0)
        self.df['StateHoliday_c'] = np.where(self.df['StateHoliday'] == 'c', 1, 0)
        self.df = self.df.drop(['StateHoliday'], axis=1)
        return self.df
    
    def process_store_type(self):
        """
        Processes the 'StoreType' column by creating binary columns for each store type
        and then drops the original 'StoreType' column.

        Returns:
        --------
        pd.DataFrame
            The updated DataFrame with new binary columns for each store type and without the original 'StoreType' column.
        """
        self.df['StoreType_a'] = np.where(self.df['StoreType'] == 'a', 1, 0)
        self.df['StoreType_b'] = np.where(self.df['StoreType'] == 'b', 1, 0)
        self.df['StoreType_c'] = np.where(self.df['StoreType'] == 'c', 1, 0)
        self.df['StoreType_d'] = np.where(self.df['StoreType'] == 'd', 1, 0)
        self.df = self.df.drop(['StoreType'], axis=1)
        return self.df


    def process_promo_interval(self):
        """
        Processes the 'PromoInterval' column by creating binary columns for each month mentioned in the interval
        and then drops the original 'PromoInterval' column.

        Returns:
        --------
        pd.DataFrame
            The updated DataFrame with new binary columns for each month mentioned in the 'PromoInterval' and without the original 'PromoInterval' column.
        """
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        for month in months:
            self.df[f'PromoInterval_{month}'] = np.where(self.df['PromoInterval'].str.contains(month, na=False), 1, 0)
        self.df = self.df.drop(['PromoInterval'], axis=1)
        return self.df


    def process_historical_data(self):
        """
        Sorts the DataFrame by 'Store' and 'Date', and calculates historical sales and customer metrics
        for the last week and last month.

        Returns:
        --------
        pd.DataFrame
            The updated DataFrame with new columns for last week's and last month's sales and customers.
        """
        # Sort the DataFrame by Store and Date
        self.df = self.df.sort_values(['Store', 'Date'])

        # Calculate the last week same day sales and customers
        self.df['Sales_LastWeek'] = self.df.groupby(['Store'])['Sales'].transform(lambda x: x.shift(7))
        self.df['Sales_LastMonth'] = self.df.groupby(['Store'])['Sales'].transform(lambda x: x.shift(30))

        self.df['Customers_LastWeek'] = self.df.groupby(['Store'])['Customers'].transform(lambda x: x.shift(7))
        self.df['Customers_LastMonth'] = self.df.groupby(['Store'])['Customers'].transform(lambda x: x.shift(30))

        return self.df
    

    def process_rolling_sales_statistics(self):
        """
        Calculates rolling statistics for sales over the last week, grouped by 'Store' and 'Month'.

        Returns:
        --------
        pd.DataFrame
            The updated DataFrame with new columns for rolling statistics of sales.
        """
        # Calculate rolling statistics for sales
        self.df['TotalSales_LastWeek'] = self.df.groupby(['Store', 'Month'])['Sales'].transform(lambda x: x.rolling(window=7).sum().shift(1))
        self.df['MeanSales_LastWeek'] = self.df.groupby(['Store', 'Month'])['Sales'].transform(lambda x: x.rolling(window=7).mean().shift(1))
        self.df['MedianSales_LastWeek'] = self.df.groupby(['Store', 'Month'])['Sales'].transform(lambda x: x.rolling(window=7).median().shift(1))
        self.df['MinSales_LastWeek'] = self.df.groupby(['Store', 'Month'])['Sales'].transform(lambda x: x.rolling(window=7).min().shift(1))
        self.df['MaxSales_LastWeek'] = self.df.groupby(['Store', 'Month'])['Sales'].transform(lambda x: x.rolling(window=7).max().shift(1))
        self.df['StdSales_LastWeek'] = self.df.groupby(['Store', 'Month'])['Sales'].transform(lambda x: x.rolling(window=7).std().shift(1))

        return self.df


    def process_rolling_customers_statistics(self):
        """
        Calculates rolling statistics for customers over the last week, grouped by 'Store' and 'Month'.

        Returns:
        --------
        pd.DataFrame
            The updated DataFrame with new columns for rolling statistics of customers.
        """
        # Calculate rolling statistics for customers
        self.df['TotalCustomers_LastWeek'] = self.df.groupby(['Store', 'Month'])['Customers'].transform(lambda x: x.rolling(window=7).sum().shift(1))
        self.df['MeanCustomers_LastWeek'] = self.df.groupby(['Store', 'Month'])['Customers'].transform(lambda x: x.rolling(window=7).mean().shift(1))
        self.df['MedianCustomers_LastWeek'] = self.df.groupby(['Store', 'Month'])['Customers'].transform(lambda x: x.rolling(window=7).median().shift(1))
        self.df['MinCustomers_LastWeek'] = self.df.groupby(['Store', 'Month'])['Customers'].transform(lambda x: x.rolling(window=7).min().shift(1))
        self.df['MaxCustomers_LastWeek'] = self.df.groupby(['Store', 'Month'])['Customers'].transform(lambda x: x.rolling(window=7).max().shift(1))
        self.df['StdCustomers_LastWeek'] = self.df.groupby(['Store', 'Month'])['Customers'].transform(lambda x: x.rolling(window=7).std().shift(1))

        return self.df