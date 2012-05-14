import logging
import logging.config


class Logger:
    """
        A logging facility, implemented with the borg design pattern. Makes
        use of the Python logging lib, see:
            http://docs.python.org/library/logging.html
    """
    __shared_state = {}

    # Check for existence of a global logging object, otherwise make one
    if 'logger' not in __shared_state.keys():
        #TODO: think about a (better) way to make this dynamic:
        import site

        if site.sys.prefix in [ '/usr', '/' ]:
            ETC_PREPEND = ''
        else:
            ETC_PREPEND = site.sys.prefix

        logging.config.fileConfig('%s/etc/cmt/logging.conf'%ETC_PREPEND)
        __shared_state['logger'] = logging.getLogger('cli')

    def __init__(self):
        """
            Assigns the global __shared_state to __dict__ to be able to use
            the class like a singleton.
        """
        self.__dict__ = self.__shared_state

    def getLogger(self):
        """
            Returns the only logger instance (or state, to be exactly).
        """
        return self.__dict__['logger']
