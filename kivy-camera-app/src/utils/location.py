from kivy.utils import platform
from functools import partial
from kivy.clock import Clock

class LocationManager:
    def __init__(self):
        self.has_permission = True
        self.location_callbacks = []
        
    def configure(self):
        if platform == 'android':
            from plyer import gps
            try:
                gps.configure(
                    on_location=self.on_location,
                    on_status=self.on_status
                )
                return True
            except:
                return False
        return True
    
    def start(self):
        if platform == 'android':
            from plyer import gps
            try:
                gps.start(minTime=1000, minDistance=1)
            except:
                pass
        else:
            # Mock location updates for Windows
            Clock.schedule_interval(self.mock_location_update, 2)
    
    def stop(self):
        if platform == 'android':
            from plyer import gps
            try:
                gps.stop()
            except:
                pass
        else:
            Clock.unschedule(self.mock_location_update)
    
    def mock_location_update(self, dt):
        # Mock location data for testing
        self.on_location({
            'lat': 48.8566,
            'lon': 2.3522,
            'accuracy': 10,
            'bearing': 0,
            'speed': 0,
            'altitude': 35
        })
    
    def on_location(self, location):
        for callback in self.location_callbacks:
            callback(location)
    
    def on_status(self, status):
        pass
    
    def add_location_callback(self, callback):
        self.location_callbacks.append(callback)
