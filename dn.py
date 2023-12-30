import json
import urllib.request
import time
from xml.etree import ElementTree as ET

def get_items(uri):
    try:
        items = []
        response = urllib.request.urlopen(uri)
        data = json.loads(response.read().decode('utf-8'))  # Decode response to UTF-8
        for item in data.get('stories', []):
            result = parse_item(item)
            items.append(result)

        xml = generate_xml(items)
        return xml
    except Exception as e:
        print(f"Error fetching or processing data: {e}")
        return None

def generate_xml(items):
    try:
        xml_items = ET.Element('items')
        for item in items:
            xml_item = ET.SubElement(xml_items, 'item')
            for key, value in item.items():
                if key == 'uid' or key == 'arg':
                    xml_item.set(key, value)
                else:
                    child = ET.SubElement(xml_item, key)
                    child.text = value
        return ET.tostring(xml_items).decode('utf-8')  # Decode XML to UTF-8
    except Exception as e:
        print(f"Error generating XML: {e}")
        return None

def parse_item(item):
    return {
        'uid': f"{item['id']}-{time.time()}",
        'arg': item.get('url', ''),
        'title': item.get('title', ''),
        'subtitle': f"{item.get('vote_count', 0)} Votes  {item.get('num_comments', 0)} Comments",
        'icon': 'icon.png'
    }
