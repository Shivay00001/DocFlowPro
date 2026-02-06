"""
Sales & Expense Prediction Engine
Time series forecasting for business intelligence
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple


class SalesPredictor:
    """Predict future sales based on historical invoices"""
    
    def __init__(self):
        self.model = None
        self.trained = False
        self.prediction_accuracy = 0
    
    def train(self, invoices: List[Dict]) -> bool:
        """
        Train prediction model on historical invoices
        Returns: True if training successful
        """
        if not invoices or len(invoices) < 10:
            return False
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(invoices)
            
            # Ensure we have required fields
            if 'invoice_date' not in df.columns or 'total_amount' not in df.columns:
                return False
            
            # Convert dates and aggregate by month
            df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
            df = df.dropna(subset=['invoice_date', 'total_amount'])
            
            # Group by month
            df['month'] = df['invoice_date'].dt.to_period('M')
            monthly_sales = df.groupby('month')['total_amount'].sum().reset_index()
            
            if len(monthly_sales) < 3:
                return False
            
            # Simple moving average for prediction
            self.model = {
                'monthly_sales': monthly_sales,
                'avg_growth': self._calculate_growth_rate(monthly_sales)
            }
            
            self.trained = True
            self.prediction_accuracy = self._estimate_accuracy(monthly_sales)
            
            return True
            
        except Exception as e:
            print(f"Training error: {e}")
            return False
    
    def predict_next_month(self) -> Dict:
        """
        Predict next month's sales
        Returns: {'amount': float, 'confidence': str, 'range': tuple}
        """
        if not self.trained or not self.model:
            return {'error': 'Model not trained'}
        
        monthly_sales = self.model['monthly_sales']
        avg_growth = self.model['avg_growth']
        
        # Last 3 months average
        recent_avg = monthly_sales['total_amount'].tail(3).mean()
        
        # Apply growth rate
        prediction = recent_avg * (1 + avg_growth)
        
        # Calculate confidence interval (±20%)
        lower = prediction * 0.8
        upper = prediction * 1.2
        
        # Determine confidence level
        if self.prediction_accuracy > 80:
            confidence = 'High'
        elif self.prediction_accuracy > 60:
            confidence = 'Medium'
        else:
            confidence = 'Low'
        
        return {
            'amount': round(prediction, 2),
            'confidence': confidence,
            'accuracy': f"{self.prediction_accuracy}%",
            'range': (round(lower, 2), round(upper, 2)),
            'note': f"Based on {len(monthly_sales)} months of data"
        }
    
    def predict_next_n_months(self, n: int = 3) -> List[Dict]:
        """Predict sales for next N months"""
        predictions = []
        
        for month in range(1, n + 1):
            pred = self.predict_next_month()
            if 'error' not in pred:
                pred['month'] = f"Month +{month}"
                predictions.append(pred)
        
        return predictions
    
    def get_trends(self, invoices: List[Dict]) -> Dict:
        """Analyze sales trends"""
        if not invoices:
            return {}
        
        df = pd.DataFrame(invoices)
        df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
        df = df.dropna(subset=['invoice_date', 'total_amount'])
        
        # Monthly aggregation
        df['month'] = df['invoice_date'].dt.to_period('M')
        monthly = df.groupby('month')['total_amount'].sum()
        
        # Calculate trends
        avg_monthly = monthly.mean()
        max_month = monthly.max()
        min_month = monthly.min()
        current_trend = 'increasing' if monthly.tail(3).is_monotonic_increasing else 'decreasing'
        
        return {
            'avg_monthly_sales': round(avg_monthly, 2),
            'best_month': round(max_month, 2),
            'worst_month': round(min_month, 2),
            'current_trend': current_trend,
            'volatility': round(monthly.std(), 2)
        }
    
    @staticmethod
    def _calculate_growth_rate(monthly_sales):
        """Calculate average month-over-month growth rate"""
        if len(monthly_sales) < 2:
            return 0
        
        amounts = monthly_sales['total_amount'].values
        growth_rates = []
        
        for i in range(1, len(amounts)):
            if amounts[i-1] > 0:
                growth = (amounts[i] - amounts[i-1]) / amounts[i-1]
                growth_rates.append(growth)
        
        return np.mean(growth_rates) if growth_rates else 0
    
    @staticmethod
    def _estimate_accuracy(monthly_sales):
        """Estimate prediction accuracy based on data consistency"""
        if len(monthly_sales) < 3:
            return 50
        
        # Calculate coefficient of variation
        amounts = monthly_sales['total_amount'].values
        cv = (np.std(amounts) / np.mean(amounts)) * 100 if np.mean(amounts) > 0 else 100
        
        # Lower CV = higher accuracy
        accuracy = max(50, min(95, 100 - cv))
        
        return round(accuracy, 1)


class ExpenseAnalyzer:
    """Analyze expense patterns and categorize spending"""
    
    @staticmethod
    def categorize_expenses(invoices: List[Dict]) -> Dict:
        """
        Categorize expenses by vendor type
        Returns: {'categories': dict, 'top_vendors': list}
        """
        if not invoices:
            return {}
        
        df = pd.DataFrame(invoices)
        
        # Group by vendor
        if 'client_name' in df.columns and 'total_amount' in df.columns:
            vendor_spending = df.groupby('client_name')['total_amount'].sum().sort_values(ascending=False)
            
            # Top 10 vendors
            top_vendors = [
                {'vendor': vendor, 'amount': round(amount, 2)}
                for vendor, amount in vendor_spending.head(10).items()
            ]
            
            # Simple categorization (can be enhanced with ML)
            total_spending = vendor_spending.sum()
            
            return {
                'total_spending': round(total_spending, 2),
                'unique_vendors': len(vendor_spending),
                'top_vendors': top_vendors,
                'avg_per_vendor': round(vendor_spending.mean(), 2)
            }
        
        return {}
    
    @staticmethod
    def detect_unusual_expenses(invoices: List[Dict], threshold: float = 2.0) -> List[Dict]:
        """
        Detect unusually high or low expenses
        threshold: Number of standard deviations
        """
        if not invoices:
            return []
        
        df = pd.DataFrame(invoices)
        
        if 'total_amount' not in df.columns:
            return []
        
        amounts = df['total_amount'].values
        mean = np.mean(amounts)
        std = np.std(amounts)
        
        unusual = []
        
        for idx, row in df.iterrows():
            amount = row['total_amount']
            z_score = abs((amount - mean) / std) if std > 0 else 0
            
            if z_score > threshold:
                unusual.append({
                    'invoice_number': row.get('invoice_number', 'N/A'),
                    'client': row.get('client_name', 'Unknown'),
                    'amount': amount,
                    'deviation': f"{z_score:.1f}σ",
                    'flag': 'High' if amount > mean else 'Low'
                })
        
        return unusual
