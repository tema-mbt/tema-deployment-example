#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import re
import time

import Tkinter as TK

binary_path=os.path.dirname(os.path.realpath(sys.argv[0]))
adapterlib_path=os.path.realpath(os.path.join(binary_path,'adapterlib'))

if adapterlib_path not in sys.path:
    sys.path.insert(0, adapterlib_path)

import adapterlib.main
from adapterlib.testrunner import TestRunner, Target

class CanvasTarget(Target):
    def __init__(self, name):
        super(CanvasTarget,self).__init__(name)
        self.__root = TK.Tk()
        self.__root.title("CanvasTarget: "+name)
        self.__canvas=TK.Canvas(self.__root,background="black",
                                width=500,height=500,
                                cursor="circle",takefocus=0)
        self.__canvas.pack(side=TK.TOP,fill=TK.BOTH,expand=1)
        self.__root.update()
        self.fill="yellow"
        self.line="gray"
        self.current_point = (None,None)

    def close(self):
        self.__root.title("Closing")
        self.update()
    def window(self):
        return self.__canvas
    def update(self):
        self.__root.update()

class CanvasTestRunner(TestRunner):
    def _setupTestAutomation(self):
        for name in self._targetNames:
            self._targets.append(CanvasTarget(name=name))
        return True

    def _cleanupTestAutomation(self):
        for t in self._targets:
            t.close()

import kw_generic
import kw_tkinter


if "__main__" == __name__ :
    am = adapterlib.main.AdapterMain()
    options, args = am.parseArguments()
    print options
    print args
    if options:
        testRunner = CanvasTestRunner(args,options.delay,options.record)
        am.runAdapter(testRunner, options)
