import bleach
from HTMLParser import HTMLParser
import re


ALLOWED_TAGS = [
	'a',
	'abbr',
	'acronym',
	'b',
	'blockquote',
	'code',
	'em',
	'i',
	'li',
	'ol',
	'strong',
	'ul',
	'p',
	'br',
	'h3',
	'h4',
	'h5',
	'h6',
	'table',
	'tr',
	'th',
	'td',
	#'img',
]


def filter_img_src(name, value):

	if name == 'rel' and value == "display" :
		return True
	return False

ALLOWED_ATTRIBUTES = {
	'a': ['href', 'title'],
	'abbr': ['title'],
	'acronym': ['title'],
#	'img': ['src', 'rel', 'alt', 'title', 'style', 'class'],
}

ALLOWED_STYLES = []

# class MyHTMLParser(HTMLParser):
# 	def __init__(self, *args, **kwargs):
# 		HTMLParser.__init__(self, *args, **kwargs)
# 		self._text = []
# 		#self._tags_to_drop = set(tags_to_drop)
#
# 	def clear_text(self):
# 		self._text = []
#
# 	def get_text(self):
# 		return ''.join(self._text)
#
# 	def handle_starttag(self, tag, attrs):
# 		if tag == 'img':
# 			#print "Start tag:", tag
# 			for attr in attrs:
# 				if attr[0] == 'class':
# 					classes = attr[1].split()
# 					if 'inline-display' in classes:
#						self._text.append(self.get_starttag_text())
#		else:
#			self._text.append(self.get_starttag_text())

#	def handle_endtag(self, tag):
#		self._text.append('</{0}>'.format(tag))

#	def handle_data(self, data):
#		self._text.append(data)

#def texta(text):
#	p = re.compile(text, r'<img.*?/>')
#	print p.sub
#	return p.sub

def sanitize(text):
	"""Cleans the HTML received."""

	cleaned_text = bleach.clean(
		text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
		styles=ALLOWED_STYLES, strip=True)
	#parser = MyHTMLParser()
	#parser.feed(cleaned_text)
	#print parser.get_text()
	#re.comp
	#cleaned_text = texta(cleaned_text)
	return cleaned_text
