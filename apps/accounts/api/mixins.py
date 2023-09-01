from rest_framework.throttling import ScopedRateThrottle


class ScopedRateThrottleForCUMixin:
    """
    Add ScopedRateThrottle class for POST PUT PATCH
    """
    def get_throttles(self):
        if self.request.method in ['PATCH','PUT','POST']:
            throttle_classes = [ScopedRateThrottle]
        else:
            throttle_classes = []
        
        return [throttle() for throttle in throttle_classes]
