import re
import time
from adapterlib.keyword import Keyword

class DrawingKW(Keyword):
    def __init__(self):
        super(DrawingKW, self).__init__()
        pattern = re.compile("([0-9]+), ?([0-9]+)(, ?([0-9]+))?")
        self.attributePattern = pattern
        self.delay = -1
        self.shouldLog = False

    def execute(self):
        matcher = self.attributePattern.match(self.attributes)
        param_vec=[]
        for idx in [1,2,4]:
            if matcher.group(idx) :
                param_vec.append(int(matcher.group(idx)))
        rval = self.doDrawing(self._target, param_vec)
        self._target.update()
        return rval

class Delay(Keyword):
    def __init__(self):
        super(Delay,self).__init__()
        pattern = re.compile("([0-9]+)")
        self.attributePattern = pattern
        self.delay = -1
        self.shouldLog = False
    def execute(self):
        matcher = self.attributePattern.match(self.attributes)
        if matcher.group(1) :
            self._target.update()
            time.sleep(int(matcher.group(1)))
            self._target.update()
        return True

class HandleEvents(Keyword):
    def __init__(self):
        super(HandleEvents, self).__init__()
        self.delay = -1
        self.shouldLog = False
    def execute(self):
        self._target.update()
        return True
    

class Dot(DrawingKW):
    def __init__(self):
        super(Dot,self).__init__()

    def doDrawing(self, trg, params):
        def oval_points(x,y,r):
            return (x-r,y-r,x+r,y+r)

        if len(params) < 2 or len(params)>3:
            return False
        if len(params) == 2 :
            params.append(7)
        X,Y,R = params
        win=trg.window()
        win.create_oval(oval_points(X,Y,R), outline=trg.line,fill=trg.fill)
        return True

class MoveTo(DrawingKW):
    def __init__(self):
        super(MoveTo,self).__init__()
    def doDrawing(self, trg, params):
        if len(params)==2 :
            X,Y = params
            if None == X :
                return False
            trg.current_point=(X,Y)
            return True
        return False

class LineTo(DrawingKW):
    def __init__(self):
        super(LineTo,self).__init__()
    def doDrawing(self,trg, params):
        if len(params)==2 :
            X,Y = params
            if None == X :
                return False
            cX,cY = trg.current_point
            if None == cX :
                return False
            win=trg.window()
            fill=trg.line
            win.create_line((cX,cY,X,Y),
                            width=2, fill=fill,
                            smooth="true")
            trg.current_point=(X,Y)
            return True
        return False


class ColorChange(Keyword):
    def __init__(self):
        super(ColorChange,self).__init__()
        pattern = re.compile("([a-z]+)|(#[0-9A-Fa-f]{6})")
        self.attributePattern = pattern
        self.delay = -1
        self.shouldLog = False

    def get_param(self):
        matcher = self.attributePattern.match(self.attributes)
        fill = None
        if matcher.group(1) :
            fill = str(matcher.group(1))
        elif matcher.group(2):
            fill = str(matcher.group(2))
        return fill
    

class Fill(ColorChange):
    def __init__(self):
        super(Fill,self).__init__()

    def execute(self):
        fill = self.get_param()
        if None == fill :
            return False
        self._target.fill=fill
        return True

class Line(ColorChange):
    def __init__(self):
        super(Line,self).__init__()

    def execute(self):
        line = self.get_param()
        if None == line :
            return False
        self._target.line=line
        return True

