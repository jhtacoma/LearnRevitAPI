# -*- coding: utf-8 -*-
__title__ = "Mod4: Parameter stuff"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0

_____________________________________________________________________
Description:
Fooling around with Parameter read/write

_____________________________________________________________________
Author: Jamie Hutchings"""                                           # Button Description shown in Revit UI


# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ ⬇️ IMPORTS
# ==================================================

from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)
from Autodesk.Revit.UI.Selection import ObjectType, Selection

# .NET Imports
import clr                                  # Common Language Runtime. Makes .NET libraries accessible
clr.AddReference("System")                  # Reference System.dll for import.
from System.Collections.Generic import List # List<ElementType>() <- it's special type of list from .NET framework that RevitAPI requires

# pyRevit
from pyrevit import revit, forms                                        # import pyRevit modules. (Lots of useful features)

# Custom Imports
from JHSnippets._trace import trace

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ 📦 VARIABLES
# ==================================================
doc         = __revit__.ActiveUIDocument.Document   # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc       = __revit__.ActiveUIDocument          # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
selection   = uidoc.Selection # type: Selection

# GLOBAL VARIABLES

# - Place global variables here.


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ 🎯 MAIN
# ==================================================


# START CODE HERE

# Use Transaction for Changes.
# t = Transaction(doc,__title__)  # Transactions are context-like objects that guard any changes made to a Revit model.
# AVOID  placing Transaction inside of your loops! It will drastically reduce perfomance of your script.

# You need to use t.Start() and t.Commit() to make changes to a Project.
# t.Start()  # <- Transaction Start

#- CHANGES TO REVIT PROJECT HERE


# t.Commit()  # <- Transaction End


# Pick object
ref_picked_object = selection.PickObject(ObjectType.Element) # PickObject always returns a REFERENCE, not an ID
picked_object = doc.GetElement(ref_picked_object)
# print (picked_object.Parameters)

def get_stored_value (p):
    """
    Returns a value from a parameter based on its StorageType.
    """
    if p.StorageType == StorageType.String:
        if p.HasValue():
            return p.AsString()
        else:
            return ""
    elif p.StorageType == StorageType.Double:
        return p.AsDouble()
    elif p.StorageType == StorageType.Integer:
        return p.AsInteger()
    elif p.StorageType == StorageType.ElementId:
        return p.AsElementId()
    else:
        return 'not string, double, integer, or elementID!'

def read_param(p, return_its_value=False):
    try:
        print ("Name: {}".format(p.Definition.Name))
        print ("ParameterGroup: {}".format(p.Definition.ParameterGroup))
        print ("BuiltInParameter: {}".format(p.Definition.BuiltInParameter))
        print ("IsReadOnly: {}".format(p.IsReadOnly))
        print ("HasValue: {}".format(p.HasValue))
        print ("IsShared: {}".format(p.IsShared))
        print ("StorageType: {}".format(p.StorageType))
        print ("Value: {}".format(get_stored_value(p)))
        print ("AsValueString: {}".format(p.AsValueString()))
        trace ()
        if p.Definition.Name == "Comments":
            print ("found the comments!!!!!!!!!!!!!!!")
    except:
        print ('nope!')
    if return_its_value:
        try:
            return get_stored_value(p)
        except:
            return "NO VALUE!"

# FOR BUILT-IN PARAMETERS
comments    = picked_object.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
mark        = picked_object.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
el_type     = picked_object.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM)
area        = picked_object.get_Parameter(BuiltInParameter.HOST_AREA_COMPUTED)
offset      = picked_object.get_Parameter(BuiltInParameter.WALL_BASE_OFFSET)


# print (read_param(comments))
# print (read_param(mark))
# print (read_param(el_type))
# print (read_param(area))
# print (read_param(offset))

# print ("Type mark: {}".format(picked_object.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_MARK)))

read_param(comments)
read_param(mark)
read_param(el_type)
read_param(area)
read_param(offset)
#
print ("comments val is {}".format(read_param(comments, True)))

with Transaction (doc, 'mychanger') as t: # type: Transaction

    t.Start()

    comments.Set(read_param(comments, True) + " NEW!")
    mark.Set(read_param(mark, True) + " NEW!")
    el_type.Set(ElementId(333631)) # note that, NATURALLY, you don't just set it to 333631, but to ElementId(333631)!
    # area.Set (25.55)
    # area.Set (-1.5)
    # area.Set(read_param(area, True) + " NEW!")

    t.Commit()


read_param(comments)
read_param(mark)
# read_param(el_type)
# read_param(area)