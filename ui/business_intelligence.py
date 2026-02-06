"""
Business Intelligence Dashboard Panel
Advanced analytics and interactive charts
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class BusinessIntelligencePanel(ttk.Frame):
    """BI Dashboard with analytics and insights"""
    
    def __init__(self, parent, engine, user_id):
        super().__init__(parent)
        self.frame = self  # For panel switching compatibility
        self.engine = engine
        self.user_id = user_id
        
        self._create_widgets()
        self._load_analytics()
    
    def _create_widgets(self):
        """Create BI dashboard interface"""
        # Title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        ttk.Label(
            title_frame,
            text="📊 Business Intelligence",
            font=('Helvetica', 16, 'bold')
        ).pack(side='left')
        
        ttk.Button(
            title_frame,
            text="🔄 Refresh",
            command=self._load_analytics
        ).pack(side='right')
        
        # Main content with scrollbar
        canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True, padx=(20, 0), pady=(0, 20))
        scrollbar.pack(side='right', fill='y', pady=(0, 20), padx=(0, 20))
        
        self.content_frame = scrollable_frame
        
    def _load_analytics(self):
        """Load and display analytics"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        try:
            from analytics.business_intel import BusinessIntelligence
            
            invoices = self.engine.get_my_invoices()
            documents = self.engine.get_my_documents()
            
            if not invoices:
                self._show_empty_state()
                return
            
            bi = BusinessIntelligence()
            
            # Dashboard metrics
            dashboard_data = bi.generate_dashboard_data(invoices, documents)
            self._show_dashboard(dashboard_data)
            
            # Revenue trends
            trends = bi.analyze_revenue_trends(invoices)
            self._show_trends(trends)
            
            # Client analytics
            clients = bi.client_analytics(invoices)
            self._show_clients(clients)
            
            # Insights
            insights = bi.generate_insights(invoices)
            self._show_insights(insights)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load analytics: {str(e)}")
    
    def _show_empty_state(self):
        """Show when no data available"""
        frame = ttk.LabelFrame(self.content_frame, text="No Data", padding=20)
        frame.pack(fill='x', pady=10)
        
        ttk.Label(
            frame,
            text="📭 No invoice data available.\n\nCreate some invoices to see analytics.",
            font=('Helvetica', 10),
            foreground='#666'
        ).pack()
    
    def _show_dashboard(self, data):
        """Show dashboard metrics"""
        frame = ttk.LabelFrame(self.content_frame, text="📈 Key Metrics", padding=15)
        frame.pack(fill='x', pady=(0, 15))
        
        metrics = [
            ("Total Revenue", f"₹{data['total_revenue']:,.2f}", "green"),
            ("Total Invoices", str(data['total_invoices']), "blue"),
            ("Avg Invoice Value", f"₹{data['avg_invoice_value']:,.2f}", "orange"),
            ("Total Documents", str(data['total_documents']), "purple")
        ]
        
        for idx, (label, value, color) in enumerate(metrics):
            metric_frame = ttk.Frame(frame)
            metric_frame.grid(row=idx//2, column=idx%2, sticky='ew', padx=10, pady=5)
            
            ttk.Label(metric_frame, text=label, font=('Helvetica', 9)).pack(anchor='w')
            ttk.Label(
                metric_frame,
                text=value,
                font=('Helvetica', 14, 'bold'),
                foreground=color
            ).pack(anchor='w')
        
        # Configure grid
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
    
    def _show_trends(self, trends):
        """Show revenue trends"""
        if not trends:
            return
        
        frame = ttk.LabelFrame(self.content_frame, text="📊 Revenue Trends", padding=15)
        frame.pack(fill='x', pady=(0, 15))
        
        # Growth rate
        growth = trends.get('growth_rate', 0)
        growth_color = 'green' if growth > 0 else 'red'
        growth_icon = '📈' if growth > 0 else '📉'
        
        ttk.Label(
            frame,
            text=f"{growth_icon} Growth Rate: {growth:.1f}%",
            font=('Helvetica', 12, 'bold'),
            foreground=growth_color
        ).pack(anchor='w', pady=(0, 10))
        
        # Trend
        trend = trends.get('trend', 'stable')
        ttk.Label(
            frame,
            text=f"Trend: {trend.title()}",
            font=('Helvetica', 10)
        ).pack(anchor='w')
        
        # Best/worst months
        if 'best_month' in trends:
            best = trends['best_month']
            ttk.Label(
                frame,
                text=f"🏆 Best Month: {best['month']} (₹{best['amount']:,.2f})",
                foreground='green'
            ).pack(anchor='w', pady=(5, 0))
    
    def _show_clients(self, clients):
        """Show client analytics"""
        if not clients or not clients.get('client_details'):
            return
        
        frame = ttk.LabelFrame(self.content_frame, text="👥 Top Clients", padding=15)
        frame.pack(fill='x', pady=(0, 15))
        
        # Top 5 clients
        for client in clients['client_details'][:5]:
            client_frame = ttk.Frame(frame)
            client_frame.pack(fill='x', pady=2)
            
            ttk.Label(
                client_frame,
                text=client['client'],
                font=('Helvetica', 10, 'bold')
            ).pack(side='left')
            
            ttk.Label(
                client_frame,
                text=f"₹{client['total_spent']:,.2f}",
                foreground='green'
            ).pack(side='right')
            
            ttk.Label(
                client_frame,
                text=f"({client['value_tier']})",
                foreground='#666'
            ).pack(side='right', padx=(5, 10))
    
    def _show_insights(self, insights):
        """Show business insights"""
        frame = ttk.LabelFrame(self.content_frame, text="💡 Business Insights", padding=15)
        frame.pack(fill='x', pady=(0, 15))
        
        for insight in insights:
            ttk.Label(
                frame,
                text=insight,
                font=('Helvetica', 10),
                wraplength=600
            ).pack(anchor='w', pady=2)
    
    def refresh(self):
        """Refresh analytics"""
        self._load_analytics()
