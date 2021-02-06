from xml.dom import minidom
import urllib.request
import sys
import re
  
DEFAULT_NAMESPACES = \
  (None, # RSS 0.91, 0.92, 0.93, 0.94, 2.0
  'http://purl.org/rss/1.0/', # RSS 1.0
  'http://my.netscape.com/rdf/simple/0.9/' # RSS 0.90
  )
  
DUBLIN_CORE = ('http://purl.org/dc/elements/1.1/',)

# Sample RSS link https://www.feedforall.com/sample.xml / sys.argv[1]
  
def load(rssURL):

  return minidom.parse(urllib.request.urlopen(rssURL))

def get_elements_by_tag_name(node, tagName, possibleNamespaces=DEFAULT_NAMESPACES):
  for namespace in possibleNamespaces:
    children = node.getElementsByTagNameNS(namespace, tagName)
    if len(children): 
      return children
  return []
  
def first(node, tagName, possibleNamespaces=DEFAULT_NAMESPACES):
  children = get_elements_by_tag_name(node, tagName, possibleNamespaces)
  return len(children) and children[0] or None
  
def text_of(node):
  return node and "".join([child.data for child in node.childNodes]) or ""

def get_rss_content(url):
  rss_document = load(url)
  result = ''
  for item in get_elements_by_tag_name(rss_document, 'item'):
      result += \
      'title: ' + text_of(first(item, 'title')) + '\n' + \
      'link: ' + text_of(first(item, 'link')) + '\n\n' + \
      'description: ' + text_of(first(item, 'description')) + '\n\n' + \
      'date: ' + text_of(first(item, 'date', DUBLIN_CORE)) + '\n' + \
      'author: ' + text_of(first(item, 'creator', DUBLIN_CORE)) + '\n'
  return result