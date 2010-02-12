from django.template import Template

print "Loading template.py"

class SmartTemplate(Template):
  """
    Smart Template class adds some functionalities to the Django Template.
  """
  def __init__(self, template_string, origin=None, name='<Unknown Template>'):
    """
      Template.__init__(self, template_string, origin=None, name='<Unknown Template>')
    """
    # Parse the first lines of the template for meta-info like:
    #  - What should be loaded as Context?
    #  - Where should the output be saved? What's the path
    #  - What daemon should be restarted/-loaded?
    #  - etc...
    print "Initializing Smart Template"
    #template_string = 
    Template.__init__(self, template_string, origin, name)

    print "Smart Template has been initialized"

  def render(self, context):
    rendered = super(SmartTemplate, self).render(context)

    # Save rendered as a file to the given path

