"""
Performance Monitor - Track operation performance
"""

import time
import functools
from collections import defaultdict
from core.logger import get_logger

logger = get_logger('app')


class PerformanceMonitor:
    """Monitor application performance"""
    
    def __init__(self):
        self.metrics = defaultdict(lambda: {
            'count': 0,
            'total_time': 0,
            'avg_time': 0,
            'min_time': float('inf'),
            'max_time': 0,
            'failures': 0
        })
        self.slow_threshold = 1.0  # Operations slower than 1s are logged as slow
    
    def track_operation(self, operation_name):
        """
        Decorator to track operation performance
        
        Usage:
            perf = Performance Monitor()
            
            @perf.track_operation('create_invoice')
            def create_invoice(...):
                ...
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                success = True
                result = None
                
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    success = False
                    raise
                finally:
                    duration = time.time() - start_time
                    self._record_metric(operation_name, duration, success)
                    
                    if duration > self.slow_threshold:
                        logger.warning(
                            f"Slow operation: {operation_name} took {duration:.2f}s"
                        )
            
            return wrapper
        return decorator
    
    def _record_metric(self, operation, duration, success):
        """Record performance metric"""
        m = self.metrics[operation]
        
        m['count'] += 1
        m['total_time'] += duration
        m['avg_time'] = m['total_time'] / m['count']
        m['min_time'] = min(m['min_time'], duration)
        m['max_time'] = max(m['max_time'], duration)
        
        if not success:
            m['failures'] += 1
    
    def get_metrics(self, operation=None):
        """Get performance metrics"""
        if operation:
            return dict(self.metrics.get(operation, {}))
        return {op: dict(metrics) for op, metrics in self.metrics.items()}
    
    def get_report(self):
        """Get formatted performance report"""
        report_lines = ["Performance Report", "=" * 50]
        
        for operation, metrics in self.metrics.items():
            report_lines.append(f"\n{operation}:")
            report_lines.append(f"  Count: {metrics['count']}")
            report_lines.append(f"  Avg Time: {metrics['avg_time']:.3f}s")
            report_lines.append(f"  Min/Max: {metrics['min_time']:.3f}s / {metrics['max_time']:.3f}s")
            report_lines.append(f"  Failures: {metrics['failures']}")
            
            if metrics['count'] > 0:
                success_rate = (metrics['count'] - metrics['failures']) / metrics['count'] * 100
                report_lines.append(f"  Success Rate: {success_rate:.1f}%")
        
        return '\n'.join(report_lines)
    
    def reset_metrics(self):
        """Reset all metrics"""
        self.metrics.clear()
        logger.info("Performance metrics reset")


# Global performance monitor instance
_performance_monitor = PerformanceMonitor()

def get_performance_monitor():
    """Get global performance monitor"""
    return _performance_monitor
