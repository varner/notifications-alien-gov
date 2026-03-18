import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import os

FEED_FILE = "feed.xml"

def load_or_create_feed():
    try:
        tree = ET.parse(FEED_FILE)
        return tree
    except (FileNotFoundError, ET.ParseError):
        # Build a minimal valid RSS skeleton
        root = ET.fromstring("""<rss version="2.0">
  <channel>
    <title>Site Status Feed</title>
    <link>https://aliens.gov</link>
    <description>Uptime notifications</description>
  </channel>
</rss>""")
        return ET.ElementTree(root)

def add_item(tree, status):
    channel = tree.getroot().find("channel")
    item = ET.SubElement(channel, "item")

    now = datetime.now(timezone.utc)
    ET.SubElement(item, "title").text = f"Site status: {status} — {now.strftime('%Y-%m-%d %H:%M UTC')}"
    ET.SubElement(item, "pubDate").text = now.strftime("%a, %d %b %Y %H:%M:%S +0000")
    ET.SubElement(item, "guid").text = now.isoformat()

    # Keep only the 50 most recent items
    items = channel.findall("item")
    for old in items[:-50]:
        channel.remove(old)

tree = load_or_create_feed()
status_code = os.environ.get("STATUS_CODE", "unknown")
add_item(tree, status_code)
ET.indent(tree, space="  ")
tree.write(FEED_FILE, encoding="unicode", xml_declaration=True)
print("feed.xml updated.")