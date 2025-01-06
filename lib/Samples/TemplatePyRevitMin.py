# -*- coding: utf-8 -*-
__title__ = "EF Template.min"
__doc__ = """Version = 1.0
Date    = 15.07.2024
_________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_________________________________________________________________
How-to:
-> Click on the button
-> ...
_________________________________________________________________
Last update: 2024-12-12
_________________________________________________________________
To-Do:
- Describe Next Features
_________________________________________________________________
Author: Jamie Hutchings, building on templates from Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *


# pyRevit
from pyrevit import revit, forms

# .NET Imports (You often need List import)
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
doc   = __revit__.ActiveUIDocument.Document #type: Document
uidoc = __revit__.ActiveUIDocument          #typ: UIDocument
app   = __revit__.Application


# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝
#==================================================

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================
# START CODE HERE
print('Template has been developed by Erik Frits.')