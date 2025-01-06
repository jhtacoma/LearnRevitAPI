# imports
#==================================================
from Autodesk.Revit.DB import *

#variables
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document



# Reusable Snippets

def get_selected_elements (target_types=None):
    """
    Get selected elements from the Revit API.
    Can optionally supply a list of element types to filter just those.

    EXAMPLE:
        sel_walls = get_selected_elements ([Wall, Floor])
    OR
        sel_walls = get_selected_elements ()
    """
    selection = uidoc.Selection
    selected_element_ids = selection.GetElementIds()
    selected_elements = [doc.GetElement(e_id) for e_id in selected_element_ids]

    if target_types:
        # Filter Selection (Optional)
        filtered_elements = [el for el in selected_elements if type(el) in target_types]
        return filtered_elements
    else:
        return selected_elements