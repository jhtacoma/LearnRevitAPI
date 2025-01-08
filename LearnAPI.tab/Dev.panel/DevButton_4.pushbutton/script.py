# -*- coding: utf-8 -*-
__title__ = "Selection stuff"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0

_____________________________________________________________________
Description:
Fooling around with Selection

_____________________________________________________________________
Author: Jamie Hutchings"""                                           # Button Description shown in Revit UI

# EXTRA: You can remove them.
__author__ = "Erik Frits"                                       # Script's Author
__helpurl__ = "https://www.youtube.com/watch?v=YhL_iOKH-1M"     # Link that can be opened with F1 when hovered over the tool in Revit UI.
# __highlight__ = "new"                                           # Button will have an orange dot + Description in Revit UI
__min_revit_ver__ = 2019                                        # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.

from Autodesk.Revit.DB.Architecture import Room

# from Samples.Selection import selected_elements

__max_revit_ver = 2022                                          # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
# __context__     = ['Walls', 'Floors', 'Roofs']                # Make your button available only when certain categories are selected. Or Revit/View Types.

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ ⬇️ IMPORTS
# ==================================================
# Regular + Autodesk
import os, sys, math, datetime, time                                    # Regular Imports
from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)
from Autodesk.Revit.DB import Transaction, FilteredElementCollector     # or Import only classes that are used.
from Autodesk.Revit.UI.Selection import ObjectType, PickBoxStyle, Selection

# pyRevit
from pyrevit import revit, forms                                        # import pyRevit modules. (Lots of useful features)

# Custom Imports
from JHSnippets._trace import trace

# .NET Imports
import clr                                  # Common Language Runtime. Makes .NET libraries accessible
clr.AddReference("System")                  # Reference System.dll for import.
from System.Collections.Generic import List # List<ElementType>() <- it's special type of list from .NET framework that RevitAPI requires
# List_example = List[ElementId]()          # use .Add() instead of append or put python list of ElementIds in parenthesis.

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ 📦 VARIABLES
# ==================================================
doc   = __revit__.ActiveUIDocument.Document   # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc = __revit__.ActiveUIDocument          # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
app   = __revit__.Application                 # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
PATH_SCRIPT = os.path.dirname(__file__)     # Absolute path to the folder where script is placed.

# GLOBAL VARIABLES

# - Place global variables here.

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝ 🧬 FUNCTIONS
# ==================================================

# - Place local functions here. If you might use any functions in other scripts, consider placing it in the lib folder.

# ╔═╗╦  ╔═╗╔═╗╔═╗╔═╗╔═╗
# ║  ║  ╠═╣╚═╗╚═╗║╣ ╚═╗
# ╚═╝╩═╝╩ ╩╚═╝╚═╝╚═╝╚═╝ ⏹️ CLASSES
# ==================================================

# - Place local classes here. If you might use any classes in other scripts, consider placing it in the lib folder.

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ 🎯 MAIN
# ==================================================
if __name__ == '__main__':

    # START CODE HERE

    # Use Transaction for Changes.
    t = Transaction(doc,__title__)  # Transactions are context-like objects that guard any changes made to a Revit model.
    # AVOID  placing Transaction inside of your loops! It will drastically reduce perfomance of your script.

    # You need to use t.Start() and t.Commit() to make changes to a Project.
    # t.Start()  # <- Transaction Start

    #- CHANGES TO REVIT PROJECT HERE


    # t.Commit()  # <- Transaction End

    selection = uidoc.Selection # type: Selection

    #1️⃣By el ids:
    # selected_element_ids = selection.GetElementIds()
    # selected_elements = [doc.GetElement(e_id) for e_id in selected_element_ids if type(doc.GetElement(e_id)) == Room]
    # print (selected_elements)

    # 2️⃣ By rectangle (selects elements directly, not their IDs!)
    # BY RECTANGLE PICKS MULTIPLE THINGS AT ONCE, BUT YOU ONLY GET ONE CHANGE TO INCLUDE IT IN YOUR SELECTION BOX
    # selected_elements = selection.PickElementsByRectangle("make a rectangle, dude!")
    # selected_elements = [el for el in selected_elements if type(el) == Wall]
    # print (selected_elements)


    # # 3️⃣ Pick object
    # selected_element = selection.PickObject(ObjectType.Element, "pick a wall!")
    # selected_elements = [el for el in selected_elements if type(el) == Wall]
    # print (selected_element)
    # print (doc.GetElement(selected_element))

    #
    # # # 4️⃣ Pick objectssss
    # PICKOBJECTS PICKS MULTIPLE THINGS AT ONCE, BUT YOU HAVE TO CLICK 'FINISH' TO PROCEED
    # ALSO, IT RETURNS *references*, NOT ELEMENTS THEMSELVES
    # selected_element_refs = selection.PickObjects(ObjectType.Element, "pick a wall!")
    # selected_elements = [el for el in [doc.GetElement(el_ref) for el_ref in selected_element_refs] if type(el) == Wall]
    # for el in selected_elements:
    #     print (el)

    # 5️⃣ Pick Point
    # sel_point = selection.PickPoint("Click somewhere please!")
    # print (sel_point)

    # 6️⃣ Pickbox
    # sel_points = selection.PickBox (PickBoxStyle.Directional, "Please pick two points!")
    # print (sel_points.Max, sel_points.Min)

    # 7️⃣ Set Selection in Revit UI
    new_selection = List [ElementId] ()
    new_selection.Add (ElementId (1399563))
    new_selection.Add (ElementId (1399682))
    new_selection.Add (ElementId (1399895))
    new_selection.Add (ElementId (1400001))

    # selection.SetElementIds (new_selection)
    selection.SetElementIds(new_selection)

    trace ("works a charm!")



    # # trace (selected_element_ids)