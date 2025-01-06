# -*- coding: utf-8 -*-
__title__   = "Code reuse template"
__doc__     = """Version = 1.0
Date    = 15.06.2024
________________________________________________________________
Description:

________________________________________________________________
Instructions:

________________________________________________________________
Author: Jamie Hutchings"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================
# from Snippets._selection import get_selected_elements
#
# sel_el = get_selected_elements ()
# sel_walls = get_selected_elements ([Wall, Floor])
#
# print (sel_el)
# print (sel_walls)
#
#



from Snippets._trace import trace


a = 5
b = "Johnny"
trace ([a, b], 'bunch of stuff')
trace (a, 'a')
trace ()
trace (b, 'b')
