"""
Data Cleaner - Auto clean messy invoice/document data
"""

import pandas as pd
from datetime import datetime
import re


class DataCleaner:
    """Automatically clean and standardize business data"""
    
    def __init__(self):
        self.cleaning_stats = {
            'duplicates_removed': 0,
            'missing_filled': 0,
            'formats_fixed': 0,
            'invalid_removed': 0
        }
    
    def clean_invoices(self, invoices: list) -> tuple:
        """
        Clean invoice data
        Returns: (cleaned_invoices, cleaning_report)
        """
        if not invoices:
            return [], self.cleaning_stats
        
        # Convert to DataFrame for easier processing
        df = pd.DataFrame(invoices)
        original_count = len(df)
        
        # 1. Remove duplicates
        df = self._remove_duplicates(df)
        
        # 2. Fix missing values
        df = self._fix_missing_values(df)
        
        # 3. Standardize formats
        df = self._standardize_formats(df)
        
        # 4. Validate data
        df = self._validate_data(df)
        
        # Convert back to list of dicts
        cleaned = df.to_dict('records')
        
        return cleaned, self.cleaning_stats
    
    def _remove_duplicates(self, df):
        """Remove duplicate invoices"""
        before = len(df)
        
        # Remove duplicates based on invoice_number
        if 'invoice_number' in df.columns:
            df = df.drop_duplicates(subset=['invoice_number'], keep='first')
        
        self.cleaning_stats['duplicates_removed'] = before - len(df)
        return df
    
    def _fix_missing_values(self, df):
        """Fill missing values intelligently"""
        missing_count = 0
        
        # Fix missing client names
        if 'client_name' in df.columns:
            missing = df['client_name'].isna().sum()
            df['client_name'] = df['client_name'].fillna('Unknown Client')  # Fixed: removed inplace
            missing_count += missing
        
        # Fix missing amounts (set to 0)
        if 'total_amount' in df.columns:
            missing = df['total_amount'].isna().sum()
            df['total_amount'] = df['total_amount'].fillna(0)  # Fixed: removed inplace
            missing_count += missing
        
        # Fix missing status
        if 'status' in df.columns:
            missing = df['status'].isna().sum()
            df['status'] = df['status'].fillna('pending')  # Fixed: removed inplace
            missing_count += missing
        
        self.cleaning_stats['missing_filled'] = missing_count
        return df
    
    def _standardize_formats(self, df):
        """Standardize date, phone, GST number formats"""
        format_count = 0
        
        # Standardize dates
        if 'invoice_date' in df.columns:
            df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
            df['invoice_date'] = df['invoice_date'].dt.strftime('%Y-%m-%d')
            format_count += len(df)
        
        # Standardize phone numbers (remove spaces, dashes)
        if 'client_phone' in df.columns:
            df['client_phone'] = df['client_phone'].apply(self._clean_phone)
            format_count += len(df)
        
        # Standardize GST numbers
        if 'gst_number' in df.columns:
            df['gst_number'] = df['gst_number'].apply(self._clean_gst)
            format_count += len(df)
        
        self.cleaning_stats['formats_fixed'] = format_count
        return df
    
    def _validate_data(self, df):
        """Remove invalid records"""
        before = len(df)
        
        # Remove invoices with zero or negative amounts
        if 'total_amount' in df.columns:
            df = df[df['total_amount'] > 0]
        
        # Remove invoices without invoice number
        if 'invoice_number' in df.columns:
            df = df[df['invoice_number'].notna()]
            df = df[df['invoice_number'] != '']
        
        self.cleaning_stats['invalid_removed'] = before - len(df)
        return df
    
    @staticmethod
    def _clean_phone(phone):
        """Clean phone number format"""
        if pd.isna(phone):
            return ''
        phone = str(phone)
        # Remove all non-digits
        phone = re.sub(r'\D', '', phone)
        # Keep last 10 digits
        return phone[-10:] if len(phone) >= 10 else phone
    
    @staticmethod
    def _clean_gst(gst):
        """Clean GST number format"""
        if pd.isna(gst):
            return ''
        gst = str(gst).upper()
        # Remove spaces and special characters
        gst = re.sub(r'[^A-Z0-9]', '', gst)
        return gst
    
    def get_cleaning_report(self) -> str:
        """Generate human-readable cleaning report"""
        report = f"""
Data Cleaning Report:
═══════════════════════

✓ Duplicates Removed: {self.cleaning_stats['duplicates_removed']}
✓ Missing Values Fixed: {self.cleaning_stats['missing_filled']}
✓ Formats Standardized: {self.cleaning_stats['formats_fixed']}
✓ Invalid Records Removed: {self.cleaning_stats['invalid_removed']}

Total Improvements: {sum(self.cleaning_stats.values())}
        """
        return report.strip()


class DataQualityScorer:
    """Score data quality (0-100)"""
    
    @staticmethod
    def score_invoice_data(invoices: list) -> dict:
        """
        Calculate data quality score
        Returns: {'score': int, 'issues': list}
        """
        if not invoices:
            return {'score': 0, 'issues': ['No data']}
        
        df = pd.DataFrame(invoices)
        total_score = 100
        issues = []
        
        # Check for duplicates (-20 points)
        if 'invoice_number' in df.columns:
            duplicates = df['invoice_number'].duplicated().sum()
            if duplicates > 0:
                total_score -= min(20, duplicates * 2)
                issues.append(f"{duplicates} duplicate invoices")
        
        # Check for missing values (-15 points each field)
        critical_fields = ['invoice_number', 'client_name', 'total_amount', 'invoice_date']
        for field in critical_fields:
            if field in df.columns:
                missing = df[field].isna().sum()
                if missing > 0:
                    total_score -= min(15, missing)
                    issues.append(f"{missing} missing {field}")
        
        # Check for invalid amounts (-10 points)
        if 'total_amount' in df.columns:
            invalid = (df['total_amount'] <= 0).sum()
            if invalid > 0:
                total_score -= min(10, invalid * 2)
                issues.append(f"{invalid} invalid amounts")
        
        # Ensure score is 0-100
        total_score = max(0, min(100, total_score))
        
        if not issues:
            issues = ['Data quality excellent!']
        
        return {
            'score': total_score,
            'issues': issues,
            'grade': 'A' if total_score >= 90 else 'B' if total_score >= 75 else 'C' if total_score >= 60 else 'D'
        }
