"""
Dashboard Panel for DocFlow Pro
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime


class DashboardPanel(ttk.Frame):
    """Main dashboard with statistics and quick actions"""
    
    def __init__(self, parent, engine, user_id):
        super().__init__(parent)
        self.frame = self  # For panel switching compatibility
        self.engine = engine
        self.user_id = user_id
        
        self._create_widgets()
        self._load_statistics()
    
    def _create_widgets(self):
        """Create dashboard widgets"""
        # Title
        title_label = ttk.Label(
            self,
            text="Dashboard",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(padx=20, pady=(20, 10), anchor='w')
        
        # Statistics frame
        stats_frame = ttk.Frame(self)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Document count card
        doc_card = self._create_stat_card(
            stats_frame,
            "Documents",
            "0",
            "#1a237e"
        )
        doc_card.pack(side='left', padx=10, fill='both', expand=True)
        self.doc_count_label = doc_card.winfo_children()[1]
        
        # Invoice count card
        inv_card = self._create_stat_card(
            stats_frame,
            "Invoices",
            "0",
            "#283593"
        )
        inv_card.pack(side='left', padx=10, fill='both', expand=True)
        self.inv_count_label = inv_card.winfo_children()[1]
        
        # Revenue card
        rev_card = self._create_stat_card(
            stats_frame,
            "Total Revenue",
            "₹0.00",
            "#4caf50"
        )
        rev_card.pack(side='left', padx=10, fill='both', expand=True)
        self.rev_label = rev_card.winfo_children()[1]
        
        # Recent activity
        activity_frame = ttk.LabelFrame(self, text="Recent Activity", padding=15)
        activity_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.activity_text = tk.Text(
            activity_frame,
            height=15,
            width=80,
            wrap='word',
            font=('Courier', 9)
        )
        self.activity_text.pack(fill='both', expand=True)
    
    def _create_stat_card(self, parent, title, value, color):
        """Create a statistics card"""
        card = ttk.Frame(parent, relief='solid', borderwidth=1)
        
        title_label = ttk.Label(
            card,
            text=title,
            font=('Helvetica', 10),
            foreground='#666'
        )
        title_label.pack(pady=(10, 5))
        
        value_label = ttk.Label(
            card,
            text=value,
            font=('Helvetica', 20, 'bold'),
            foreground=color
        )
        value_label.pack(pady=(0, 10))
        
        return card
    
    def _load_statistics(self):
        """Load user statistics"""
        try:
            stats = self.engine.get_my_statistics()
            
            # Update counts
            self.doc_count_label.config(text=str(stats.get('total_documents', 0)))
            self.inv_count_label.config(text=str(stats.get('total_invoices', 0)))
            self.rev_label.config(text=f"₹{stats.get('total_revenue', 0):.2f}")
            
            # Show recent activity
            self.activity_text.delete('1.0', 'end')
            
            recent_activity = stats.get('recent_activity', [])
            if recent_activity:
                for activity in recent_activity[:10]:
                    action = activity.get('action', '')
                    details = activity.get('details', '')
                    created = activity.get('created_at', '')[:19]
                    
                    self.activity_text.insert('end', f"[{created}] {action}\n")
                    if details:
                        self.activity_text.insert('end', f"  {details}\n")
                    self.activity_text.insert('end', "\n")
            else:
                self.activity_text.insert('end', "No recent activity")
                
        except Exception as e:
            print(f"Error loading statistics: {e}")
    
    def refresh(self):
        """Refresh dashboard data"""
        self._load_statistics()
