"""
Data Cleaning Panel
Clean and improve data quality
"""

import tkinter as tk
from tkinter import ttk, messagebox


class DataCleaningPanel(ttk.Frame):
    """Data cleaning and quality improvement"""
    
    def __init__(self, parent, engine, user_id):
        super().__init__(parent)
        self.frame = self  # For panel switching compatibility
        self.engine = engine
        self.user_id = user_id
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create data cleaning interface"""
        # Title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        ttk.Label(
            title_frame,
            text="🧹 Data Cleaning",
            font=('Helvetica', 16, 'bold')
        ).pack(side='left')
        
        ttk.Label(
            title_frame,
            text="Improve data quality automatically",
            font=('Helvetica', 9),
            foreground='#666'
        ).pack(side='left', padx=(10, 0))
        
        # Content
        content = ttk.Frame(self)
        content.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Data quality score
        score_frame = ttk.LabelFrame(content, text="📊 Data Quality Score", padding=15)
        score_frame.pack(fill='x', pady=(0, 15))
        
        self.score_label = ttk.Label(
            score_frame,
            text="Click 'Analyze' to check data quality",
            font=('Helvetica', 12)
        )
        self.score_label.pack()
        
        ttk.Button(
            score_frame,
            text="🔍 Analyze Data Quality",
            command=self._analyze_quality
        ).pack(pady=(10, 0))
        
        # Cleaning options
        clean_frame = ttk.LabelFrame(content, text="🧹 Cleaning Operations", padding=15)
        clean_frame.pack(fill='x', pady=(0, 15))
        
        operations = [
            ("Remove Duplicates", self._remove_duplicates),
            ("Fix Missing Values", self._fix_missing),
            ("Standardize Formats", self._standardize_formats),
            ("Validate Data", self._validate_data),
            ("Clean All (Recommended)", self._clean_all)
        ]
        
        for text, command in operations:
            ttk.Button(
                clean_frame,
                text=text,
                command=command,
                width=25
            ).pack(pady=2)
        
        # Results display
        results_frame = ttk.LabelFrame(content, text="📋 Cleaning Results", padding=15)
        results_frame.pack(fill='both', expand=True)
        
        self.results_text = tk.Text(
            results_frame,
            height=15,
            width=80,
            wrap='word',
            font=('Courier', 9)
        )
        self.results_text.pack(fill='both', expand=True)
    
    def _analyze_quality(self):
        """Analyze data quality"""
        try:
            from ml.data_cleaner import DataQualityScorer
            
            invoices = self.engine.get_my_invoices()
            
            if not invoices:
                messagebox.showinfo("No Data", "No invoices to analyze")
                return
            
            result = DataQualityScorer.score_invoice_data(invoices)
            
            score = result['score']
            grade = result['grade']
            issues = result['issues']
            
            # Color based on score
            if score >= 90:
                color = 'green'
                emoji = '🟢'
            elif score >= 75:
                color = 'orange'
                emoji = '🟡'
            else:
                color = 'red'
                emoji = '🔴'
            
            self.score_label.config(
                text=f"{emoji} Data Quality: {score}/100 (Grade: {grade})",
                foreground=color
            )
            
            # Show issues
            self.results_text.delete('1.0', 'end')
            output = "Data Quality Analysis Results\n"
            output += "=" * 60 + "\n\n"
            output += f"Score: {score}/100\n"
            output += f"Grade: {grade}\n\n"
            output += "Issues Found:\n"
            for issue in issues:
                output += f"  • {issue}\n"
            
            self.results_text.insert('1.0', output)
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
    
    def _clean_all(self):
        """Clean all data"""
        try:
            from ml.data_cleaner import DataCleaner
            
            invoices = self.engine.get_my_invoices()
            
            if not invoices:
                messagebox.showinfo("No Data", "No invoices to clean")
                return
            
            cleaner = DataCleaner()
            cleaned, stats = cleaner.clean_invoices(invoices)
            
            # Show results
            report = cleaner.get_cleaning_report()
            self.results_text.delete('1.0', 'end')
            self.results_text.insert('1.0', report)
            
            messagebox.showinfo(
                "Success",
                f"✓ Data cleaned successfully!\n\n"
                f"Improvements: {sum(stats.values())}\n"
                f"Cleaned invoices: {len(cleaned)}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Cleaning failed: {str(e)}")
    
    def _remove_duplicates(self):
        """Remove duplicate records"""
        try:
            invoices = self.engine.get_my_invoices()
            
            if not invoices:
                messagebox.showinfo("No Data", "No invoices to process")
                return
            
            # Find duplicates by invoice_number
            seen = {}
            duplicates = []
            
            for inv in invoices:
                inv_num = inv.get('invoice_number', '')
                if inv_num in seen:
                    duplicates.append(inv)
                else:
                    seen[inv_num] = inv
            
            self.results_text.delete('1.0', 'end')
            output = "Duplicate Removal Results\n"
            output += "=" * 60 + "\n\n"
            output += f"Total Invoices: {len(invoices)}\n"
            output += f"Unique Invoices: {len(seen)}\n"
            output += f"Duplicates Found: {len(duplicates)}\n\n"
            
            if duplicates:
                output += "Duplicate Invoice Numbers:\n"
                for dup in duplicates:
                    output += f"  • {dup.get('invoice_number')} - {dup.get('client_name')}\n"
            else:
                output += "✓ No duplicates found!\n"
            
            self.results_text.insert('1.0', output)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {str(e)}")
    
    def _fix_missing(self):
        """Fix missing values"""
        try:
            invoices = self.engine.get_my_invoices()
            
            if not invoices:
                messagebox.showinfo("No Data", "No invoices to process")
                return
            
            missing_count = 0
            issues = []
            
            for inv in invoices:
                if not inv.get('client_name'):
                    issues.append(f"Invoice #{inv.get('invoice_number')}: Missing client name")
                    missing_count += 1
                
                if not inv.get('client_email'):
                    issues.append(f"Invoice #{inv.get('invoice_number')}: Missing email")
                    missing_count += 1
                
                if inv.get('total_amount', 0) == 0:
                    issues.append(f"Invoice #{inv.get('invoice_number')}: Zero amount")
                    missing_count += 1
            
            self.results_text.delete('1.0', 'end')
            output = "Missing Values Report\n"
            output += "=" * 60 + "\n\n"
            output += f"Total Invoices: {len(invoices)}\n"
            output += f"Missing/Invalid Fields: {missing_count}\n\n"
            
            if issues:
                output += "Issues Found:\n"
                for issue in issues[:20]:  # Show first 20
                    output += f"  • {issue}\n"
                if len(issues) > 20:
                    output += f"\n...and {len(issues)-20} more\n"
            else:
                output += "✓ No missing values found!\n"
            
            self.results_text.insert('1.0', output)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {str(e)}")
    
    def _standardize_formats(self):
        """Standardize data formats"""
        try:
            invoices = self.engine.get_my_invoices()
            
            if not invoices:
                messagebox.showinfo("No Data", "No invoices to process")
                return
            
            format_issues = []
            
            for inv in invoices:
                # Check date format
                inv_date = inv.get('invoice_date', '')
                if inv_date and not inv_date.count('-') == 2:
                    format_issues.append(f"Invoice #{inv.get('invoice_number')}: Invalid date format")
                
                # Check invoice number format
                inv_num = inv.get('invoice_number', '')
                if inv_num and not any(c.isdigit() for c in inv_num):
                    format_issues.append(f"Invoice #{inv_num}: No digits in invoice number")
            
            self.results_text.delete('1.0', 'end')
            output = "Format Standardization Report\n"
            output += "=" * 60 + "\n\n"
            output += f"Total Invoices: {len(invoices)}\n"
            output += f"Format Issues: {len(format_issues)}\n\n"
            
            if format_issues:
                output += "Issues Found:\n"
                for issue in format_issues[:15]:
                    output += f"  • {issue}\n"
                if len(format_issues) > 15:
                    output += f"\n...and {len(format_issues)-15} more\n"
            else:
               output += "✓ All formats are standardized!\n"
            
            self.results_text.insert('1.0', output)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {str(e)}")
    
    def _validate_data(self):
        """Validate data integrity"""
        try:
            invoices = self.engine.get_my_invoices()
            
            if not invoices:
                messagebox.showinfo("No Data", "No invoices to process")
                return
            
            errors = []
            warnings = []
            
            for inv in invoices:
                # Critical errors
                if not inv.get('invoice_number'):
                    errors.append("Missing invoice number")
                
                if not inv.get('client_name'):
                    errors.append(f"Invoice #{inv.get('invoice_number', 'Unknown')}: Missing client")
                
                if inv.get('total_amount', 0) < 0:
                    errors.append(f"Invoice #{inv.get('invoice_number')}: Negative amount")
                
                # Warnings
                if inv.get('total_amount', 0) > 1000000:
                    warnings.append(f"Invoice #{inv.get('invoice_number')}: Very high amount (₹{inv.get('total_amount'):,.0f})")
                
                if inv.get('status') == 'pending' and inv.get('invoice_date', '').startswith('2023'):
                    warnings.append(f"Invoice #{inv.get('invoice_number')}: Old pending invoice")
            
            self.results_text.delete('1.0', 'end')
            output = "Data Validation Report\n"
            output += "=" * 60 + "\n\n"
            output += f"Total Invoices: {len(invoices)}\n"
            output += f"Critical Errors: {len(errors)}\n"
            output += f"Warnings: {len(warnings)}\n\n"
            
            if errors:
                output += "Critical Errors:\n"
                for error in errors[:10]:
                    output += f"  ❌ {error}\n"
            
            if warnings:
                output += "\nWarnings:\n"
                for warning in warnings[:10]:
                    output += f"  ⚠️ {warning}\n"
            
            if not errors and not warnings:
                output += "✓ All data is valid!\n"
            
            self.results_text.insert('1.0', output)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {str(e)}")
    
    def refresh(self):
        """Refresh panel"""
        self.results_text.delete('1.0', 'end')
        self.score_label.config(text="Click 'Analyze' to check data quality")
