# -*- coding: utf-8 -*-
__title__ = "Context Managers"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0

_____________________________________________________________________
Description:
context managers :)

_____________________________________________________________________
Author: Jamie Hutchings"""                                           # Button Description shown in Revit UI

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ ⬇️ IMPORTS
# ==================================================
from Autodesk.Revit.DB import Transaction
import contextlib, traceback
doc         = __revit__.ActiveUIDocument.Document   # type: Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ 🎯 MAIN
# ==================================================

@contextlib.contextmanager
def transaction_wrapper (doc, title, debug=False):
    """Context Manager that will initiate Transaction .Start() and .Commit() methods.
    In case of an error - it will .RollBack() transaction and display error message if debug = True.
    :param doc:   Document where Transaction should be created
    :param title: Name of Transaction
    :param debug: True - Display error messages \ False - Suppres error messages.
    Example:
    with ef_Transaction(doc, 'title', debug = True):
        #Changes Here"""
    with Transaction (doc, title) as t: # type:Transaction
        t.Start()
        try:
            yield # go do whatever the calling function wanted to do, then come back here when it's done
            t.Commit()
        except:
            if debug:
                print (traceback.format_exc())
            t.RollBack()

@contextlib.contextmanager
def try_except(debug=False):
    """Context Manager for using Try/Except statements.
    If case of an error it will display error message if debug = True.
    :param debug: True - Display error messages \ False - Suppress error messages.
    Example:
    with try_except(debug = True):
        #Code for Try statement here."""
    try:
        yield
    except:
        if debug:
            print(traceback.format_exc())