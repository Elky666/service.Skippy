import os
import xml.etree.ElementTree as ET
import xbmc
import xbmcaddon
import xbmcvfs
import settings

addon = xbmcaddon.Addon()

def get_intro_times(media_path):
    base, _ = os.path.splitext(media_path)
    base = xbmcvfs.translatePath(base)
    edl_file = base + ".edl"
    chapter_file = base + "_chapters.xml"

    xbmc.log(f"Checking for chapter file: {chapter_file}", level=xbmc.LOGDEBUG)

    if xbmcvfs.exists(edl_file):
        xbmc.log(f"Found EDL file: {edl_file}", level=xbmc.LOGDEBUG)
        with xbmcvfs.File(edl_file) as f:
            line = f.readline()
            if line:
                parts = line.strip().split()
                return float(parts[0]), float(parts[1])

    if xbmcvfs.exists(chapter_file):
        xbmc.log(f"Found chapter file: {chapter_file}", level=xbmc.LOGDEBUG)
        try:
            with xbmcvfs.File(chapter_file) as f:
                xml_data = f.read()
            tree = ET.ElementTree(ET.fromstring(xml_data))
            root = tree.getroot()
            for chapter in root.findall(".//ChapterAtom"):
                display = chapter.find("ChapterDisplay")
                if display is not None:
                    title = display.find("ChapterString")
                    if title is not None and settings.OPENING_KEYWORD.lower() in title.text.lower():
                        start = chapter.find("ChapterTimeStart").text
                        end = chapter.find("ChapterTimeEnd").text
                        return _parse_time(start), _parse_time(end)
        except Exception as e:
            xbmc.log(f"Error parsing chapter file: {e}", level=xbmc.LOGERROR)
    else:
        xbmc.log(f"Chapter file not found: {chapter_file}", level=xbmc.LOGWARNING)
    return None, None

def _parse_time(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)