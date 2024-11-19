# cv-markdown

This script generates an HTML *curriculum vitae* from the Markdown file. It allows using a version control system to track changes in the cv. Moreover, the separation of content and design makes the updates easier.

```bash
usage: md2cv.py [-h] [-o OUTPUT] markdown template

A tool to convert markdown cv to html

positional arguments:
  markdown              Path to the markdown file
  template              Name of a template without extension. Templates are
                        stored in the templates/ directory

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output folder. Default: ./output/```