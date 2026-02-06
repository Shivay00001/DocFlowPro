"""
Business Intelligence - Advanced analytics and insights
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from collections import Counter


class BusinessIntelligence:
    """Generate business insights from invoice/document data"""
    
    @staticmethod
    def generate_dashboard_data(invoices: List[Dict], documents: List[Dict]) -> Dict:
        """
        Generate comprehensive dashboard data
        Returns: Complete BI metrics for dashboard
        """
        if not invoices:
            return {
                'error': 'No invoice data available',
                'revenue': 0,
                'invoices_count': 0
            }
        
        df = pd.DataFrame(invoices)
        
        # Revenue metrics
        total_revenue = df['total_amount'].sum() if 'total_amount' in df.columns else 0
        avg_invoice = df['total_amount'].mean() if 'total_amount' in df.columns else 0
        
        # Status breakdown
        status_counts = df['status'].value_counts().to_dict() if 'status' in df.columns else {}
        
        # Top clients
        top_clients = []
        if 'client_name' in df.columns and 'total_amount' in df.columns:
            client_revenue = df.groupby('client_name')['total_amount'].sum().sort_values(ascending=False).head(5)
            top_clients = [{'name': k, 'amount': v} for k, v in client_revenue.items()]
        
       # Recent activity (last 30 days)
        if 'invoice_date' in df.columns:
            df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
            recent_df = df[df['invoice_date'] >= (datetime.now() - timedelta(days=30))]
            recent_revenue = recent_df['total_amount'].sum()
            recent_count = len(recent_df)
        else:
            recent_revenue = 0
            recent_count = 0
        
        return {
            'total_revenue': round(total_revenue, 2),
            'avg_invoice_value': round(avg_invoice, 2),
            'total_invoices': len(df),
            'total_documents': len(documents) if documents else 0,
            'status_breakdown': status_counts,
            'top_clients': top_clients,
            'recent_30_days': {
                'revenue': round(recent_revenue, 2),
                'count': recent_count
            }
        }
    
    @staticmethod
    def analyze_revenue_trends(invoices: List[Dict]) -> Dict:
        """Analyze revenue trends over time"""
        if not invoices:
            return {}
        
        df = pd.DataFrame(invoices)
        
        if 'invoice_date' not in df.columns or 'total_amount' not in df.columns:
            return {}
        
        df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
        df = df.dropna(subset=['invoice_date'])
        
        # Monthly aggregation
        df['month'] = df['invoice_date'].dt.to_period('M')
        monthly_revenue = df.groupby('month')['total_amount'].sum()
        
        # Calculate growth rate
        if len(monthly_revenue) >= 2:
            current_month = monthly_revenue.iloc[-1]
            previous_month = monthly_revenue.iloc[-2]
            growth_rate = ((current_month - previous_month) / previous_month * 100) if previous_month > 0 else 0
        else:
            growth_rate = 0
        
        # Trend direction
        if len(monthly_revenue) >= 3:
            recent_avg = monthly_revenue.tail(3).mean()
            older_avg = monthly_revenue.head(len(monthly_revenue) - 3).mean() if len(monthly_revenue) > 3 else monthly_revenue.iloc[0]
            trend = 'increasing' if recent_avg > older_avg else 'decreasing'
        else:
            trend = 'stable'
        
        return {
            'monthly_revenue': {str(k): v for k, v in monthly_revenue.items()},
            'growth_rate': round(growth_rate, 2),
            'trend': trend,
            'best_month': {'month': str(monthly_revenue.idxmax()), 'amount': monthly_revenue.max()},
            'worst_month': {'month': str(monthly_revenue.idxmin()), 'amount': monthly_revenue.min()}
        }
    
    @staticmethod
    def client_analytics(invoices: List[Dict]) -> Dict:
        """Analyze client behavior and patterns"""
        if not invoices:
            return {}
        
        df = pd.DataFrame(invoices)
        
        if 'client_name' not in df.columns:
            return {}
        
        client_stats = []
        
        for client, client_df in df.groupby('client_name'):
            total_invoices = len(client_df)
            total_spent = client_df['total_amount'].sum() if 'total_amount' in client_df.columns else 0
            avg_invoice = client_df['total_amount'].mean() if 'total_amount' in client_df.columns else 0
            
            # Payment behavior
            if 'status' in client_df.columns:
                paid_count = (client_df['status'] == 'paid').sum()
                payment_rate = (paid_count / total_invoices * 100) if total_invoices > 0 else 0
            else:
                payment_rate = 0
            
            # Classify client value
            if total_spent >= 100000:
                value_tier = 'Premium'
            elif total_spent >= 50000:
                value_tier = 'High Value'
            elif total_spent >= 10000:
                value_tier = 'Medium Value'
            else:
                value_tier = 'Low Value'
            
            client_stats.append({
                'client': client,
                'total_invoices': total_invoices,
                'total_spent': round(total_spent, 2),
                'avg_invoice': round(avg_invoice, 2),
                'payment_rate': round(payment_rate, 1),
                'value_tier': value_tier
            })
        
        # Sort by total spent
        client_stats.sort(key=lambda x: x['total_spent'], reverse=True)
        
        return {
            'total_clients': len(client_stats),
            'client_details': client_stats,
            'premium_clients': len([c for c in client_stats if c['value_tier'] == 'Premium']),
            'avg_client_value': round(sum(c['total_spent'] for c in client_stats) / len(client_stats), 2) if client_stats else 0
        }
    
    @staticmethod
    def payment_cycle_analysis(invoices: List[Dict]) -> Dict:
        """Analyze payment cycles and delays"""
        if not invoices:
            return {}
        
        df = pd.DataFrame(invoices)
        
        required_cols = ['invoice_date', 'due_date', 'status']
        if not all(col in df.columns for col in required_cols):
            return {}
        
        df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
        df['due_date'] = pd.to_datetime(df['due_date'], errors='coerce')
        
        # Calculate payment delays
        df['days_to_due'] = (df['due_date'] - df['invoice_date']).dt.days
        
        # Paid invoices
        paid_df = df[df['status'] == 'paid']
        
        # Overdue analysis
        today = datetime.now()
        df['overdue'] = (df['due_date'] < today) & (df['status'] != 'paid')
        overdue_count = df['overdue'].sum()
        overdue_amount = df[df['overdue']]['total_amount'].sum() if 'total_amount' in df.columns else 0
        
        return {
            'avg_payment_cycle': round(df['days_to_due'].mean(), 1) if len(df) > 0 else 0,
            'overdue_invoices': int(overdue_count),
            'overdue_amount': round(overdue_amount, 2),
            'on_time_payment_rate': round(len(paid_df) / len(df) * 100, 1) if len(df) > 0 else 0
        }
    
    @staticmethod
    def generate_insights(invoices: List[Dict]) -> List[str]:
        """Generate actionable business insights"""
        insights = []
        
        if not invoices or len(invoices) < 5:
            insights.append("💡 Not enough data for insights. Add more invoices.")
            return insights
        
        df = pd.DataFrame(invoices)
        
        # Revenue insight
        if 'total_amount' in df.columns:
            total_revenue = df['total_amount'].sum()
            avg_invoice = df['total_amount'].mean()
            
            if total_revenue > 100000:
                insights.append(f"🎉 Great job! Total revenue crossed ₹1 Lakh (₹{total_revenue:,.0f})")
            
            if avg_invoice > 10000:
                insights.append(f"💰 High-value transactions! Avg invoice = ₹{avg_invoice:,.0f}")
        
        # Payment insights
        if 'status' in df.columns:
            paid_rate = (df['status'] == 'paid').sum() / len(df) * 100
            
            if paid_rate < 50:
                insights.append(f"⚠️ Low payment rate ({paid_rate:.0f}%). Focus on collections!")
            elif paid_rate > 80:
                insights.append(f"✅ Excellent payment rate ({paid_rate:.0f}%)!")
        
        # Client concentration
        if 'client_name' in df.columns and 'total_amount' in df.columns:
            client_revenue = df.groupby('client_name')['total_amount'].sum()
            top_client_pct = client_revenue.max() / client_revenue.sum() * 100
            
            if top_client_pct > 40:
                insights.append(f"⚠️ Revenue concentrated in one client ({top_client_pct:.0f}%). Diversify!")
        
        # Trend insights
        if 'invoice_date' in df.columns and 'total_amount' in df.columns:
            df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
            df['month'] = df['invoice_date'].dt.to_period('M')
            monthly = df.groupby('month')['total_amount'].sum()
            
            if len(monthly) >= 3:
                recent_trend = monthly.tail(3).is_monotonic_increasing
                if recent_trend:
                    insights.append("📈 Revenue trending up for last 3 months!")
                else:
                    insights.append("📉 Revenue declining. Time to boost sales!")
        
        if not insights:
            insights.append("📊 Business is stable. Keep up the good work!")
        
        return insights
    
    @staticmethod
    def forecast_next_quarter(invoices: List[Dict]) -> Dict:
        """Forecast revenue for next quarter"""
        if not invoices or len(invoices) < 12:
            return {'error': 'Need at least 12 invoices for forecasting'}
        
        df = pd.DataFrame(invoices)
        
        if 'invoice_date' not in df.columns or 'total_amount' not in df.columns:
            return {}
        
        df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
        df['month'] = df['invoice_date'].dt.to_period('M')
        
        monthly_revenue = df.groupby('month')['total_amount'].sum()
        
        # Simple forecast: average of last 3 months × 3
        last_3_avg = monthly_revenue.tail(3).mean()
        forecast = last_3_avg * 3
        
        # Confidence based on volatility
        std = monthly_revenue.tail(6).std()
        cv = (std / last_3_avg * 100) if last_3_avg > 0 else 100
        
        confidence = 'High' if cv < 20 else 'Medium' if cv < 40 else 'Low'
        
        return {
            'forecast_amount': round(forecast, 2),
            'monthly_avg': round(last_3_avg, 2),
            'confidence': confidence,
            'range': (round(forecast * 0.8, 2), round(forecast * 1.2, 2))
        }
