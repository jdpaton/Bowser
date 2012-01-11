import functools

from bottle import HTTPError, SimpleTemplate, BaseTemplate, view, template
from pyjade import Root, Environment

import bottle

class BottleEnvironment(Environment):

  auto_close_tags = {'for': 'endfor',
                       'if': '',
                       'else': 'end',
                    }

  may_contain_tags = {'if': ['elif','else'], 
                      'for': ['empty'], 
                      'with': ['with'] }
 
  code_tags = ('include', 'extends', 'for', 'block', 'if', 'else', 'elif', 'filter', 'with', 'while', 'set','macro')

  def __init__(self, *args, **kwargs):
     for dictarg in args: kwargs.update(dictarg)
     self.vars = kwargs

  def tag_begin(self, node):
    return '%%%s:\n' % (node.statement)

  def tag_end(self, node):
        print dir(node)
        return '%%%s' % node.closetag if node.closetag else ''

  def var(self, node):
    try:
      self.vars[node.raw]
    except KeyError:
      raise HTTPError(output="Jade Template: Unknown variable: %s" % node.raw)
    bottle.TEMPLATES.clear() 
    return '%s' % (self.vars[node.raw])

class JadeTemplate(BaseTemplate):

    def prepare(self, **options):
      if self.source:
        self.tpl = Root(self.source, env=BottleEnvironment)

    def render(self, *args, **kwargs):
      for dictarg in args: kwargs.update(dictarg)
       
      if self.source:  
        return unicode(Root(self.source, env=BottleEnvironment() ))
      elif self.filename:
        self.source = open(self.filename, 'r').read()
        tpl = unicode(Root(self.source, env=BottleEnvironment(kwargs) ))
        print tpl
        return SimpleTemplate(tpl).render(kwargs)


jade_view = functools.partial(view, template_adapter=JadeTemplate)
jade_template = functools.partial(template, template_adapter=JadeTemplate)
