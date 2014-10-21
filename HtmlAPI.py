from BeautifulSoup import BeautifulSoup
from pygments import highlight
from pygments.lexers import XmlLexer, SqlLexer
from pygments.formatters import HtmlFormatter


cdata_prefix = "<![CDATA["
cdata_suffix = "]]>"


def get_html_from_url(url, http):
    """

    :param url:
    :param http:
    :return:
    """
    resp, docs_content = http.request(url, "GET")
    return docs_content


def get_css_from_tree(tree):
    all_styles = tree.head.findAll('style')
    css_style = ""
    for stylee in all_styles:
        css_style += stylee.text
    css_content_header = '<ac:macro ac:name="style"><ac:plain-text-body><![CDATA['
    css_content_header += css_style
    css_content_header += ']]></ac:plain-text-body></ac:macro>'
    return css_content_header


def get_syntax_css():
    pygments_css = HtmlFormatter().get_style_defs()
    return pygments_css


def colour_syntax(code, syntax_type, use_inline_styles=False):
    formatter = HtmlFormatter(linenos=False, noclasses=use_inline_styles, nowrap=True)
    code_output = ""
    if syntax_type == "xml":
        code_output += highlight(code, XmlLexer(), formatter)
    elif syntax_type == "sql":
        code_output += highlight(code, SqlLexer(), formatter)
    else:
        code_output += code.replace('>', '&gt;').replace('<', '&lt;')
    return code_output


def create_link_tag(href, text):
    return '<a href="' + href + '">' + text + '</a>'

def get_body_string_from_html(html):
    tree = BeautifulSoup(html)
    result = str(tree.body)
    return result

def execute_function_over_body_html_from_url(url, function_to_execute, http):
    html = get_html_from_url(url, http)
    tree = BeautifulSoup(html)
    result_list = function_to_execute(tree.body) #handleElementRecursive
    return result_list
