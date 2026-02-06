"""
Expense Categorization - Auto-classify expenses using ML
"""

import pandas as pd
from typing import List, Dict
from collections import Counter


class ExpenseCategorizer:
    """Automatically categorize expenses into business categories"""
    
    # Pre-defined categories with keywords
    CATEGORIES = {
        'Office Supplies': ['stationery', 'paper', 'pen', 'printer', 'ink', 'toner', 'supplies'],
        'Utilities': ['electricity', 'water', 'internet', 'phone', 'mobile', 'broadband', 'wifi'],
        'Rent': ['rent', 'lease', 'rental', 'office space'],
        'Salary & Wages': ['salary', 'wages', 'payroll', 'employee', 'staff'],
        'Travel': ['travel', 'flight', 'hotel', 'taxi', 'uber', 'ola', 'transport'],
        'Marketing': ['advertising', 'marketing', 'promotion', 'social media', 'ads', 'google ads'],
        'Software': ['software', 'saas', 'subscription', 'license', 'app', 'cloud'],
        'Professional Fees': ['consultant', 'lawyer', 'accountant', 'ca', 'professional', 'audit'],
        'Equipment': ['computer', 'laptop', 'furniture', 'equipment', 'machinery'],
        'Maintenance': ['repair', 'maintenance', 'service', 'cleaning'],
        'Raw Materials': ['raw material', 'inventory', 'stock', 'material', 'goods'],
        'Insurance': ['insurance', 'policy', 'premium'],
        'Banking': ['bank', 'interest', 'charges', 'fees'],
        'Miscellaneous': []  # Default category
    }
    
    def __init__(self):
        self.trained_keywords = self.CATEGORIES.copy()
    
    def categorize_invoice(self, invoice: Dict) -> str:
        """
        Categorize a single invoice
        Returns: category name
        """
        # Get relevant text fields
        text_fields = [
            invoice.get('client_name', ''),
            invoice.get('description', ''),
            invoice.get('notes', ''),
            str(invoice.get('items', ''))
        ]
        
        combined_text = ' '.join(text_fields).lower()
        
        # Check each category's keywords
        scores = {}
        
        for category, keywords in self.CATEGORIES.items():
            if category == 'Miscellaneous':
                scores[category] = 0
                continue
            
            # Count keyword matches
            matches = sum(1 for keyword in keywords if keyword in combined_text)
            scores[category] = matches
        
        # Return category with highest score
        best_category = max(scores, key=scores.get)
        
        # If no matches, return Miscellaneous
        if scores[best_category] == 0:
            return 'Miscellaneous'
        
        return best_category
    
    def categorize_batch(self, invoices: List[Dict]) -> Dict:
        """
        Categorize multiple invoices
        Returns: {'categorized': list, 'summary': dict}
        """
        categorized = []
        category_counts = Counter()
        category_amounts = Counter()
        
        for invoice in invoices:
            category = self.categorize_invoice(invoice)
            
            categorized.append({
                'invoice_number': invoice.get('invoice_number', 'N/A'),
                'client': invoice.get('client_name', 'Unknown'),
                'amount': invoice.get('total_amount', 0),
                'category': category,
                'date': invoice.get('invoice_date', 'N/A')
            })
            
            category_counts[category] += 1
            category_amounts[category] += invoice.get('total_amount', 0)
        
        # Create summary
        summary = []
        for category in sorted(category_counts.keys()):
            summary.append({
                'category': category,
                'count': category_counts[category],
                'total_amount': round(category_amounts[category], 2),
                'percentage': round(category_counts[category] / len(invoices) * 100, 1) if invoices else 0
            })
        
        # Sort by amount (descending)
        summary.sort(key=lambda x: x['total_amount'], reverse=True)
        
        return {
            'categorized': categorized,
            'summary': summary,
            'total_invoices': len(invoices),
            'total_categories': len([s for s in summary if s['count'] > 0])
        }
    
    def get_spending_breakdown(self, invoices: List[Dict]) -> Dict:
        """
        Get detailed spending breakdown by category
        Returns: pie chart data
        """
        result = self.categorize_batch(invoices)
        summary = result['summary']
        
        # Filter out zero amounts
        summary = [s for s in summary if s['total_amount'] > 0]
        
        return {
            'labels': [s['category'] for s in summary],
            'amounts': [s['total_amount'] for s in summary],
            'percentages': [s['percentage'] for s in summary],
            'total': sum(s['total_amount'] for s in summary)
        }
    
    def suggest_category(self, vendor_name: str) -> str:
        """Suggest category based on vendor name"""
        invoice_stub = {'client_name': vendor_name}
        return self.categorize_invoice(invoice_stub)
    
    def train_from_user_labels(self, labeled_data: List[Dict]):
        """
        Learn from user-provided labels
        labeled_data: [{'invoice': dict, 'category': str}, ...]
        """
        # Extract keywords from labeled invoices
        for item in labeled_data:
            invoice = item['invoice']
            category = item['category']
            
            if category not in self.trained_keywords:
                self.trained_keywords[category] = []
            
            # Extract potential keywords from client name
            client_name = invoice.get('client_name', '').lower()
            words = client_name.split()
            
            # Add new keywords
            for word in words:
                if len(word) > 3 and word not in self.trained_keywords[category]:
                    self.trained_keywords[category].append(word)


class SmartInvoiceClassifier:
    """Advanced classification using invoice patterns"""
    
    @staticmethod
    def classify_by_amount_range(invoices: List[Dict]) -> Dict:
        """Classify invoices into amount ranges"""
        if not invoices:
            return {}
        
        df = pd.DataFrame(invoices)
        
        if 'total_amount' not in df.columns:
            return {}
        
        # Define ranges
        ranges = {
            'Micro (₹0-1k)': (0, 1000),
            'Small (₹1k-10k)': (1000, 10000),
            'Medium (₹10k-50k)': (10000, 50000),
            'Large (₹50k-1L)': (50000, 100000),
            'Enterprise (₹1L+)': (100000, float('inf'))
        }
        
        classification = {}
        
        for range_name, (min_amt, max_amt) in ranges.items():
            in_range = df[(df['total_amount'] >= min_amt) & (df['total_amount'] < max_amt)]
            classification[range_name] = {
                'count': len(in_range),
                'total_amount': round(in_range['total_amount'].sum(), 2),
                'avg_amount': round(in_range['total_amount'].mean(), 2) if len(in_range) > 0 else 0
            }
        
        return classification
    
    @staticmethod
    def classify_by_payment_status(invoices: List[Dict]) -> Dict:
        """Classify by payment status"""
        if not invoices:
            return {}
        
        df = pd.DataFrame(invoices)
        
        if 'status' not in df.columns or 'total_amount' not in df.columns:
            return {}
        
        status_summary = {}
        
        for status in df['status'].unique():
            status_invoices = df[df['status'] == status]
            status_summary[status.upper()] = {
                'count': len(status_invoices),
                'total_amount': round(status_invoices['total_amount'].sum(), 2),
                'avg_amount': round(status_invoices['total_amount'].mean(), 2)
            }
        
        return status_summary
