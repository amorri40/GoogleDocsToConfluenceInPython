#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from BeautifulSoup import BeautifulSoup
from HtmlAPI import get_css_from_tree
from ConfluenceAPI import get_confluence_server_and_token, get_confluence_page, post_to_confluence, \
    add_table_of_contents, warning_macro, send_content_to_confluence
import GDocAPI


vol1_doc = "1Lv6fxk4sfZcg7MCf0wCRNimbkDrzgGKrez2pPF1p8dQ"
vol2_doc = "1Xo3c6koLdJsGuhjdd_gWFXXMEGyvD-484TEzUsof-YM"
vol3_doc = "1CeyBNyt86hKOGtpbQkk3u9FaePlD71sm_zUgDMF5-oI"
vol4_doc = "1S546uVnR1hM-42oSPak4xJtIuT0cto_oFkMr9xuuwdA"


def setup_header(documentId):
    doc_content_header = warning_macro("Warning: This is Automatically Generated", """This Page is Automatically Generated from a section in the NewStartNotes Google Document. So any Changes you make to this wiki page will be replaced during the next sync.
         <a href='https://docs.google.com/document/d/%(documentId)s/edit'>Edit the Google Document instead!</a>""") % {'documentId' : documentId}

    doc_content_header += """<h1>Table of Contents</h1>""" + add_table_of_contents()
    return doc_content_header


def get_h1_text_from_html_with_only_one_h1(html):
    tree = BeautifulSoup(html)
    section_headers = tree.findAll('h1')
    assert (len(section_headers) == 1)
    return section_headers[0].text


def main(argv, documentId):
    mainParentId = '80643689'

    gdoc_content = GDocAPI.init(documentId)  #get_html_of_gdoc(nsn_doc,http)
    css_content_header = get_css_from_tree(BeautifulSoup(gdoc_content))

    sections = gdoc_content.split("<h1 class=")[2:]  #split and ignore the first section
    for section_html in sections:
        section_html = "<h1 class=" + section_html

        section_name = get_h1_text_from_html_with_only_one_h1(section_html)

        if len(section_name) < 2: continue  #make sure we don't have a section name smaller than 2
        print(section_name)

        doc_content_header=setup_header(documentId)
        send_content_to_confluence(section_html, section_name, mainParentId, "ENG",
                                   doc_content_header + css_content_header, "(NewStartNotes)")
        #break #only do 1

    print("Finished!")


if __name__ == '__main__':
    main(sys.argv,vol1_doc)
    main(sys.argv,vol2_doc)
    main(sys.argv,vol3_doc)
    main(sys.argv,vol4_doc)
