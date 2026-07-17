import os
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        self.in_nav = False
        
    def handle_starttag(self, tag, attrs):
        if tag in ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr', 'path']:
            return
        if tag == 'nav' and dict(attrs).get('class') == 'navbar':
            self.in_nav = True
        if self.in_nav:
            self.stack.append(tag)
            
    def handle_endtag(self, tag):
        if tag in ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr', 'path']:
            return
        if self.in_nav:
            if not self.stack:
                self.errors.append(f"Unexpected closing tag: {tag}")
            elif self.stack[-1] == tag:
                self.stack.pop()
            else:
                self.errors.append(f"Mismatched tag: expected </{self.stack[-1]}> but got </{tag}>")
                # try to recover
                if tag in self.stack:
                    while self.stack[-1] != tag:
                        self.stack.pop()
                    self.stack.pop()
        
        if tag == 'nav' and self.in_nav:
            self.in_nav = False

for file in os.listdir('.'):
    if file.endswith('.html'):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        parser = MyHTMLParser()
        try:
            parser.feed(content)
            if parser.errors:
                print(f"Errors in {file}:")
                for err in parser.errors:
                    print(f"  {err}")
        except Exception as e:
            print(f"Exception parsing {file}: {e}")
