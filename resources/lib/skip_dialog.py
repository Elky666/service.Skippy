import xbmc
import xbmcgui
import xbmcaddon
import time
import threading

addon = xbmcaddon.Addon()

class SkippyIntroDialog(xbmcgui.WindowXMLDialog):
    
    SKIP_IMAGE_ID = 100
    def __init__(self, *args, **kwargs):
        """Initialize dialog with end time and auto-skip settings"""
        super(SkippyIntroDialog, self).__init__()
        self.end_time = kwargs.get('end_time', 0)
        self.auto_skip_delay = kwargs.get('auto_skip_delay', 10)
        self.auto_skip_enabled = kwargs.get('auto_skip_enabled', True)
        self.player = xbmc.Player()
        self.skipped = False
        self.start_time = time.time()
        
    def onInit(self):
        """Initialize dialog and start auto-close timer"""
        try:
            xbmc.log("Image dialog initialized", xbmc.LOGINFO)
            threading.Thread(target=self.auto_close_timer, daemon=True).start()
        except Exception as e:
            xbmc.log(f"Dialog init error: {e}", xbmc.LOGERROR)
    
    def auto_close_timer(self):
        """Automatically close dialog after end time or delay"""
        while not self.skipped:
            try:
                if not self.player.isPlaying():
                    self.close()
                    break
                    
                current_time = self.player.getTime()
                elapsed = time.time() - self.start_time
                
                if (current_time >= float(self.end_time) or 
                    elapsed >= self.auto_skip_delay):
                    
                    if (self.auto_skip_enabled and 
                        current_time < float(self.end_time)):
                        self.skip_intro()
                    else:
                        self.close()
                    break
                    
                xbmc.sleep(200)
                
            except Exception as e:
                xbmc.log(f"Timer error: {e}", xbmc.LOGERROR)
                break
    
    def onControl(self, control):
        """Handle image clicks"""
        if control.getId() == self.SKIP_IMAGE_ID:
            xbmc.log("Image clicked - skipping", xbmc.LOGINFO)
            self.skip_intro()
    
    def skip_intro(self):
        """Skip intro"""
        try:
            self.skipped = True
            self.player.seekTime(float(self.end_time))
            xbmc.log("Skipped to end time", xbmc.LOGINFO)
            self.close()
        except Exception as e:
            xbmc.log(f"Skip error: {e}", xbmc.LOGERROR)
            self.close()
    
    def onAction(self, action):
        """Handle remote actions"""
        if action.getId() in [xbmcgui.ACTION_NAV_BACK, 
                            xbmcgui.ACTION_PREVIOUS_MENU,
                            xbmcgui.ACTION_STOP]:
            self.close()
        elif action.getId() in [xbmcgui.ACTION_SELECT_ITEM,
                            xbmcgui.ACTION_PLAYER_PLAY]:
            self.skip_intro()


def show_skip_dialog(end_time, auto_skip_delay=10, auto_skip_enabled=True):
    """Show pure image dialog"""
    try:
        xbmc.log("Attempting to show image dialog", xbmc.LOGINFO)
        
        dialog = SkippyIntroDialog(
            'skip-intro-dialog.xml',
            addon.getAddonInfo('path'),
            'default',
            '1080i',
            end_time=end_time,
            auto_skip_delay=auto_skip_delay,
            auto_skip_enabled=auto_skip_enabled
        )
        dialog.doModal()
        
        xbmc.log(f"Dialog closed, skipped: {dialog.skipped}", xbmc.LOGINFO)
        return dialog.skipped
        
    except Exception as e:
        xbmc.log(f"Image dialog failed: {e}", xbmc.LOGERROR)
        # No fallback - just return False
        return False