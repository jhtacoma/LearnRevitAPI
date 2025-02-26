# -*- coding: utf-8 -*-
__title__ = "Mod4: Wall params"                           # Name of the button displayed in Revit UI
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
from pyrevit.forms import alert
from Autodesk.Revit.DB import *
# from Autodesk.Revit.UI import Selection
# from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter
# pyRevit
from pyrevit import revit, forms                                        # import pyRevit modules. (Lots of useful features)
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,
                          Separator, Button, CheckBox)
# from Samples.Selection import el_id

clr.AddReference("System")                  # Reference System.dll for import.
from System.Collections.Generic import List # List<ElementType>() <- it's special type of list from .NET framework that RevitAPI requires


# Custom Imports
from JHSnippets._trace import trace

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ 📦 VARIABLES
# ==================================================
doc         = __revit__.ActiveUIDocument.Document   # type: Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc       = __revit__.ActiveUIDocument            # type: UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
selection   = uidoc.Selection                       # type: Selection

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




# 1️⃣ GET THE SELECTED WALLS

# first is my method, not using ISelectionFilter:
# refs_sel_walls = uidoc.Selection.PickObjects (ObjectType.Element, "SELECT WALL(S)")
# sel_walls = [el for el in [doc.GetElement(el_ref) for el_ref in refs_sel_walls] if type(el) == Wall]

# now it's Erik's method, with ISelectionFilter:
def get_selected_walls ():
    # get current selection
    sel_ids = selection.GetElementIds()
    sel_walls = [el for el in [doc.GetElement(el_id) for el_id in sel_ids] if type(el) == Wall]

    # if no walls already selected, prompt user with PickObject()
    if not sel_walls:
        alert ("Please select one or more walls.", )
        try:
            picked_refs = selection.PickObjects (ObjectType.Element, ISelectionFilter_Walls(), "Pick some walls!")
            sel_walls = [doc.GetElement(ref) for ref in picked_refs]
        except:
            pass

    return sel_walls


sel_walls = get_selected_walls()

def get_value_of_name (the_parameter):
    """
    Returns value of one of those inaccessible 'names' of certain elements and parameters.
    """
    return Element.Name.GetValue(the_parameter)

# for w in sel_walls: # type: # Wall
#
#     # print (read_param(w.get_Parameter(BuiltInParameter.WALL_BASE_CONSTRAINT), True))
#     # print ('Wall type: {}'.format(Element.Name.__get__(w)))
#     # print ('Wall type: {}'.format(Element.Name.GetValue(w)))
#     print ('Wall type: {}'.format(get_value_of_name(w)))

# 2️⃣ GET THE USER'S INPUT (CREATE UI FORM FOR LEVELS)

def get_user_input():
    """
    Function to get user input for wall levels.
    Returns a dictionary that may include:
        checkbox_base
        combobox_level_base
        checkbox_top
        combobox_level_top
    """
    all_levels = FilteredElementCollector (doc).OfClass(Level).ToElements() # remember FilteredElementCollector isn't a list of anything; it's essentially a pointer. Therefore we always have to invoke ToElements() to get the actual elements!
    # levels_dict = {}
    # for level in all_levels: #type: Level
    #     levels_dict [level.Name] = level.Elevation
    # levels_dict = {level.Name : level for level in all_levels}
    levels_dict = {level.Name : level for level in all_levels}

    components = [Label('Change wall levels:'),
                  CheckBox('checkbox_base', 'Modify base?'),
                  ComboBox('combobox_level_base', levels_dict),
                  CheckBox('checkbox_top', 'Modify top?'),
                  ComboBox('combobox_level_top', levels_dict),
                  Separator(),
                  Button('Select')]
    form = FlexForm('Pick wall vertical extents', components)
    form.show()
    # try:
    #     if not form.values:
    #         forms.alert("No levels selected.\nPlease try again", exitscript=True)
    #     else:
    #         print ("about to return")
    #         return form.values
    # except:
    #     print ('about to pass')
    #     pass
    if not form.values:
        forms.alert("No levels selected.\nPlease try again", exitscript=True)
    return form.values


user_input = get_user_input()
# new_base_level      = user_input ['combobox_level_base'].Elevation
new_base_level      = user_input ['combobox_level_base']  # type:Level
are_modifying_base  = user_input ['checkbox_base']
new_top_level       = user_input ['combobox_level_top'] # type:Level
are_modifying_top   = user_input ['checkbox_top']

# print (user_input)
# User selects `Opt 1`, types 'Wood' in TextBox, and select Checkbox
# form.values
# {'combobox_level_base': [a level element], 'combobox_level_top': [a level element], 'checkbox_base': True}

# Start transaction
t = Transaction(doc, 'Modify Wall levels')
t.Start()

# 3️⃣ CALCULATED NEW OFFSETS FOR NEW LEVELS
for wall in sel_walls: #type : Wall

    try:
        # first, get the parameters
        p_base_level = wall.get_Parameter (BuiltInParameter.WALL_BASE_CONSTRAINT) # type: Parameter # -- it IS a parameter, NOT the value of WALL_BASE_CONSTRAINT!
        p_base_offset = wall.get_Parameter (BuiltInParameter.WALL_BASE_OFFSET) # type: Parameter
        p_top_level = wall.get_Parameter (BuiltInParameter.WALL_HEIGHT_TYPE) # type: Parameter
        p_top_offset = wall.get_Parameter (BuiltInParameter.WALL_TOP_OFFSET) # type: Parameter
        p_wall_height = wall.get_Parameter (BuiltInParameter.WALL_USER_HEIGHT_PARAM) # type: Parameter



        # next, extract the values FROM those parameters...
        base_level = doc.GetElement (p_base_level.AsElementId()) # type: Level
        base_offset = p_base_offset.AsDouble() # type: Double
        # top_level = doc.GetElement (p_top_level.AsElementId()) # type: Level
        # top_offset = p_top_offset.AsDouble() # type: Double
        wall_height = p_wall_height.AsDouble() # type: Double


        # calculate elevations
        wall_base_elevation = base_level.Elevation + base_offset
        wall_top_elevation= wall_base_elevation + wall_height

        # 4️⃣ MODIFY BASE/TOP LEVELS AND OFFSETS


        # calculate any modifications
        if are_modifying_base:
            offset_new = wall_base_elevation - new_base_level.Elevation
            p_base_level.Set (new_base_level.Id)
            p_base_offset.Set (offset_new)

        if are_modifying_top:
            offset_new = wall_top_elevation - new_top_level.Elevation
            p_top_level.Set (new_top_level.Id)
            p_top_offset.Set (offset_new)

    except:
        import traceback
        print (traceback.format_exc(), wall.Id)
t.Commit()





