"""
Regulatory Helper - GST, TDS, Compliance reports
"""

from datetime import datetime
from typing import List, Dict
import pandas as pd


class RegulatoryHelper:
    """Helper for GST filing, TDS, and compliance"""
    
    @staticmethod
    def generate_gst_report(invoices: List[Dict], month: str = None) -> Dict:
        """
        Generate GST report for filing
        month: 'YYYY-MM' format, defaults to current month
        """
        if not invoices:
            return {'error': 'No invoice data'}
        
        df = pd.DataFrame(invoices)
        
        # Filter by month if specified
        if month and 'invoice_date' in df.columns:
            df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
            df['month'] = df['invoice_date'].dt.to_period('M')
            df = df[df['month'] == month]
        
        # Calculate GST components
        if 'tax_rate' not in df.columns or 'tax_amount' not in df.columns:
            # Assume 18% GST if not specified
            df['tax_amount'] = df.get('total_amount', 0) * 0.18 / 1.18
        
        total_taxable = df.get('subtotal', df.get('total_amount', 0) - df['tax_amount']).sum()
        total_gst = df['tax_amount'].sum()
        
        # CGST + SGST (for intra-state) or IGST (for inter-state)
        cgst = total_gst / 2
        sgst = total_gst / 2
        
        return {
            'period': month or datetime.now().strftime('%Y-%m'),
            'total_invoices': len(df),
            'taxable_amount': round(total_taxable, 2),
            'total_gst': round(total_gst, 2),
            'cgst': round(cgst, 2),
            'sgst': round(sgst, 2),
            'total_with_tax': round(df.get('total_amount', 0).sum(), 2)
        }
    
    @staticmethod
    def gst_filing_checklist() -> List[str]:
        """GST filing checklist"""
        return [
            "✓ Collect all tax invoices for the month",
            "✓ Verify GST numbers of all clients",
            "✓ Match invoice totals with bank statements",
            "✓ Calculate CGST, SGST, IGST",
            "✓ File GSTR-1 (outward supplies)",
            "✓ File GSTR-3B (summary return)",
            "✓ Pay GST liability before deadline",
            "✓ Download acknowledgment receipts"
        ]
    
    @staticmethod
    def calculate_tds(invoice_amount: float, rate: float = 2.0) -> Dict:
        """Calculate TDS on professional fees"""
        tds_amount = invoice_amount * (rate / 100)
        net_payable = invoice_amount - tds_amount
        
        return {
            'gross_amount': round(invoice_amount, 2),
            'tds_rate': f"{rate}%",
            'tds_amount': round(tds_amount, 2),
            'net_payable': round(net_payable, 2),
            'note': 'TDS to be deposited with Form 26AS'
        }
    
    @staticmethod
    def audit_trail_report(audit_logs: List[Dict], start_date: str = None, end_date: str = None) -> Dict:
        """Generate audit trail report for compliance"""
        if not audit_logs:
            return {'error': 'No audit data'}
        
        df = pd.DataFrame(audit_logs)
        
        # Filter by date range if specified
        if start_date and end_date and 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
            df = df[(df['created_at'] >= start_date) & (df['created_at'] <= end_date)]
        
        # Action summary
        action_counts = df['action'].value_counts().to_dict() if 'action' in df.columns else {}
        
        # User activity
        user_activity = df['user_id'].value_counts().to_dict() if 'user_id' in df.columns else {}
        
        return {
            'total_actions': len(df),
            'date_range': {
                'start': start_date or 'All time',
                'end': end_date or datetime.now().strftime('%Y-%m-%d')
            },
            'action_breakdown': action_counts,
            'user_activity': user_activity,
            'compliance_status': 'Complete' if len(df) > 0 else 'Incomplete'
        }
    
    @staticmethod
    def income_tax_summary(invoices: List[Dict], financial_year: str = None) -> Dict:
        """Generate income tax summary"""
        if not invoices:
            return {}
        
        df = pd.DataFrame(invoices)
        
        # Filter by financial year (Apr-Mar)
        if financial_year and 'invoice_date' in df.columns:
            # FY 2023-24 means Apr 2023 to Mar 2024
            pass  # Implement FY filtering
        
        total_income = df.get('total_amount', 0).sum()
        
        return {
            'financial_year': financial_year or datetime.now().strftime('%Y'),
            'total_revenue': round(total_income, 2),
            'total_invoices': len(df),
            'avg_revenue': round(total_income / len(df), 2) if len(df) > 0 else 0,
            'note': 'Verify with P&L statement before filing'
        }


class ComplianceChecker:
    """Check compliance requirements"""
    
    @staticmethod
    def check_invoice_compliance(invoice: Dict) -> Dict:
        """Check if invoice meets legal requirements"""
        issues = []
        
        # Required fields
        required_fields = ['invoice_number', 'invoice_date', 'client_name', 'total_amount']
        
        for field in required_fields:
            if not invoice.get(field):
                issues.append(f"Missing {field}")
        
        # GST number check (if amount > 50k)
        if invoice.get('total_amount', 0) > 50000:
            if not invoice.get('client_gst'):
                issues.append("GST number required for amounts > ₹50,000")
        
        # PAN check (if amount > 50k)
        if invoice.get('total_amount', 0) > 50000:
            if not invoice.get('client_pan'):
                issues.append("PAN required for amounts > ₹50,000")
        
        # Compliance status
        if not issues:
            status = 'Compliant'
            color = 'green'
        elif len(issues) <= 2:
            status = 'Minor Issues'
            color = 'yellow'
        else:
            status = 'Non-Compliant'
            color = 'red'
        
        return {
            'status': status,
            'color': color,
            'issues': issues,
            'issue_count': len(issues)
        }
    
    @staticmethod
    def data_retention_check(documents: List[Dict], retention_years: int = 7) -> Dict:
        """Check if documents meet retention requirements"""
        if not documents:
            return {}
        
        df = pd.DataFrame(documents)
        
        if 'created_at' not in df.columns:
            return {}
        
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        cutoff_date = datetime.now().replace(year=datetime.now().year - retention_years)
        
        old_docs = df[df['created_at'] < cutoff_date]
        
        return {
            'total_documents': len(df),
            'old_documents': len(old_docs),
            'retention_years': retention_years,
            'compliance': 'OK' if len(old_docs) == 0 else f"{len(old_docs)} documents can be archived",
            'oldest_document': df['created_at'].min().strftime('%Y-%m-%d') if len(df) > 0 else 'N/A'
        }
