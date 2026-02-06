"""
Modern UI Components with World-Class Styling
Interactive elements with animations and effects
"""

import tkinter as tk
from tkinter import ttk
from ui.theme import COLORS, FONTS, SPACING, RADIUS, SHADOWS, BUTTON_STYLES


class ModernButton(tk.Canvas):
    """Modern button with hover effects and animations"""
    
    def __init__(self, parent, text, command=None, style='primary', width=150, height=40, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        
        self.text = text
        self.command = command
        self.style_name = style
        self.style = BUTTON_STYLES[style]
        self.width = width
        self.height = height
        
        self.is_hovered = False
        self.is_pressed = False
        
        self._draw()
        self._bind_events()
    
    def _draw(self):
        """Draw button with current state"""
        self.delete('all')
        
        # Determine colors based on state
        if self.is_pressed:
            bg = self.style['active_bg']
        elif self.is_hovered:
            bg = self.style['hover_bg']
        else:
            bg = self.style['bg']
        
        fg = self.style['fg']
        
        # Draw rounded rectangle
        radius = RADIUS['md']
        self.create_rounded_rect(0, 0, self.width, self.height, radius, fill=bg, outline='')
        
        # Draw text
        self.create_text(
            self.width/2, self.height/2,
            text=self.text,
            fill=fg,
            font=FONTS['sizes']['body']
        )
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Draw rounded rectangle"""
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _bind_events(self):
        """Bind mouse events"""
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)
    
    def _on_enter(self, event):
        """Mouse enter"""
        self.is_hovered = True
        self.config(cursor='hand2')
        self._draw()
    
    def _on_leave(self, event):
        """Mouse leave"""
        self.is_hovered = False
        self.is_pressed = False
        self.config(cursor='')
        self._draw()
    
    def _on_press(self, event):
        """Mouse press"""
        self.is_pressed = True
        self._draw()
    
    def _on_release(self, event):
        """Mouse release"""
        self.is_pressed = False
        self._draw()
        if self.command and self.is_hovered:
            self.command()


class GradientFrame(tk.Canvas):
    """Frame with gradient background"""
    
    def __init__(self, parent, width=800, height=100, color1=None, color2=None, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        
        self.color1 = color1 or COLORS['gradient_start']
        self.color2 = color2 or COLORS['gradient_end']
        
        self._draw_gradient()
    
    def _draw_gradient(self):
        """Draw vertical gradient"""
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        
        # Simple gradient simulation (top to bottom)
        limit = height
        for i in range(limit):
            r1, g1, b1 = self._hex_to_rgb(self.color1)
            r2, g2, b2 = self._hex_to_rgb(self.color2)
            
            r = int(r1 + (r2 - r1) * i / limit)
            g = int(g1 + (g2 - g1) * i / limit)
            b = int(b1 + (b2 - b1) * i / limit)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.create_line(0, i, width, i, fill=color)
    
    @staticmethod
    def _hex_to_rgb(hex_color):
        """Convert hex to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


class ModernCard(ttk.Frame):
    """Card component with shadow effect"""
    
    def __init__(self, parent, title=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(relief='flat', borderwidth=0)
        
        # Configure style
        style = ttk.Style()
        style.configure('Card.TFrame', background=COLORS['surface'])
        self.configure(style='Card.TFrame')
        
        if title:
            title_label = ttk.Label(
                self,
                text=title,
                font=FONTS['sizes']['heading'],
                foreground=COLORS['text_primary'],
                background=COLORS['surface']
            )
            title_label.pack(anchor='w', padx=SPACING['md'], pady=(SPACING['md'], SPACING['sm']))


class StatusBadge(tk.Label):
    """Colored status badge"""
    
    def __init__(self, parent, text, status='info', **kwargs):
        """
        status: 'success', 'warning', 'error', 'info'
        """
        color_map = {
            'success': COLORS['success'],
            'warning': COLORS['warning'],
            'error': COLORS['error'],
            'info': COLORS['info'],
        }
        
        bg_color = color_map.get(status, COLORS['info'])
        
        super().__init__(
            parent,
            text=text,
            bg=bg_color,
            fg='white',
            font=FONTS['sizes']['small'],
            padx=8,
            pady=4,
            **kwargs
        )


class IconButton(tk.Label):
    """Icon-only button with hover effect"""
    
    def __init__(self, parent, icon, command=None, **kwargs):
        super().__init__(
            parent,
            text=icon,
            font=('Segoe UI', 16),
            cursor='hand2',
            **kwargs
        )
        
        self.command = command
        self.default_bg = kwargs.get('bg', COLORS['surface'])
        
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)
    
    def _on_enter(self, event):
        self.configure(bg=COLORS['background'])
    
    def _on_leave(self, event):
        self.configure(bg=self.default_bg)
    
    def _on_click(self, event):
        if self.command:
            self.command()


class ProgressBar(tk.Canvas):
    """Modern progress bar with animation"""
    
    def __init__(self, parent, width=300, height=8, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        
        self.width = width
        self.height = height
        self.progress = 0
        
        self._draw()
    
    def _draw(self):
        """Draw progress bar"""
        self.delete('all')
        
        # Background
        self.create_rectangle(
            0, 0, self.width, self.height,
            fill=COLORS['background'],
            outline=''
        )
        
        # Progress fill
        if self.progress > 0:
            fill_width = self.width * (self.progress / 100)
            self.create_rectangle(
                0, 0, fill_width, self.height,
                fill=COLORS['accent'],
                outline=''
            )
    
    def set_progress(self, value):
        """Set progress (0-100)"""
        self.progress = max(0, min(100, value))
        self._draw()


class SearchBox(ttk.Frame):
    """Modern search box with icon"""
    
    def __init__(self, parent, placeholder="Search...", on_search=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.on_search = on_search
        
        # Search icon
        icon = ttk.Label(self, text="🔍", font=('Segoe UI', 12))
        icon.pack(side='left', padx=(SPACING['sm'], 0))
        
        # Entry field
        self.entry = ttk.Entry(self, font=FONTS['sizes']['body'], width=30)
        self.entry.pack(side='left', fill='x', expand=True, padx=SPACING['xs'])
        self.entry.insert(0, placeholder)
        self.entry.config(foreground=COLORS['text_hint'])
        
        # Bindings
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
        self.entry.bind('<Return>', lambda e: self._search())
        
        self.placeholder = placeholder
    
    def _on_focus_in(self, event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, 'end')
            self.entry.config(foreground=COLORS['text_primary'])
    
    def _on_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(foreground=COLORS['text_hint'])
    
    def _search(self):
        text = self.entry.get()
        if text and text != self.placeholder and self.on_search:
            self.on_search(text)
    
    def get(self):
        text = self.entry.get()
        return text if text != self.placeholder else ""
