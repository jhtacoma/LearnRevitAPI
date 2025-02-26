# -*- coding: utf-8 -*-
__title__ = "Mod6: FEC basics"                           # Name of the button displayed in Revit UI
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

# from Samples.Selection import selected_stuff



# from Samples.FilteredElementCollector import all_levels

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ 📦 VARIABLES
# ==================================================
doc         = __revit__.ActiveUIDocument.Document   # type: Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc       = __revit__.ActiveUIDocument            # type: UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
active_view = doc.ActiveView                        # type: View

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


# my_filter = ISelectionFilter_Walls()
# selected_walls = selection.PickObjects(ObjectType.Element, my_filter,'Pick some walls')
# try:
#     selected_walls_refs = selection.PickObjects(ObjectType.Element, 'Pick some walls')
#     selected_walls = [doc.GetElement(ref) for ref in selected_walls_refs]
# except:
#     print ("pick something, man!")
#     import sys
#     sys.exit()


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


# all_walls_by_class = FilteredElementCollector(doc).OfClass(Wall).ToElements()
# all_walls_by_cat = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
# print ("found {} walls by class".format(len(all_walls_by_class)))
# print ("found {} walls by category".format(len(all_walls_by_cat)))
# walls_no_mip_by_class = [wall for wall in all_walls_by_class if not wall.Symbol.Family.IsInPlace]
# walls_no_mip_by_category = [wall for wall in all_walls_by_cat if not wall.Symbol.Family.IsInPlace]
# print ("[less mip] found {} walls by class".format(len(all_walls_by_class)))
# print ("[less mip] found {} walls by category".format(len(all_walls_by_cat)))

# all_walls_by_cat = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
# print ("found {} walls by category".format(len(all_walls_by_cat)))

# walls_no_mip_by_category = [wall for wall in all_walls_by_cat if not wall.Symbol.Family.IsInPlace]
# print ("[less mip] found {} walls by category".format(len(all_walls_by_cat)))

def jh_collect_category  (doc, the_category, the_active_view=doc.ActiveView.Id):
    '''
    My FilteredElementCollector, using OfCategory and returning a
    .NET list of elements, excluding the ElementType.
    '''

    return FilteredElementCollector(doc, the_active_view).OfCategory(the_category).WhereElementIsNotElementType().ToElements()

def jh_collect_class  (doc, the_class):
    '''
    My FilteredElementCollector, using OfClass and returning a
    .NET list of elements, excluding the ElementType.
    '''
    return FilteredElementCollector(doc).OfClass(the_class).ToElements()

# all_doors = jh_collect_category (doc, BuiltInCategory.OST_Doors) #FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
# print ("found {} doors by category".format(len(all_doors)))
# doors_no_mip =  [door for door in all_doors if not door.Symbol.Family.IsInPlace]
# print ("[less mip] found {} doors by category".format(len(doors_no_mip)))
# for door in all_doors:
#     print (door.Symbol)
# print ()
#
# all_walls = jh_collect_category (doc, BuiltInCategory.OST_Walls) #FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
# print ("found {} walls by category".format(len(all_walls)))





# selected_stuff = uidoc.Selection.GetElementIds()
#
# if selected_stuff:
#     el_collector = FilteredElementCollector (doc, selected_stuff).OfClass(Wall).WhereElementIsNotElementType().ToElements()
#     print ("There are {} Walls ".format(len(el_collector)))
#
#
# all_design_options = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DesignOptions).ToElements()
# print ("Found {} design options.".format(len(all_design_options)))
# print (all_design_options[0].Name)





# mats = jh_collect_category (doc, BuiltInCategory.OST_Materials)
# mats_ = jh_collect_class(doc, Material)
# print ("found {} materials by category".format(len(mats)))
# print ("found {} materials by class".format(len(mats_)))

# views = jh_collect_category (doc, BuiltInCategory.OST_Views, active_view.Id)
# views_ = jh_collect_class(doc, View)
#
#
# data = []
# for view in views_: #type:View
#     typ             = str(type(view)).replace("<type '", '').replace("'>", '')
#     view_type       = str(view.ViewType)
#     view_id         = str(view.Name)
#     category        = str(view.Category.BuiltInCategory) if view.Category else 'n/a'
#     data.append([typ, view_type, view_id, category])
#
# from pyrevit import script
# output_window = script.get_output()
# output_window.print_table(table_data=data,
#                           columns=["Type", "ViewType", "Name", "Category"],
#                           title="Example output table")

# views = jh_collect_category (doc, BuiltInCategory.OST_Views)
# views_3D = [view for view in jh_collect_class(doc, View) if type(view) == View3D]
# views_3D = [view for view in jh_collect_class(doc, View) if view.ViewType == ViewType.ThreeD]
# print (len(views_3D))

# def is_model_in_place_wall(wall):
#     # Check if the element is a FamilyInstance
#     wall_as_instance = wall if isinstance(wall, FamilyInstance) else None
#
#     if wall_as_instance is not None:
#         # Check if the FamilyInstance's Family is an in-place family
#         return wall_as_instance.Symbol.Family.IsInPlace
#
#     # If the element is not a FamilyInstance, it's not a model-in-place wall
#     return False
#
# sel_wall = selection.PickObject (ObjectType.Element, 'Pick one wall')
# if not sel_wall:
#     print ("please pick something!")
#     import sys
#     sys.exit()
# print (sel_wall)
# # print (is_model_in_place_wall(sel_wall))
# print ("isinstance(sel_wall, FamilyInstance) returns {}".format(isinstance(sel_wall, FamilyInstance)))




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



import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


# Start a transaction
t = Transaction(doc, "Create grids")
t.Start()

# Create vertical gridlines (A to E)
vertical_grids = []
for i, name in enumerate(['A', 'B', 'C', 'D', 'E']):
    line = Line.CreateBound(XYZ(i * 10, 0, 0), XYZ(i * 10, 50, 0))
    grid = Grid.Create(doc, line)
    grid.Name = name
    vertical_grids.append(grid)

# Create horizontal gridlines (1 to 5)
horizontal_grids = []
for i, name in enumerate(['1', '2', '3', '4', '5']):
    line = Line.CreateBound(XYZ(0, i * 10, 0), XYZ(50, i * 10, 0))
    grid = Grid.Create(doc, line)
    grid.Name = name
    horizontal_grids.append(grid)
t.Commit()

t = Transaction(doc, "Add structure")
t.Start()
# Load a structural column family and type
column_type = FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_StructuralColumns).FirstElement()

# Load a structural framing family and type
framing_type = FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(BuiltInCategory.OST_StructuralFraming).FirstElement()

# Create columns at grid intersections
column_height = 13 * 0.3048  # Convert feet to meters
columns = []
print ("num vert grids is {}".format(len(vertical_grids)))
print ("num hor grids is {}".format(len(horizontal_grids)))
for v_grid in vertical_grids:
    for h_grid in horizontal_grids:
        intersectionResults = IntersectionResultArray()
        # result = v_grid.Curve.Intersect(h_grid.Curve, intersectionResults)
        all_results = clr.Reference[IntersectionResultArray](IntersectionResultArray())
        result = v_grid.Curve.Intersect(h_grid.Curve, all_results)
        if result == SetComparisonResult.Overlap:
            for i in range(intersectionResults.Size):
                intersectionResult = intersectionResults.get_Item(i)
                point = intersectionResult.XYZPoint
                base_point = XYZ(point.X, point.Y, 0)
                top_point = XYZ(point.X, point.Y, column_height)
                column = doc.Create.NewFamilyInstance(base_point, column_type, Structure.StructuralType.Column)
                column.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM).Set(top_point)
                columns.append(column)

# Create framing members along the gridlines
for i in range(len(vertical_grids)):
    for j in range(len(horizontal_grids)):
        start_point = XYZ(i * 10, j * 10, column_height)
        if i < len(vertical_grids) - 1:
            # start_point = XYZ(i * 10, j * 10, column_height)
            end_point = XYZ((i + 1) * 10, j * 10, column_height)
            line = Line.CreateBound(start_point, end_point)
            fam_inst = doc.Create.NewFamilyInstance(start_point, framing_type, Structure.StructuralType.Beam)
            fam_inst.Location.Curve = line
        if j < len(horizontal_grids) - 1:
            # start_point = XYZ(i * 10, j * 10, column_height)
            end_point = XYZ(i * 10, (j + 1) * 10, column_height)
            line = Line.CreateBound(start_point, end_point)
            fam_inst = doc.Create.NewFamilyInstance(start_point, framing_type, Structure.StructuralType.Beam)
            fam_inst.Location.Curve = line
        '''
        NEXT:
            create columns at those locations
                create piers and footings under those locations (maybe)
            create a slab same size as grid + extension
                make ref planes for this first, then lock to these
        '''

# Commit the transaction
t.Commit()
