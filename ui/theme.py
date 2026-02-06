"""
Modern Theme Configuration for DocFlow Pro v2.0
World-class UI styling
"""

# Color Palette - Premium Modern Design
COLORS = {
    # Primary Colors
    'primary': '#1a237e',           # Deep Blue
    'primary_light': '#3f51b5',     # Indigo
    'primary_dark': '#0d1642',      # Navy
    
    # Accent Colors
    'accent': '#00bcd4',            # Cyan
    'accent_light': '#62efff',      # Light Cyan
    'accent_dark': '#008ba3',       # Dark Cyan
    
    # Success/Info/Warning/Error
    'success': '#4caf50',           # Green
    'info': '#2196f3',              # Blue
    'warning': '#ff9800',           # Orange
    'error': '#f44336',             # Red
    
    # Neutral Colors
    'background': '#f5f7fa',        # Light Gray
    'surface': '#ffffff',           # White
    'border': '#e0e0e0',            # Border Gray
    
    # Text Colors
    'text_primary': '#212121',      # Dark Gray
    'text_secondary': '#757575',    # Medium Gray
    'text_hint': '#9e9e9e',         # Light Gray
    
    # Gradient Colors
    'gradient_start': '#1a237e',
    'gradient_end': '#00bcd4',
    
    # Glass Effect
    'glass_bg': 'rgba(255, 255, 255, 0.7)',
    'glass_border': 'rgba(255, 255, 255, 0.18)',
}

# Typography
FONTS = {
    'primary': 'Segoe UI',
    'secondary': 'Arial',
    'mono': 'Consolas',
    'sizes': {
        'title': ('Segoe UI', 24, 'bold'),
        'heading': ('Segoe UI', 18, 'bold'),
        'subheading': ('Segoe UI', 14, 'bold'),
        'body': ('Segoe UI', 11),
        'small': ('Segoe UI', 9),
        'code': ('Consolas', 10),
    }
}

# Spacing
SPACING = {
    'xs': 5,
    'sm': 10,
    'md': 15,
    'lg': 20,
    'xl': 30,
}

# Border Radius
RADIUS = {
    'sm': 4,
    'md': 8,
    'lg': 12,
    'xl': 16,
    'full': 999,
}

# Shadows
SHADOWS = {
    'sm': '0 2px 4px rgba(0,0,0,0.1)',
    'md': '0 4px 8px rgba(0,0,0,0.15)',
    'lg': '0 8px 16px rgba(0,0,0,0.2)',
    'xl': '0 12px 24px rgba(0,0,0,0.25)',
}

# Animations
ANIMATIONS = {
    'duration_fast': 150,    # ms
    'duration_normal': 300,  # ms
    'duration_slow': 500,    # ms
    'easing': 'ease-in-out',
}

# Button Styles
BUTTON_STYLES = {
    'primary': {
        'bg': COLORS['primary'],
        'fg': '#ffffff',
        'hover_bg': COLORS['primary_light'],
        'active_bg': COLORS['primary_dark'],
    },
    'accent': {
        'bg': COLORS['accent'],
        'fg': '#ffffff',
        'hover_bg': COLORS['accent_light'],
        'active_bg': COLORS['accent_dark'],
    },
    'success': {
        'bg': COLORS['success'],
        'fg': '#ffffff',
        'hover_bg': '#66bb6a',
        'active_bg': '#388e3c',
    },
    'ghost': {
        'bg': 'transparent',
        'fg': COLORS['primary'],
        'hover_bg': 'rgba(26,35,126,0.1)',
        'active_bg': 'rgba(26,35,126,0.2)',
    }
}

# Panel Styles
PANEL_STYLES = {
    'default': {
        'bg': COLORS['surface'],
        'border': COLORS['border'],
        'shadow': SHADOWS['sm'],
        'radius': RADIUS['md'],
    },
    'elevated': {
        'bg': COLORS['surface'],
        'border': 'none',
        'shadow': SHADOWS['lg'],
        'radius': RADIUS['lg'],
    },
    'glass': {
        'bg': COLORS['glass_bg'],
        'border': COLORS['glass_border'],
        'shadow': SHADOWS['md'],
        'radius': RADIUS['lg'],
        'backdrop_filter': 'blur(10px)',
    }
}

# Icon mapping for emojis (can be replaced with icon font)
ICONS = {
    'dashboard': '📊',
    'documents': '📄',
    'invoices': '🧾',
    'export': '📤',
    'ai_factory': '🏭',
    'bi': '📈',
    'cleaning': '🧹',
    'ai_settings': '🤖',
    'regulatory': '📚',
    'settings': '⚙️',
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    'loading': '⏳',
}
