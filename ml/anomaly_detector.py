"""
Anomaly Detection - Find unusual transactions and potential fraud
"""

import pandas as pd
import numpy as np
from typing import List, Dict


class AnomalyDetector:
    """Detect unusual patterns in invoice/expense data"""
    
    def __init__(self, sensitivity: float = 2.5):
        """
        Initialize detector
        sensitivity: Lower = more alerts, Higher = fewer alerts (default 2.5σ)
        """
        self.sensitivity = sensitivity
        self.anomalies_found = []
    
    def detect_invoice_anomalies(self, invoices: List[Dict]) -> List[Dict]:
        """
        Detect anomalies in invoice data
        Returns: List of anomalous invoices with reasons
        """
        if not invoices or len(invoices) < 10:
            return []
        
        df = pd.DataFrame(invoices)
        anomalies = []
        
        # 1. Amount-based anomalies
        anomalies.extend(self._detect_amount_anomalies(df))
        
        # 2. Duplicate detection (same amount, same day, same vendor)
        anomalies.extend(self._detect_duplicates(df))
        
        # 3. Unusually frequent transactions
        anomalies.extend(self._detect_frequency_anomalies(df))
        
        # 4. Round number anomalies (fraud indicator)
        anomalies.extend(self._detect_round_numbers(df))
        
        self.anomalies_found = anomalies
        return anomalies
    
    def _detect_amount_anomalies(self, df) -> List[Dict]:
        """Detect unusually high or low amounts"""
        anomalies = []
        
        if 'total_amount' not in df.columns:
            return anomalies
        
        amounts = df['total_amount'].values
        mean = np.mean(amounts)
        std = np.std(amounts)
        
        for idx, row in df.iterrows():
            amount = row['total_amount']
            
            if std > 0:
                z_score = abs((amount - mean) / std)
                
                if z_score > self.sensitivity:
                    anomalies.append({
                        'invoice_id': row.get('id', idx),
                        'invoice_number': row.get('invoice_number', 'N/A'),
                        'client': row.get('client_name', 'Unknown'),
                        'amount': amount,
                        'type': 'Unusual Amount',
                        'severity': 'High' if z_score > 3 else 'Medium',
                        'reason': f"Amount is {z_score:.1f}σ from average (₹{mean:.2f})",
                        'recommendation': 'Verify transaction details'
                    })
        
        return anomalies
    
    def _detect_duplicates(self, df) -> List[Dict]:
        """Detect potential duplicate transactions"""
        anomalies = []
        
        required_cols = ['total_amount', 'invoice_date', 'client_name']
        if not all(col in df.columns for col in required_cols):
            return anomalies
        
        # Find duplicates
        df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
        
        # Group by amount, date, client
        duplicates = df.groupby(['total_amount', 'invoice_date', 'client_name']).size()
        duplicates = duplicates[duplicates > 1]
        
        for (amount, date, client), count in duplicates.items():
            anomalies.append({
                'invoice_id': 'Multiple',
                'invoice_number': 'Multiple',
                'client': client,
                'amount': amount,
                'type': 'Duplicate Transaction',
                'severity': 'High',
                'reason': f"{count} identical transactions found",
                'recommendation': 'Check for duplicate entries or fraudulent activity'
            })
        
        return anomalies
    
    def _detect_frequency_anomalies(self, df) -> List[Dict]:
        """Detect unusually frequent transactions from same vendor"""
        anomalies = []
        
        if 'client_name' not in df.columns or 'invoice_date' not in df.columns:
            return anomalies
        
        df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
        df['date_only'] = df['invoice_date'].dt.date
        
        # Count transactions per vendor per day
        daily_counts = df.groupby(['client_name', 'date_only']).size()
        
        # Flag if more than 5 transactions from same vendor in one day
        high_frequency = daily_counts[daily_counts > 5]
        
        for (client, date), count in high_frequency.items():
            anomalies.append({
                'invoice_id': 'Multiple',
                'invoice_number': 'Multiple',
                'client': client,
                'amount': 'Various',
                'type': 'High Transaction Frequency',
                'severity': 'Medium',
                'reason': f"{count} transactions on {date}",
                'recommendation': 'Verify if this is expected vendor activity'
            })
        
        return anomalies
    
    def _detect_round_numbers(self, df) -> List[Dict]:
        """Detect suspiciously round numbers (fraud indicator)"""
        anomalies = []
        
        if 'total_amount' not in df.columns:
            return anomalies
        
        # Check for very round numbers (ends with 000)
        for idx, row in df.iterrows():
            amount = row['total_amount']
            
            # Check if ends with 000 and is large
            if amount >= 10000 and amount % 1000 == 0:
                anomalies.append({
                    'invoice_id': row.get('id', idx),
                    'invoice_number': row.get('invoice_number', 'N/A'),
                    'client': row.get('client_name', 'Unknown'),
                    'amount': amount,
                    'type': 'Round Number',
                    'severity': 'Low',
                    'reason': f"Exact round amount: ₹{amount:,.0f}",
                    'recommendation': 'Common pattern, but verify if suspicious'
                })
        
        return anomalies
    
    def get_risk_score(self, invoices: List[Dict]) -> Dict:
        """
        Calculate overall risk score for invoice data
        Returns: {'score': 0-100, 'level': str, 'summary': str}
        """
        anomalies = self.detect_invoice_anomalies(invoices)
        
        if not invoices:
            return {'score': 0, 'level': 'Unknown', 'summary': 'No data'}
        
        # Calculate risk score
        total_invoices = len(invoices)
        anomaly_count = len(anomalies)
        
        # Risk percentage
        risk_percentage = (anomaly_count / total_invoices) * 100 if total_invoices > 0 else 0
        
        # Count high severity
        high_severity = sum(1 for a in anomalies if a.get('severity') == 'High')
        
        # Risk score (0-100, higher = more risk)
        risk_score = min(100, risk_percentage * 5 + high_severity * 10)
        
        # Risk level
        if risk_score < 20:
            level = 'Low'
            color = 'green'
        elif risk_score < 50:
            level = 'Medium'
            color = 'yellow'
        else:
            level = 'High'
            color = 'red'
        
        summary = f"{anomaly_count} anomalies found in {total_invoices} invoices ({high_severity} high-risk)"
        
        return {
            'score': round(risk_score, 1),
            'level': level,
            'color': color,
            'anomaly_count': anomaly_count,
            'high_risk_count': high_severity,
            'summary': summary
        }


class VendorRiskScorer:
    """Score vendor reliability based on payment history"""
    
    @staticmethod
    def score_vendors(invoices: List[Dict]) -> List[Dict]:
        """
        Score each vendor's reliability (0-100)
        Based on: payment delays, invoice amounts, frequency
        """
        if not invoices:
            return []
        
        df = pd.DataFrame(invoices)
        
        required_cols = ['client_name', 'status', 'total_amount']
        if not all(col in df.columns for col in required_cols):
            return []
        
        vendor_scores = []
        
        # Group by vendor
        for vendor, vendor_df in df.groupby('client_name'):
            total_invoices = len(vendor_df)
            total_amount = vendor_df['total_amount'].sum()
            
            # Payment rate (paid / total)
            paid_count = (vendor_df['status'] == 'paid').sum()
            payment_rate = (paid_count / total_invoices * 100) if total_invoices > 0 else 0
            
            # Amount consistency
            amount_std = vendor_df['total_amount'].std()
            amount_mean = vendor_df['total_amount'].mean()
            consistency = (1 - (amount_std / amount_mean)) * 100 if amount_mean > 0 else 50
            consistency = max(0, min(100, consistency))
            
            # Overall score (weighted average)
            risk_score = (payment_rate * 0.6) + (consistency * 0.4)
            
            # Risk level
            if risk_score >= 80:
                risk_level = 'Low Risk'
                color = 'green'
            elif risk_score >= 50:
                risk_level = 'Medium Risk'
                color = 'yellow'
            else:
                risk_level = 'High Risk'
                color = 'red'
            
            vendor_scores.append({
                'vendor': vendor,
                'score': round(risk_score, 1),
                'risk_level': risk_level,
                'color': color,
                'total_invoices': total_invoices,
                'total_amount': round(total_amount, 2),
                'payment_rate': f"{payment_rate:.1f}%",
                'paid_count': paid_count
            })
        
        # Sort by score (ascending = highest risk first)
        vendor_scores.sort(key=lambda x: x['score'])
        
        return vendor_scores
