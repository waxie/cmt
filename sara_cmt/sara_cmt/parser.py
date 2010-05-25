import optparse


class Parser:
    """
        Optionparser, implemented with the borg design pattern.
    """
    __shared_state = {}

    # Check for existence of a global parser object, otherwise make one
    if 'parser' not in __shared_state.keys():
        __shared_state['parser'] = optparse.OptionParser()

    def __init__(self):
        self.__dict__ = self.__shared_state

    def getParser(self):
        return self.__dict__['parser']
