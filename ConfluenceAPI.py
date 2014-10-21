# -*- coding: utf-8 -*-
import xmlrpclib
from time import sleep
from BeautifulSoup import BeautifulSoup
from PersonalSettings import WIKI_USERNAME, WIKI_PASSWORD
import sqlite3

your_wiki_url = "https://yoursoftware.jira.com/wiki/rpc/xmlrpc"


def send_content_to_confluence(page_content, section_name, parent_id, space, doc_content_header='',
                               section_name_suffix='(Auto Gen)'):
    if doc_content_header == '':
        doc_content_header = get_default_warning()
    #print "Sending "+section_name+" to confluence, please wait..."
    #confluence_server, token = get_confluence_server_and_token()
    tree = BeautifulSoup(page_content)
    pretty_tree = str(tree)  #tree.prettify()
    return post_to_confluence(pretty_tree, section_name + ' '+section_name_suffix, parent_id, doc_content_header, space)

#######
# Macros
#######

def wrap_in_expand_macro(content):
    expand_prefix = """<ac:structured-macro ac:name="expand">
  <ac:parameter ac:name="">View Changes</ac:parameter>
  <ac:rich-text-body>"""
    expand_suffix = """</ac:rich-text-body>
  </ac:structured-macro>"""
    return expand_prefix + content + expand_suffix

def get_default_warning():
    return warning_macro('Warning Auto-Generated!','Do not modify this fine as any chnges you make will be overwritten')

def warning_macro(title,content):
    return """<ac:structured-macro ac:name="warning">
  <ac:parameter ac:name="icon">true</ac:parameter>
  <ac:parameter ac:name="title">"""+title+"""</ac:parameter>
  <ac:rich-text-body>
  """+content+"""
  </ac:rich-text-body>
</ac:structured-macro>"""

def add_css_macro(css_content):
    print css_content
    css_content_header = '<ac:macro ac:name="style"><ac:plain-text-body><![CDATA['
    css_content_header += css_content
    css_content_header += ']]></ac:plain-text-body></ac:macro>'
    return css_content_header


def add_task_list_macro(title='Tasks'):
    task_list = """<ac:structured-macro ac:name="tasklist">
    <ac:parameter ac:name="title">""" + title + """</ac:parameter>
    <ac:parameter ac:name="enableLocking">false</ac:parameter>
    <ac:parameter ac:name="width">100%</ac:parameter>
    <ac:parameter ac:name="promptOnDelete">true</ac:parameter>
    <ac:plain-text-body><![CDATA[||Completed||Priority||Locked||CreatedDate||CompletedDate||Assignee||Name||
  ]]></ac:plain-text-body>
  </ac:structured-macro>"""
    return task_list

def add_table_of_contents():
    return "<ac:structured-macro ac:name='toc'></ac:structured-macro>"

######
# Main Functions
######
confluence_server = None
confluence_token = None
set_confluence_server = False
def get_confluence_server_and_token():
    global confluence_server,confluence_token, set_confluence_server
    if not set_confluence_server:
        confluence_server = xmlrpclib.Server(your_wiki_url)
        confluence_token = confluence_server.confluence2.login(WIKI_USERNAME, WIKI_PASSWORD)
        set_confluence_server = True
    return confluence_server, confluence_token


def get_confluence_page(confluence_server, token, title, space="ENG"):
    try:
        nsn_page = confluence_server.confluence2.getPage(token, space, title)
        return nsn_page
    except:
        print("Error Page does not exist!")
        return ''

def get_confluence_page_id(title, space="ENG"):
    confluence_server, token = get_confluence_server_and_token()
    print "Getting page:"+title
    page = confluence_server.confluence2.getPage(token, space, title)
    page_id = page['id']
    print page_id
    return page_id



g_gdoc_content_header = """<b>This has been Auto-generated from Google Docs, So do NOT edit this page!!</b><br /><a href='https://docs.google.com/document/d/1Lv6fxk4sfZcg7MCf0wCRNimbkDrzgGKrez2pPF1p8dQ/edit'>Edit here instead</a> <p> This was generated in order to be searchable within the wiki, rather than having to search both the wiki and GDocs. Use Ctrl+ F to search for what you want within the document.</p><h1>Table of Contents</h1><ac:structured-macro ac:name='toc'></ac:structured-macro>"""


def post_to_confluence(gdoc_content, title, parentId, content_header=g_gdoc_content_header, space="ENG"):
    confluence_server, token = get_confluence_server_and_token()
    nsn_page = {}
    quit_due_to_creation_of_page = False  # we only want to create 1 new page at a time to avoid accidental spam!
    try:
        nsn_page = confluence_server.confluence2.getPage(token, space, title)
    except:
        print("ERROR: page not found")
        #quit_due_to_creation_of_page=True
    nsn_page['parentId'] = str(parentId)

    new_content = content_header + gdoc_content

    nsn_page['content'] = new_content
    nsn_page['title'] = title
    nsn_page['space'] = space
    try:
        stored_page = confluence_server.confluence2.storePage(token, nsn_page)
        page_id = stored_page['id']
        return page_id
    except xmlrpclib.ProtocolError, e:
        print e
        sleep(120)
        #page_id = post_to_confluence(gdoc_content, title, parentId, content_header,space)
        return -1 #page_id
    except xmlrpclib.Fault, e:
        print e

    if quit_due_to_creation_of_page:
        assert (False)
        exit();
