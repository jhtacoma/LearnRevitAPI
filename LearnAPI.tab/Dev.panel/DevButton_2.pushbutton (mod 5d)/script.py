# -*- coding: utf-8 -*-
__title__ = "Mod5: transactions!"                           # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0

_____________________________________________________________________
Description:

_____________________________________________________________________
Author: Jamie Hutchings"""                                           # Button Description shown in Revit UI

from symbol import factor

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ ⬇️ IMPORTS
# ==================================================
from Autodesk.Revit.DB import *
import sys
import contextlib, traceback
from Autodesk.Revit.UI.Selection import *
# from Autodesk.Revit.UI.Selection import ObjectType
from JHSnippets._jh_context_managers import *
from JHSnippets._trace import trace
from pyrevit import forms

# from Samples.FilteredElementCollector import all_levels

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ 📦 VARIABLES
# ==================================================
doc         = __revit__.ActiveUIDocument.Document   # type: Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc       = __revit__.ActiveUIDocument            # type: UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.


# GLOBAL VARIABLES

# - Place global variables here.

selection = uidoc.Selection #type:Selection

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ 🎯 MAIN
# ==================================================
class ISelectionFilter_Walls (ISelectionFilter):
    def AllowElement (self, element):
        if type (element) == Wall:
            return True
        return False

from Autodesk.Revit.DB import FailureDefinitionRegistry

# Transaction error handler
class SupressWarnings(IFailuresPreprocessor):
    def PreprocessFailures(self, failuresAccessor):
        try:
            failures = failuresAccessor.GetFailureMessages()

            for fail in failures: #type: FailureMessageAccessor
                severity    = fail.GetSeverity()
                description = fail.GetDescriptionText()
                fail_id     = fail.GetFailureDefinitionId() #type:FailureDefinitionId
                if severity == FailureSeverity.Warning:
                    # print ("captures: {}".format(description))
                    fdr = FailureDefinitionRegistry ()
                    print (FailureDefinitionRegistry.FindFailureDefinition(fdr, fail_id))

                    if fail_id == BuiltInFailures.GeneralFailures.DuplicateValue:
                        print ('looks like a duplicate')
                        failuresAccessor.DeleteWarning(fail)
                    elif fail_id == BuiltInFailures.RoomFailures.RoomsInSameRegion:
                        print ("silly ninny! rooms in same region!")
                    elif fail_id == BuiltInFailures.RoomFailures.RoomNotEnclosed:
                        print ("RoomNotEnclosed")
                    elif fail_id == BuiltInFailures.RoomFailures.RoomNotEnclosedAreas:
                        print ("RoomNotEnclosedAreas")
                        print (" warning: {}".format(description))
                    elif fail_id == BuiltInFailures.RoomFailures.RoomNotEnclosedRooms:
                        print ("RoomNotEnclosedRooms")
                        print (" warning: {}".format(description))
                    elif fail_id == BuiltInFailures.RoomFailures.RoomsInSameRegionRooms:
                        print ("RoomsInSameRegionRooms")
                        failuresAccessor.DeleteWarning(fail)
                        print (" warning: {}".format(description))
                    elif fail_id == BuiltInFailures.RoomFailures.RoomsInSameRegionAreas:
                        print ("	RoomsInSameRegionAreas")
                    elif fail_id == BuiltInFailures.RoomFailures.RoomsInSameRegionLoadAreas:
                        print ("	RoomsInSameRegionLoadAreas")
                    else:
                        print ("different warning: {}".format(description))
                        print ("id {}".format(fail_id))
        except:
            import traceback
            print (traceback.format_exc())
        return FailureProcessingResult.Continue


# my_filter = ISelectionFilter_Walls()
# selected_walls = selection.PickObjects(ObjectType.Element, my_filter,'Pick some walls')
try:
    selected_walls_refs = selection.PickObjects(ObjectType.Element, 'Pick some walls')
    selected_walls = [doc.GetElement(ref) for ref in selected_walls_refs]
except:
    print ("pick something, man!")
    import sys
    sys.exit()


for wall in selected_walls: #type:Wall
    t = Transaction(doc, 'Update Mark')
    t.Start()
    p_mark = wall.get_Parameter(BuiltInParameter.ALL_MODEL_MARK) #type:Parameter
    p_mark.Set('Warning2')

    doc.Delete (wall.Id)

    failure_handling_options = t.GetFailureHandlingOptions()
    failure_handling_options.SetFailuresPreprocessor(SupressWarnings())
    t.SetFailureHandlingOptions(failure_handling_options)
    t.Commit()


# selected_walls_refs = selection.PickObjects(ObjectType.Element, 'Pick some walls')
# selected_walls = [doc.GetElement(ref) for ref in selected_walls_refs]
# if not selected_walls:
#     print ("please pick something!")
#     import sys
#     sys.exit()

#
# forms.SelectFromList.show(
#         {'All': '1 2 3 4 5 6 7 8 9 0'.split(),
#          'Odd': '1 3 5 7 9'.split(),
#          'Even': '2 4 6 8 0'.split()},
#         title='MultiGroup List',
#         group_selector_title='Select Integer Range:',
#         multiselect=True
#     )


# all_levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
# print (all_levels)
# all_levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
# trace ()
# print (all_levels)
# sys.exit()


# all_levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
#
#
# selected_levels = forms.SelectFromList.show(all_levels,
#                                 multiselect=True,
#                                 name_attr='Name',
#                                 button_name='Select Levels')
# # Attempt to delete selected level to get a list of dependant Elements.
# # RollBack() so level is not deleted
#
# for level in selected_levels: # type: Level
#     print (level)
#     t = Transaction (doc, 'temp')
#     t.Start ()
#     returned_element_ids = doc.Delete (level.Id)
#     t.RollBack()
#     returned_elements = [doc.GetElement(e_id) for e_id in returned_element_ids]
#     e_types = {type(elem) for elem in returned_elements}
#     print ('{} has {} dependant Elements.'.format(level.Name, len(returned_elements)))
#     for x in e_types:
#         print ('--type:{}'.format(x))
#     print ('----')
#







#
# with try_except ():
#     pt = XYZ (0, 0, 0)
#     pt2 = XYZ (10, 20, 30)
#
# with transaction_wrapper (doc, __title__) as t:
#     # Create a wall
#     start    = XYZ(0, 0, 0)
#     end      = XYZ(10, 10, 0)
#     geomLine = Line.CreateBound(start, end)
#     new_wall = Wall.Create(doc, geomLine, all_levels[0].Id, False)


# with ef_Transaction(doc, 'Create a Wall'):
#     # Create a wall
#     start    = XYZ(0, 0, 0)
#     end      = XYZ(10, 10, 0)
#     geomLine = Line.CreateBound(start, end)
#     new_wall = Wall.Create(doc, geomLine, all_levels[0].Id, False)
