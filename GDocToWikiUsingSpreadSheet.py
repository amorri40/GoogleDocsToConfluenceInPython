#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gspread
import GDocAPI
from ConfluenceAPI import get_confluence_server_and_token, get_confluence_page, post_to_confluence
from BeautifulSoup import BeautifulSoup
from PersonalSettings import GDOC_USERNAME, GDOC_PASSWORD
from HtmlAPI import get_css_from_tree

# Login with your Google account
gc = gspread.login(GDOC_USERNAME, GDOC_PASSWORD)

worksheet = gc.open_by_key('0Ald2AYWnsGhXdHV6MVhIVm80RnBHNHBIdVg2Q3dTNXc').sheet1

doc_content_header="""<b>This is has been Auto-generated from docs.google.com, So do NOT edit this page!!</b>"""
#doc_content_header='<ac:macro ac:name="composition-setup"><ac:parameter ac:name="import.css">3</ac:parameter></ac:plain-text-body></ac:macro>'
#doc_content_header+='<ac:macro ac:name="style"><ac:plain-text-body><![CDATA[ol{margin:0;padding:0}.c6{max-width:468pt;background-color:#ffffff;padding:72pt 72pt 72pt 72pt}.c2{direction:ltr}.c1{font-style:italic}.c4{height:11pt}.c3{font-size:12pt}.c0{font-weight:bold}.c5{font-size:14pt}.title{widows:2;padding-top:0pt;line-height:1.15;orphans:2;text-align:left;color:#000000;font-size:21pt;font-family:"Trebuchet MS";padding-bottom:0pt;page-break-after:avoid}.subtitle{widows:2;padding-top:0pt;line-height:1.15;orphans:2;text-align:left;color:#666666;font-style:italic;font-size:13pt;font-family:"Trebuchet MS";padding-bottom:10pt;page-break-after:avoid}li{color:#000000;font-size:11pt;font-family:"Arial"}p{color:#000000;font-size:11pt;margin:0;font-family:"Arial"}h1{widows:2;padding-top:10pt;line-height:1.15;orphans:2;text-align:left;color:#000000;font-size:16pt;font-family:"Trebuchet MS";padding-bottom:0pt;page-break-after:avoid}h2{widows:2;padding-top:10pt;line-height:1.15;orphans:2;text-align:left;color:#000000;font-size:13pt;font-family:"Trebuchet MS";font-weight:bold;padding-bottom:0pt;page-break-after:avoid}h3{widows:2;padding-top:8pt;line-height:1.15;orphans:2;text-align:left;color:#666666;font-size:12pt;font-family:"Trebuchet MS";font-weight:bold;padding-bottom:0pt;page-break-after:avoid}h4{widows:2;padding-top:8pt;line-height:1.15;orphans:2;text-align:left;color:#666666;font-size:11pt;text-decoration:underline;font-family:"Trebuchet MS";padding-bottom:0pt;page-break-after:avoid}h5{widows:2;padding-top:8pt;line-height:1.15;orphans:2;text-align:left;color:#666666;font-size:11pt;font-family:"Trebuchet MS";padding-bottom:0pt;page-break-after:avoid}h6{widows:2;padding-top:8pt;line-height:1.15;orphans:2;text-align:left;color:#666666;font-style:italic;font-size:11pt;font-family:"Trebuchet MS";padding-bottom:0pt;page-break-after:avoid}]]></ac:plain-text-body></ac:macro>'

def postToConfluence(page_content, section_name, parentId, space, doc_content_header):
	confluence_server,token = get_confluence_server_and_token()
	
	tree = BeautifulSoup(page_content)
	pretty_tree = tree.body.prettify()
	css_content_header=get_css_from_tree(tree)
	
	post_to_confluence(pretty_tree,section_name+" (docs.google.com)",parentId,doc_content_header+css_content_header,space)


list_of_lists = worksheet.get_all_values()

i=0
for row in list_of_lists:
	i=i+1
	if i==1: continue #the first one is the heading row!
	gdoc_url = row[1]
	confluence_parent = row[2].replace('https://yoururl.jira.com/wiki/pages/viewpage.action?pageId=','').replace(' ','')
	title = row[3]
	space= row[4]
	gdoc_id = gdoc_url.replace('https://docs.google.com/document/d/','').replace(' ','')
	edit_position = gdoc_id.index('/edit')
	
	if edit_position>2:
		gdoc_id = gdoc_id[:edit_position]
	
	print 'gdoc_id:'+gdoc_id + ' confluence_parent:'+confluence_parent+"\n"
	html_output = GDocAPI.init(gdoc_id)
	#print html_output
	full_content_header=doc_content_header+"<a href='+"+gdoc_url+"'>Edit here instead</a><br />"
	postToConfluence(html_output,title,confluence_parent,space,doc_content_header)
	