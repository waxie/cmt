import logging
import logging.config
import os
from sara_cmt import settings
class Logger:
  """
    A logging facility, implemented with the borg design pattern. Makes use of
    the Python logging lib, see: http://docs.python.org/library/logging.html
  """
  __shared_state = {}

  # Check for existence of a global logging object, otherwise make one
  if 'logger' not in __shared_state.keys():
    #logging.config.fileConfig(os.path.join(settings.CMTS_PATH, 'logging.conf'))
    logging.config.fileConfig(os.path.join('/home/sil/checkouts/subtrac/sil/trunk/cmts/sara_cmt', 'logging.conf'))
    __shared_state['logger'] = logging.getLogger('cli')

  def __init__(self):
    """
      Assigns the global __shared_state to __dict__ to be able to use the class
      like a singleton.
    """
    self.__dict__ = self.__shared_state

  def getLogger(self):
    """
      Returns the one and only logger instance (or state, to be exactly).
    """
    return self.__dict__['logger']
