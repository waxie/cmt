from django.template import Template

from sara_cmt.logger import Logger
logger = Logger().getLogger()

class CMTTemplate(Template):
  """
    CMTTemplate class adds some smart functionalities to the Django Template.
  """
  def __init__(self, template_string, origin=None, name='<Unknown Template>'):
    """
      Template.__init__(self, template_string, origin=None, name='<Unknown Template>')
    """
    logger.info('Initializing CMT Template')
    Template.__init__(self, template_string, origin, name)

    logger.info('CMT Template has been initialized')

  def render(self, context):
    rendered = super(CMTTemplate, self).render(context)
    return rendered
