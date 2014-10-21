#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from time import sleep
from ConfluenceAPI import send_content_to_confluence
import ConfluenceAPI
from HtmlAPI import get_body_string_from_html
import PersonalSettings
from CommonAPI import CommonAPI
path_to_auto_doc = PersonalSettings.AUTO_DOC_LOCATION

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

global_dict_of_pages = {}

def handle_file(file_path):
    global global_dict_of_pages
    file_path_without_root_location = file_path[len(path_to_auto_doc):]
    packages = file_path_without_root_location.split('/')
    if (len(packages) <2): return

    root_package = packages[0]
    sub_package = packages[1]
    if not sub_package == 'API': return
    if root_package.startswith('WG'): return

    #packages = packages[1:]
    for package in packages:
        if package == 'Test': return
        if package == 'Implementation': return
    page_name = root_package+"/"+sub_package
    #print "Store to:"+page_name
    section_name = "/".join(packages)
    if page_name in global_dict_of_pages:
        global_dict_of_pages[page_name].append(section_name)
    else:
        global_dict_of_pages[page_name] = [section_name]

CommonAPI.walk_directory(path_to_auto_doc, handle_file)
print global_dict_of_pages
print str(len(global_dict_of_pages))+" pages"

css_contents = CommonAPI.get_contents_of_file(path_to_auto_doc+'/stylesheet.css')
doc_header = ConfluenceAPI.add_css_macro(css_contents) + ConfluenceAPI.add_table_of_contents()
print css_contents

start_from = 'FrameworkEVA/API'

for page_name in global_dict_of_pages:
    if not start_from == '':
        if page_name == start_from: start_from = ''
        else: continue
    print page_name
    page_sections = global_dict_of_pages[page_name]
    body_contents=''
    for page_section in page_sections:
        print page_section
        body_contents += '<h1>'+page_section.replace('.html','')+'</h1>'
        page_contents = CommonAPI.get_contents_of_file( os.path.join(path_to_auto_doc, page_section) )
        body_contents += get_body_string_from_html(page_contents)
    #print body_contents

    send_content_to_confluence(body_contents, page_name.replace('/',' ') , "161320450",
                 '~amorrison',doc_header)
    sleep(30)
    #break # only do 1st page
