# -*- coding: utf-8 -*-
__title__ = "Mod5: transactions!"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0

_____________________________________________________________________
Description:

_____________________________________________________________________
Author: Jamie Hutchings"""                                           # Button Description shown in Revit UI


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ ⬇️ IMPORTS
# ==================================================
from Autodesk.Revit.DB import *
import contextlib, traceback
from Autodesk.Revit.UI.Selection import ISelectionFilter
from JHSnippets._jh_context_managers import *

# from Samples.FilteredElementCollector import all_levels

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ 📦 VARIABLES
# ==================================================
doc         = __revit__.ActiveUIDocument.Document   # type: Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc       = __revit__.ActiveUIDocument            # type: UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.


# GLOBAL VARIABLES

# - Place global variables here.


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ 🎯 MAIN
# ==================================================
class ISelectionFilter_Walls (ISelectionFilter):
    def AllowElement (self, element):
        if type (element) == Wall:
            return True
        return False

all_levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
# OR, in a plan view:
# target_level = doc.ActiveView.GenLevel
# print (all_levels[0].Id)
# print (target_level.Id)



with try_except ():
    pt = XYZ (0, 0, 0)
    pt2 = XYZ (10, 20, 30)

with transaction_wrapper (doc, __title__) as t:
    # Create a wall
    start    = XYZ(0, 0, 0)
    end      = XYZ(10, 10, 0)
    geomLine = Line.CreateBound(start, end)
    new_wall = Wall.Create(doc, geomLine, all_levels[0].Id, False)


# with ef_Transaction(doc, 'Create a Wall'):
#     # Create a wall
#     start    = XYZ(0, 0, 0)
#     end      = XYZ(10, 10, 0)
#     geomLine = Line.CreateBound(start, end)
#     new_wall = Wall.Create(doc, geomLine, all_levels[0].Id, False)
