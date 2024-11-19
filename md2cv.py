import argparse
import warnings
import os
import shutil
import codecs
import markdown2
from bs4 import BeautifulSoup, Tag

parser = argparse.ArgumentParser(description="A tool to convert markdown cv to html")

parser.add_argument('markdown', type=str, help='Path to the markdown file')
parser.add_argument('template', type=str, help='Name of a template without extension. Templates are stored in the templates/ directory')
parser.add_argument('-o', '--output', type=str, default="output/", help='Output folder. Default: ./output/')
args = parser.parse_args()

class SectionSoup(BeautifulSoup):
    """Basic BeautifulSoup with additional method new_section.

    """
    def new_section(self, parent=None, css_class='', title=None, content=None):
        """Create a section inside a parent tag. Insert two tags: Title and Content.

        Parameters
        ----------
        parent : bs4.Tag
            Parent tag.
        css_class : str
            CSS class prefix. Will be added before Title and Content 
        title : str or bs4.Tag
            String or tag that will be used as section ID.
        content : bs4.Tag, optional
            Tag with content that will be added to Content tag.

        Returns
        ------
        bs4.Tag
            A Content tag of the section.

        Warns
        --------
        warnings.UserWarning
            If the parent tag is not specified, the section will be added to the end of the document.

        """
        if isinstance(title, str):
            css_id = title.replace(' ', '_')
        elif isinstance(title, Tag):
            css_id = title.string.replace(' ', '_')
        else:
            css_id = ''
        if parent is None:
            parent = self
            warnings.warn('Parent tag is not specified. The section will be added to the end of the document.')
        section_tag = self.new_tag('div', attrs={'class' : css_class, 'id' : css_id})
        title_tag = self.new_tag('div', attrs = {'class' : css_class + 'Title'})
        content_tag = self.new_tag('div', attrs = {'class' : css_class + 'Content'})
        parent.append(section_tag)
        if title is not None:
            title_tag.append(title)
        if content is not None:
            content_tag.append(content)
        section_tag.extend([title_tag, content_tag])
        return content_tag

with open(args.markdown, 'r') as inf:
    html = markdown2.markdown(inf.read())
soup = BeautifulSoup(html, features='lxml')

with open('templates/{}.html'.format(args.template), 'r') as inf:
    template = SectionSoup(inf.read(), features='lxml')

main_tag = template.find(id = 'cv')
parent_tag = main_tag
for tag in soup.body.contents:
    if tag.name is not None:
        if tag.name == 'h1':
            segment = template.new_section(parent=main_tag, title=tag)
            parent_tag = segment
        elif tag.name == 'h2':
            section = template.new_section(parent=segment, css_class='Section', title=tag)
            parent_tag = section
        elif tag.name == 'h3':
            parent_tag = template.new_section(parent=section, css_class='Subsection', title=tag)
        elif tag.name == 'h4':
            parent_tag = template.new_section(parent=section, css_class='Subsection', title=tag)
        else:
            parent_tag.append(tag)

name_div = template.find(id='PERSONAL')
if name_div:
    name = name_div.find('p').text + ' - '
    template.title.insert(0, name)
    template.title.smooth()
    meta_description = template.find(attrs ={'name' : 'description'})
    meta_description['content'] = name + meta_description['content']

if not os.path.isdir(args.output):
    os.mkdir(args.output)

output_html = os.path.join(args.output, '{}.html'.format(args.template))
output_css = os.path.join(args.output, '{}.css'.format(args.template))

with codecs.open(output_html, 'w', 'utf-8-sig') as outf:
    outf.write(template.prettify())

shutil.copy('templates/{}.css'.format(args.template), output_css)