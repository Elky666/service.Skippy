import xbmc
import xbmcaddon

# Global variables
AUTO_SKIP = None
AUTO_SKIP_DELAY = None
ENABLE_TVSHOW = None
ENABLE_MOVIES = None
OPENING_KEYWORD = None

def load_settings():
    """Load settings from addon"""
    global AUTO_SKIP, AUTO_SKIP_DELAY, ENABLE_TVSHOW, ENABLE_MOVIES, OPENING_KEYWORD
    
    try:
        addon = xbmcaddon.Addon()
        
        # Use the correct setting IDs from your settings.xml
        AUTO_SKIP = addon.getSettingBool("enable_autoskip")
        AUTO_SKIP_DELAY = addon.getSettingInt("autoskip_delay")
        ENABLE_TVSHOW = addon.getSettingBool("enable_tvshow")
        ENABLE_MOVIES = addon.getSettingBool("enable_movies")
        
        # Add the opening keyword setting
        OPENING_KEYWORD = addon.getSetting("chapter_keyword") or "Opening"
        
        xbmc.log(f"Settings loaded - AUTO_SKIP: {AUTO_SKIP}, DELAY: {AUTO_SKIP_DELAY}, TV: {ENABLE_TVSHOW}, MOVIES: {ENABLE_MOVIES}, KEYWORD: {OPENING_KEYWORD}", xbmc.LOGINFO)
        
    except Exception as e:
        xbmc.log(f"Error loading addon settings: {e}", xbmc.LOGERROR)
        # Set defaults
        AUTO_SKIP = True
        AUTO_SKIP_DELAY = 10
        ENABLE_TVSHOW = True
        ENABLE_MOVIES = True
        OPENING_KEYWORD = "Opening"

# Load settings on import
load_settings()