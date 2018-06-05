# -*- coding: utf-8 -*-
__author__ = 'wjjn3033'

import os
import re
import sys
import six
import json


def get_script_info(script_path):
    """extract info from script, like basename, __author__, __title__ and __desc__."""
    script_name = os.path.basename(script_path)
    pyfilename = script_name.replace(".air", ".py")
    pyfilepath = os.path.join(script_path, pyfilename)

    if not os.path.exists(pyfilepath) and six.PY2:
        pyfilepath = pyfilepath.encode(sys.getfilesystemencoding())
    with open(pyfilepath) as pyfile:
        pyfilecontent = pyfile.read()

    author, title, desc = get_author_title_desc(pyfilecontent)

    result_json = {"name": script_name, "author": author, "title": title, "desc": desc}
    return json.dumps(result_json)


def get_author_title_desc(text):
    """Get author title desc."""
    regex1 = r'__(?P<attr>\w+)__\s*=\s*(?P<val>"[^"]+"|"""[^"]+""")'
    regex2 = r"__(?P<attr>\w+)__\s*=\s*(?P<val>'[^']+'|'''[^']+''')"
    data1 = re.findall(regex1, text)
    data2 = re.findall(regex2, text)
    data1.extend(data2)
    file_info = dict(data1)
    author = strip_str(file_info.get("author", ""))
    title = strip_str(file_info.get("title", ""))
    desc = strip_str(file_info.get("desc", ""))
    return author, title, desc


def strip_str(string):
    """Strip string."""
    return string.strip('"').strip("'").strip()
