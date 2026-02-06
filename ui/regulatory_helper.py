"""
Enhanced Regulatory Helper with Interactive GST Filing
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
import os


class RegulatoryHelperPanel(ttk.Frame):
    """Enhanced regulatory compliance and GST filing assistant"""
    
    def __init__(self, parent, engine, user_id):
        super().__init__(parent)
        self.frame = self  # For panel switching compatibility
        self.engine = engine
        self.user_id = user_id
        
        # GST checklist status
        self.checklist_status = self._load_checklist_status()
        
        self._create_widgets()
    
    def _load_checklist_status(self):
        """Load GST checklist status from file"""
        try:
            if os.path.exists('gst_checklist.json'):
                with open('gst_checklist.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'collect_invoices': False,
            'verify_gst': False,
            'match_bank': False,
            'calculate_tax': False,
            'file_gstr1': False,
            'file_gstr3b': False,
            'pay_liability': False,
            'download_ack': False
        }
    
    def _save_checklist_status(self):
        """Save GST checklist status"""
        try:
            with open('gst_checklist.json', 'w') as f:
                json.dump(self.checklist_status, f, indent=2)
        except:
            pass
    
    def _create_widgets(self):
        """Create regulatory helper interface"""
        # Header
        header = tk.Frame(self, bg='white', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📚 GST Compliance & Filing Assistant",
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg='#333'
        ).pack(side='left', padx=20, pady=20)
        
        # Main content
        content = tk.Frame(self, bg='#f5f7fa')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Tabs
        notebook = ttk.Notebook(content)
        notebook.pack(fill='both', expand=True)
        
        # Tab 1: GST Filing Checklist
        checklist_tab = self._create_checklist_tab(notebook)
        notebook.add(checklist_tab, text='📋 Filing Checklist')
        
        # Tab 2: Client GST Verification
        verification_tab = self._create_verification_tab(notebook)
        notebook.add(verification_tab, text='✓ GST Verification')
        
        # Tab 3: Tax Calculation
        calculation_tab = self._create_calculation_tab(notebook)
        notebook.add(calculation_tab, text='🧮 Tax Calculator')
        
        # Tab 4: Reports
        reports_tab = self._create_reports_tab(notebook)
        notebook.add(reports_tab, text='📊 Reports')
    
    def _create_checklist_tab(self, parent):
        """Create interactive GST filing checklist"""
        tab = tk.Frame(parent, bg='white')
        
        tk.Label(
            tab,
            text="GST Filing Checklist - Track Your Progress",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#333'
        ).pack(pady=15)
        
        # Checklist items
        checklist_items = [
            ('collect_invoices', '✓ Collect all tax invoices for the month', self._collect_invoices),
            ('verify_gst', '✓ Verify GST numbers of all clients', self._verify_gst_numbers),
            ('match_bank', '✓ Match invoice totals with bank statements', self._match_bank_statements),
            ('calculate_tax', '✓ Calculate CGST, SGST, IGST', self._calculate_taxes),
            ('file_gstr1', '✓ File GSTR-1 (outward supplies)', self._file_gstr1),
            ('file_gstr3b', '✓ File GSTR-3B (summary return)', self._file_gstr3b),
            ('pay_liability', '✓ Pay GST liability before deadline', self._pay_liability),
            ('download_ack', '✓ Download acknowledgment receipts', self._download_acknowledgments)
        ]
        
        self.checklist_vars = {}
        
        for key, text, command in checklist_items:
            item_frame = tk.Frame(tab, bg='white')
            item_frame.pack(fill='x', padx=30, pady=5)
            
            # Checkbox
            var = tk.BooleanVar(value=self.checklist_status.get(key, False))
            self.checklist_vars[key] = var
            
            check = tk.Checkbutton(
                item_frame,
                variable=var,
                bg='white',
                command=lambda k=key: self._update_checklist(k)
            )
            check.pack(side='left')
            
            # Label
            tk.Label(
                item_frame,
                text=text,
                font=('Segoe UI', 11),
                bg='white',
                fg='#333'
            ).pack(side='left', padx=5)
            
            # Action button
            tk.Button(
                item_frame,
                text="▶ Start",
                font=('Segoe UI', 9),
                bg='#2196f3',
                fg='white',
                relief='flat',
                cursor='hand2',
                padx=10,
                pady=3,
                command=command
            ).pack(side='right')
        
        # Progress bar
        progress_frame = tk.Frame(tab, bg='white')
        progress_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Label(
            progress_frame,
            text="Overall Progress:",
            font=('Segoe UI', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', pady=5)
        
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            length=500,
            mode='determinate',
            variable=self.progress_var
        )
        self.progress_bar.pack(fill='x', pady=5)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="0% Complete",
            font=('Segoe UI', 10),
            bg='white',
            fg='#666'
        )
        self.progress_label.pack()
        
        self._update_progress()
        
        return tab
    
    def _create_verification_tab(self, parent):
        """Create GST verification tab"""
        tab = tk.Frame(parent, bg='white')
        
        tk.Label(
            tab,
            text="Client GST Verification",
            font=('Segoe UI', 14, 'bold'),
            bg='white'
        ).pack(pady=15)
        
        tk.Button(
            tab,
            text="🔍 Verify All Client GST Numbers",
            font=('Segoe UI', 12),
            bg='#4caf50',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10,
            command=self._verify_all_gst
        ).pack(pady=10)
        
        # Results
        tk.Label(
            tab,
            text="Verification Results:",
            font=('Segoe UI', 11, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=20, pady=(20, 5))
        
        self.verification_text = tk.Text(
            tab,
            height=15,
            width=70,
            font=('Courier', 9),
            wrap='word'
        )
        self.verification_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        return tab
    
    def _create_calculation_tab(self, parent):
        """Create tax calculation tab"""
        tab = tk.Frame(parent, bg='white')
        
        tk.Label(
            tab,
            text="CGST, SGST, IGST Calculator",
            font=('Segoe UI', 14, 'bold'),
            bg='white'
        ).pack(pady=15)
        
        # Input fields
        input_frame = tk.Frame(tab, bg='white')
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Month (YYYY-MM):", bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.month_entry = tk.Entry(input_frame, width=20)
        self.month_entry.insert(0, datetime.now().strftime('%Y-%m'))
        self.month_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(
            tab,
            text="🧮 Calculate Taxes for Month",
            font=('Segoe UI', 11),
            bg='#ff9800',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8,
            command=self._calculate_month_taxes
        ).pack(pady=10)
        
        # Results
        self.tax_results_text = tk.Text(
            tab,
            height=12,
            width=70,
            font=('Courier', 10),
            wrap='word'
        )
        self.tax_results_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        return tab
    
    def _create_reports_tab(self, parent):
        """Create reports tab"""
        tab = tk.Frame(parent, bg='white')
        
        tk.Label(
            tab,
            text="GST Reports & Downloads",
            font=('Segoe UI', 14, 'bold'),
            bg='white'
        ).pack(pady=15)
        
        buttons = [
            ("📄 Generate GSTR-1 Summary", self._generate_gstr1_summary),
            ("📄 Generate GSTR-3B Summary", self._generate_gstr3b_summary),
            ("💾 Export Complete GST Report", self._export_gst_report),
            ("📋 View Filing History", self._view_filing_history)
        ]
        
        for text, command in buttons:
            tk.Button(
                tab,
                text=text,
                font=('Segoe UI', 11),
                bg='#673ab7',
                fg='white',
                relief='flat',
                cursor='hand2',
                width=35,
                pady=8,
                command=command
            ).pack(pady=5)
        
        return tab
    
    def _update_checklist(self, key):
        """Update checklist status"""
        self.checklist_status[key] = self.checklist_vars[key].get()
        self._save_checklist_status()
        self._update_progress()
    
    def _update_progress(self):
        """Update progress bar"""
        completed = sum(1 for v in self.checklist_status.values() if v)
        total = len(self.checklist_status)
        percentage = int((completed / total) * 100)
        
        self.progress_var.set(percentage)
        self.progress_label.config(text=f"{percentage}% Complete ({completed}/{total} tasks)")
    
    def _collect_invoices(self):
        """Collect tax invoices"""
        invoices = self.engine.get_my_invoices()
        month = datetime.now().strftime('%Y-%m')
        
        messagebox.showinfo(
            "Invoice Collection",
            f"Found {len(invoices)} total invoices\n\n"
            f"Current month ({month}): Ready for processing\n\n"
            "✓ Mark checklist item when collection is complete"
        )
    
    def _verify_gst_numbers(self):
        """Verify GST numbers of clients"""
        self._verify_all_gst()
    
    def _verify_all_gst(self):
        """Verify all client GST numbers"""
        invoices = self.engine.get_my_invoices()
        
        clients = {}
        for inv in invoices:
            client = inv.get('client_name', 'Unknown')
            gst = inv.get('client_gst', 'Not Provided')
            clients[client] = gst
        
        self.verification_text.delete('1.0', 'end')
        output = "Client GST Verification Report\n"
        output += "=" * 60 + "\n\n"
        output += f"Total Unique Clients: {len(clients)}\n\n"
        
        verified_count = 0
        for client, gst in clients.items():
            if gst and gst != 'Not Provided' and len(gst) == 15:
                status = "✓ Valid Format"
                verified_count += 1
            else:
                status = "❌ Missing/Invalid"
            
            output += f"{client}:\n  GST: {gst}\n  Status: {status}\n\n"
        
        output += f"\nVerified: {verified_count}/{len(clients)}\n"
        
        self.verification_text.insert('1.0', output)
    
    def _match_bank_statements(self):
        """Match with bank statements"""
        messagebox.showinfo(
            "Bank Matching",
            "Bank Statement Matching:\n\n"
            "1. Export your bank statement for the month\n"
            "2. Compare invoice totals with deposits\n"
            "3. Identify any discrepancies\n\n"
            "Tip: Use Export panel to get invoice summary"
        )
    
    def _calculate_taxes(self):
        """Calculate CGST/SGST/IGST"""
        self._calculate_month_taxes()
    
    def _calculate_month_taxes(self):
        """Calculate taxes for the month"""
        try:
            month = self.month_entry.get()
            invoices = self.engine.get_my_invoices()
            
            # Filter by month
            month_invoices = [inv for inv in invoices 
                            if inv.get('invoice_date', '').startswith(month)]
            
            if not month_invoices:
                messagebox.showinfo("No Data", f"No invoices found for {month}")
                return
            
            total_taxable = sum(inv.get('subtotal', 0) for inv in month_invoices)
            total_tax = sum(inv.get('tax_amount', 0) for inv in month_invoices)
            cgst = total_tax / 2
            sgst = total_tax / 2
            
            self.tax_results_text.delete('1.0', 'end')
            output = f"Tax Calculation for {month}\n"
            output += "=" * 60 + "\n\n"
            output += f"Total Invoices: {len(month_invoices)}\n"
            output += f"Taxable Amount: ₹{total_taxable:,.2f}\n\n"
            output += f"CGST (9%): ₹{cgst:,.2f}\n"
            output += f"SGST (9%): ₹{sgst:,.2f}\n"
            output += f"Total GST: ₹{total_tax:,.2f}\n\n"
            output += f"Grand Total: ₹{total_taxable + total_tax:,.2f}\n"
            
            self.tax_results_text.insert('1.0', output)
            
        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed: {str(e)}")
    
    def _file_gstr1(self):
        """File GSTR-1"""
        messagebox.showinfo(
            "GSTR-1 Filing",
            "GSTR-1 Filing Steps:\n\n"
            "1. Login to GST Portal (www.gst.gov.in)\n"
            "2. Go to Services > Returns > GSTR-1\n"
            "3. Upload invoice details\n"
            "4. Review and Submit\n\n"
            "Use 'Generate GSTR-1 Summary' in Reports tab"
        )
    
    def _file_gstr3b(self):
        """File GSTR-3B"""
        messagebox.showinfo(
            "GSTR-3B Filing",
            "GSTR-3B Filing Steps:\n\n"
            "1. Login to GST Portal\n"
            "2. Go to Services > Returns > GSTR-3B\n"
            "3. Fill tax liability details\n"
            "4. Pay and File\n\n"
            "Use 'Generate GSTR-3B Summary' in Reports tab"
        )
    
    def _pay_liability(self):
        """Pay GST liability"""
        messagebox.showinfo(
            "GST Payment",
            "GST Payment Process:\n\n"
            "1. Calculate total tax liability\n"
            "2. Login to GST Portal\n"
            "3. Services > Payments > Create Challan\n"
            "4. Pay online via Net Banking/Card\n\n"
            "Deadline: 20th of next month"
        )
    
    def _download_acknowledgments(self):
        """Download acknowledgments"""
        messagebox.showinfo(
            "Acknowledgments",
            "Download Filing Acknowledgments:\n\n"
            "1. Login to GST Portal\n"
            "2. Services > Returns > Track Return Status\n"
            "3. Download ARN for GSTR-1 and GSTR-3B\n"
            "4. Save for records\n\n"
            "Keep these for audit purposes"
        )
    
    def _generate_gstr1_summary(self):
        """Generate GSTR-1 summary"""
        invoices = self.engine.get_my_invoices()
        
        summary = "GSTR-1 Summary Report\n"
        summary += "=" * 60 + "\n\n"
        summary += f"Total Invoices: {len(invoices)}\n"
        summary += f"Total Value: ₹{sum(inv.get('total_amount', 0) for inv in invoices):,.2f}\n\n"
        summary += "Ready for GSTR-1 filing on GST Portal\n"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"GSTR1_Summary_{datetime.now().strftime('%Y%m')}.txt"
        )
        
        if filename:
            with open(filename, 'w') as f:
                f.write(summary)
            messagebox.showinfo("Success", f"GSTR-1 summary saved:\n{filename}")
    
    def _generate_gstr3b_summary(self):
        """Generate GSTR-3B summary"""
        invoices = self.engine.get_my_invoices()
        
        total_tax = sum(inv.get('tax_amount', 0) for inv in invoices)
        
        summary = "GSTR-3B Summary Report\n"
        summary += "=" * 60 + "\n\n"
        summary += f"Tax Liability: ₹{total_tax:,.2f}\n"
        summary += f"CGST: ₹{total_tax/2:,.2f}\n"
        summary += f"SGST: ₹{total_tax/2:,.2f}\n\n"
        summary += "Ready for GSTR-3B filing on GST Portal\n"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"GSTR3B_Summary_{datetime.now().strftime('%Y%m')}.txt"
        )
        
        if filename:
            with open(filename, 'w') as f:
                f.write(summary)
            messagebox.showinfo("Success", f"GSTR-3B summary saved:\n{filename}")
    
    def _export_gst_report(self):
        """Export complete GST report"""
        from analytics.regulatory import RegulatoryHelper
        
        invoices = self.engine.get_my_invoices()
        month = datetime.now().strftime('%Y-%m')
        
        report = RegulatoryHelper.generate_gst_report(invoices, month)
        
        messagebox.showinfo("GST Report", f"GST Report Generated\n\nPeriod: {report.get('period')}\nTotal GST: ₹{report.get('total_gst', 0):,.2f}")
    
    def _view_filing_history(self):
        """View filing history"""
        messagebox.showinfo(
            "Filing History",
            "GST Filing History:\n\n"
            "Track your completed filings:\n"
            "• GSTR-1 submissions\n"
            "• GSTR-3B submissions\n"
            "• Payment records\n\n"
            "Feature: Coming in next update"
        )
    
    def refresh(self):
        """Refresh panel"""
        self.checklist_status = self._load_checklist_status()
        for key, var in self.checklist_vars.items():
            var.set(self.checklist_status.get(key, False))
        self._update_progress()
