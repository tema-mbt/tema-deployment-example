import re
from adapterlib.keyword import Keyword

class IsTrue(Keyword):
    """
    Kw_IsTrue returns True or False depending on the parameter

    Usage::

        kw_IsTrue True
        kw_IsTrue False
    """
    def __init__(self):
        super(IsTrue,self).__init__()
        pattern = re.compile("((True)|(False))?")
        self.attributePattern = pattern
        self.delay = -1
        self.shouldLog = False

    def execute(self):

        matcher = self.attributePattern.match(self.attributes)
        if(matcher.group(2) != None):
            return True
        return False

## kw_Delay moved to kw_tkinter because updates needed.
