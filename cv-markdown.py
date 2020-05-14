import codecs
import markdown2
import warnings
from bs4 import BeautifulSoup

md_path = 'cv.md'

with open(md_path, 'r') as inf:
    html = markdown2.markdown(inf.read())
soup = BeautifulSoup(html)

class SectionSoup(BeautifulSoup):
    def new_section(self, parent=None, css_class='', title=None, content=None):
        if parent is None:
            parent = self
            warnings.warn('Parent tag is not specified. The section will be added to the end of the document')
        section_tag = self.new_tag('div', attrs={'class' : css_class})
        title_tag = self.new_tag('div', attrs = {'class' : css_class + 'Title'})
        content_tag = self.new_tag('div', attrs = {'class' : css_class + 'Content'})
        parent.append(section_tag)
        if title is not None:
            title_tag.append(title)
        if content is not None:
            content_tag.append(content)
        section_tag.extend([title_tag, content_tag])
        return content_tag

with open('templates/cv.html', 'r') as inf:
    template = SectionSoup(inf.read())

name = template.find(id = 'name')
name.append(soup.h1)
name_str = str(name.h1.string)

template.title.insert(0, name_str)
template.title.smooth()

meta_description = template.find(attrs ={'name' : 'description'})
meta_description['content'] = name_str + meta_description['content']

contacts = template.find(id = 'contacts')
first_p = soup.p.extract()
for line in first_p.string.split('\n'):
    title, content = line.split(':')
    template.new_section(parent=contacts, css_class='contact', title=title, content=content)

main_tag = template.find(id = 'main')
parent_tag = main_tag
for tag in soup.body.contents:
    if tag.name is not None:
        if tag.name == 'h2':
            section = template.new_section(parent=main_tag, css_class='section', title=tag)
            parent_tag = section
        elif tag.name == 'h3':
            parent_tag = template.new_section(parent=section, css_class='subsection', title=tag)
        else:
            parent_tag.append(tag)

output = 'cv.html'

with codecs.open(output, 'w', 'utf-8-sig') as outf:
    outf.write(template.prettify())