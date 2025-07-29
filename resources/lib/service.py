import xbmc
import threading
import settings
from tv_skip import handle_tvshow
from movie_skip import handle_movie

class SkippyService(xbmc.Monitor):
    def __init__(self):
        super(SkippyService, self).__init__()
        self.tv_thread = None
        self.movie_thread = None
        
    def onSettingsChanged(self):
        xbmc.log("Skippy Service: Settings changed, reloading...", xbmc.LOGINFO)
        settings.load_settings()
    
    def run(self):
        xbmc.log("Skippy Service: Starting", xbmc.LOGINFO)
        
        # Start TV show monitoring thread if enabled
        if settings.ENABLE_TVSHOW:
            self.tv_thread = threading.Thread(target=handle_tvshow, daemon=True)
            self.tv_thread.start()
            xbmc.log("Skippy Service: TV show monitoring started", xbmc.LOGINFO)
        
        # Start movie monitoring thread if enabled  
        if settings.ENABLE_MOVIES:
            self.movie_thread = threading.Thread(target=handle_movie, daemon=True)
            self.movie_thread.start()
            xbmc.log("Skippy Service: Movie monitoring started", xbmc.LOGINFO)
        
        # Keep service alive
        while not self.abortRequested():
            if self.waitForAbort(10):  # Check every 10 seconds instead of 1
                break
                
        xbmc.log("Skippy Service: Shutting down", xbmc.LOGINFO)

if __name__ == '__main__':
    service = SkippyService()
    service.run()