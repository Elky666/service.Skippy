import xbmc
import xbmcgui
import time
import threading
import xbmcaddon
import settings
from skip_utils import get_intro_times
from skip_dialog import show_skip_dialog

addon = xbmcaddon.Addon()

class SkipIntroMonitor(xbmc.Monitor):
    def __init__(self):
        super(SkipIntroMonitor, self).__init__()
        self.skipped = False
        self.button_shown = False
        self.last_path = None

monitor = SkipIntroMonitor()
player = xbmc.Player()

def handle_tvshow():
    """Main TV show handling loop with NO notifications or text"""
    while not monitor.abortRequested():
        
        if player.isPlaying():
            path = player.getPlayingFile()
            
            # Reset flags when new file starts playing
            if path != monitor.last_path:
                monitor.skipped = False
                monitor.button_shown = False
                monitor.last_path = path
                xbmc.log(f"Skip Intro: New file playing", xbmc.LOGDEBUG)

            intro_start, intro_end = get_intro_times(path)
            
            # NO notifications for missing intro chapters
            if intro_start is not None and not monitor.skipped:
                current_time = player.getTime()
                
                # Check if we're in the intro timeframe
                if intro_start <= current_time <= intro_end:
                    if not monitor.button_shown:
                        monitor.button_shown = True
                        xbmc.log(f"Skip Intro: Showing dialog", xbmc.LOGDEBUG)
                        
                        # Show the custom image-only dialog
                        skipped = show_skip_dialog(
                            end_time=intro_end,
                            auto_skip_delay=settings.AUTO_SKIP_DELAY or 10,
                            auto_skip_enabled=settings.AUTO_SKIP or False
                        )
                        
                        if skipped:
                            monitor.skipped = True
                            xbmc.log("Skip Intro: Skipped", xbmc.LOGDEBUG)
                            
                # Reset button_shown flag when we're past the intro
                elif current_time > intro_end and monitor.button_shown:
                    monitor.button_shown = False
                    
        else:
            # Reset when not playing
            if monitor.last_path is not None:
                monitor.skipped = False
                monitor.button_shown = False
                monitor.last_path = None

        # Wait before next check
        if monitor.waitForAbort(1):
            break