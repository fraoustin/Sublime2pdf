# -*- coding: utf-8 -*-

# Copyright 2012 Frédéric Aoustin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations
# under the License.





import sys
import os, os.path
import tempfile
import zipfile
import glob
import shutil
import traceback

import sublime
import sublime_plugin

#I have a problem with reportlab ans rst2pdf module
# import zip module is not ok
# extract module for add zip and module in sys.path
zip_decompress = ['reportlab*.zip', 'rst2pdf*.zip']

pkg_path = os.path.abspath(os.path.dirname(__file__))
libs_path = os.path.join(pkg_path, 'libs')
sys.path.insert(0, libs_path)

for i in zip_decompress:
    try:
        name = glob.glob(os.path.join(libs_path,i))[0]
        zipd = os.path.join(libs_path,'.'.join(os.path.basename(name).split('.')[:-1]))
        if os.path.isdir(zipd):
            shutil.rmtree(zipd)
        os.makedirs(zipd)
        zipf = zipfile.ZipFile(name)
        zipf.extractall(zipd)
        zipf.close()
        os.remove(name)
    except:
        pass

for i in os.listdir(libs_path):
    lib_path = os.path.join(libs_path, i)
    if lib_path not in sys.path:
        sys.path.insert(0, lib_path)



from pygments.lexers._mapping import LEXERS
import rst2pdf
import rst2pdf.createpdf

RST_CODE = '.. code-block:: %s\n\n'
RST_CODE_UNDEFINED = '::\n\n'


def get_language(syntax, ext):
    """
    search language of pygments by syntax and after by extension
    """
    if len(ext) == 0 : ext='none'
    if ext[0] == '.': ext = '*' + ext
    if ext[0] != '*': ext = '*.' + ext
    s = os.path.basename(os.path.join(sublime.packages_path(),syntax))
    if s[-len('.tmLanguage'):] == '.tmLanguage':
        s = s[:-len('.tmLanguage')]
        for module_name, name, aliases, exts, mine in LEXERS.itervalues():
            if s.lower() in aliases:
                return s.lower()
        for module_name, name, aliases, exts, mine in LEXERS.itervalues():
            if ext in exts:
                return aliases[0]
    return None


class ToPdfCommand(sublime_plugin.TextCommand):

    def run(self, edit):        
        try:
            self.settings = sublime.load_settings('2pdf.sublime-settings')
            package_dir = os.path.join(sublime.packages_path(), __name__)
            stylesheet_code = self.settings.get('stylesheet-code')
            if stylesheet_code != None and len(stylesheet_code) > 0:
                stylesheet_code = os.path.join(package_dir, stylesheet_code)
                if os.path.isfile(stylesheet_code) == False:
                    stylesheet_code = None
            else:
                stylesheet_code = None  
            stylesheet_rst = self.settings.get('stylesheet-rst')
            if stylesheet_rst != None and len(stylesheet_rst) > 0:
                stylesheet_rst = os.path.join(package_dir, stylesheet_rst)
                if os.path.isfile(stylesheet_rst) == False:
                    stylesheet_rst = None
            else:
                stylesheet_rst = None  
            view = self.view
            syntax = view.settings().get('syntax')
            encoding = view.encoding()
            if view.file_name() != None:
                ext=os.path.splitext(view.file_name())[1]
            else:
                ext=""
            regions = view.sel()
            # if there are more than 1 region or region one and it's not empty
            if len(regions) > 1 or not regions[0].empty():
                for region in view.sel():
                    if not region.empty():
                        s = view.substr(region)
                        s = self._run(s, syntax, encoding, ext, stylesheet_code, stylesheet_rst)
            else:   #format all text
                alltextreg = sublime.Region(0, view.size())
                s = view.substr(alltextreg)
                s = self._run(s, syntax, encoding, ext, stylesheet_code, stylesheet_rst)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            sublime.error_message(str(' '.join(formatted_lines)))

    def _run(self, s, syntax=None, encoding="utf-8", ext="", stylesheet_code=None, stylesheet_rst=None):
        try:
            s = s.encode(encoding)
        except:
            s = s.encode("utf-8")
        temp = tempfile.NamedTemporaryFile(delete=False)
        if get_language(syntax,ext) != 'restructuredtext':
            if get_language(syntax,ext) != None:
                temp.write(RST_CODE % get_language(syntax,ext))
            else:
                temp.write(RST_CODE_UNDEFINED)
            for i in s.split('\n'):
                temp.write('\t%s\n' % i)
            stylesheet = stylesheet_code
        else:
            temp.write(s)
            stylesheet = stylesheet_rst
        temp.close()        
        if stylesheet != None:
             stylesheets=[stylesheet]
        else:
             stylesheets=[]
        infile = open(temp.name)
        outfile = temp.name + '.pdf'
        if self.view.file_name() != None:
            src_path = os.path.dirname(self.view.file_name())
        else:
            src_path = os.getcwd()
        rst2pdf.createpdf.RstToPdf(stylesheets=stylesheets,
                             language='fr_FR',
                             basedir=src_path,
                             breaklevel=self.settings.get('breaklevel')
                                ).createPdf(text=infile.read(),
                                    source_path=infile.name,
                                    output=outfile,
                                    compressed=self.settings.get('compressed'))
        os.startfile(outfile)
        infile.close()
        os.remove(temp.name)
        #sublime.message_dialog(stylesheet)
        return 1