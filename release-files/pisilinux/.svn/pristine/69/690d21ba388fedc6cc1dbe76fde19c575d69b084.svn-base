#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from BeautifulSoup import BeautifulSoup

if __name__ == "__main__":
    html_path = sys.argv[1]

    source = open(html_path).read()
    soup = BeautifulSoup(source)

    title = soup.find("p", {"id": "title"})
    producttitle = soup.find("div", {"class": "producttitle"})

    source = source.replace(str(title), "").replace(str(producttitle), "")

    print source
    #open(html_path, "w").write(source)
