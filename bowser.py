#!/usr/bin/env python
import bottle
import time
import json
import os

from bottle_ext_jade import jade_template
from bottle import (
    route, run, 
    static_file, 
    template
  )

from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name

bottle.debug = True

HOST = '0.0.0.0'
PORT = '8080'
STATIC_DIR = [ 'file', '/Users/jamie/dev/' ]
SITE_NAME = 'demo site'
SHOW_DOTFILES = False

@route('/')
def index():
  return static_file('./bowser.html', root='./')

@route('/static/<path:path>')
def serve_static(path):
  return static_file(path, root='./static')


# XXX REMOVE Non-JS listings
@route('/listing')
def index():
  return jade_template(os.path.join(TEMPLATES_DIR,'index.tpl'), title=SITE_NAME) 

@route("/{0}/<path:path>".format(STATIC_DIR[0]))
def serve_file(path):
  return static_file(path, root=STATIC_DIR[1])

@route("/preview/<path:path>")
def preview_file(path):
  path = path.replace('//', '/')
  fullpath = os.path.join(STATIC_DIR[1], path)
  code = open(fullpath, 'r').read()
  try:
    lexer = get_lexer_for_filename(os.path.basename(fullpath))
    formatter = HtmlFormatter(style="tango", full=True)
    result = highlight(code, lexer, formatter)
    return result
  except:
    return serve_file(path)

@route("/dir/<path:path>")
def serve_dir(path):

      if path.startswith('/'):
        path = path.rpartition('/')[2]

      fullpath = os.path.join(STATIC_DIR[1],path)
      files = os.listdir(fullpath)
      filelist, dirs = [], []


      for f in files:
        if os.path.isdir(os.path.join(fullpath, f)):
          if not (f.startswith('.') and SHOW_DOTFILES is False):
            dirs.append(f)
        else:
          if not (f.startswith('.') and SHOW_DOTFILES is False):
            fmtime = time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(os.path.getmtime(os.path.join(fullpath,f))))
            filelist.append({ 'filename' : f, 'modtime' : fmtime})

      parent_dir = '/'.join(path.split('/')[:-2])
      if len(path.split('/')) > 2:
        if not parent_dir.endswith('/'): parent_dir = parent_dir + '/'
        if not parent_dir.startswith('/'): parent_dir = '/' + parent_dir
      else:
        parent_dir = '/'
      parent_dir = parent_dir.replace('//', '/')
      path = path.replace('//', '/')

      return {'parentdir': parent_dir,'curdir': path, 'breadcrumbs' : breadcrumb(path), 'files': filelist, 'dirs': dirs}


def breadcrumb(path):
    crumbs = []
    a,b = '',''
    for p in path.strip("/").split("/"):                                            
      b = p
      p = os.path.join(a,p)                                                         
      a = p                                                                         
      crumbs.append([p,b])
    return crumbs

if __name__ == '__main__':
  run(host=HOST, port=PORT, reloader=True)
