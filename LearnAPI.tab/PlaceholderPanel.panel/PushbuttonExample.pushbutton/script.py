# -*- coding: utf-8 -*-
__title__ = "Rename views"
__doc__ = """Version = 1.0
Date    = 15.07.2024
_________________________________________________________________
Description:
Rename views using Find/Replace logic
_________________________________________________________________
How-to:
-> Click on the button
-> Select Views
-> Define the renaming rules
-> Rename the views
_________________________________________________________________
Last update: 2024-12-12

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

# SELECT VIEWS
sel_el_ids = uidoc.Selection.GetElementIds ()
sel_elem = [doc.GetElement(elemID) for elemID in sel_el_ids] # note the List comprehension there....
sel_views = [elem for elem in sel_elem if issubclass(type(elem), View)] # if the element's TYPE is a SUBCLASS of VIEW
# I'd normally think of it like: if elem.type == 'View' .... or maybe   t = getType (elem); if t == subclass('View')
# so instead of thinking   if Object.Property == ParticularType ... think of it like   if issubclass (type(Object), ParticularType)

# IF NO VIEWS SELECTED, PROMPT THE USER TO SELECT SOME
if not sel_views:
    sel_views = forms.select_views()

if not sel_views: # if STILL no selected views, even after presenting the form above!
    forms.alert("No views selected! Please try again.", exitscript=True)


# DEFINE RENAMING
#2️⃣🅰
# prefix = 'jhef-'
# find = 'EXTERIOR WALLS'
# replace = 'PARAPARAPARAPETS'
# suffix = '-test'
#2️⃣🅱
from rpw.ui.forms import (FlexForm, Label, TextBox, Separator, Button)
components = [Label('Prefix?:'), TextBox('prefix'),
              Label('Find?:'), TextBox ('find'),
              Label ('Replace?'), TextBox ('replace'),
              Label ('Suffix?'), TextBox ('suffix'),
              Separator(),
              Button('RENAME SELECTED VIEWS')]
form = FlexForm('Rename selected views', components)
form.show()

user_inputs = form.values # this is a dictionary
prefix = user_inputs['prefix']
find = user_inputs['find']
replace = user_inputs['replace']
suffix = user_inputs['suffix']



#🔒 start transaction
t = Transaction (doc,'jh-Rename Views')
t.Start() #🔓
for view in sel_views:
    #3️⃣ create the view name
    old_name = view.Name
    # print ("old_name is " + old_name)
    new_name = prefix + old_name.replace(find, replace) + suffix
    #4️⃣ rename views, ensuring a unique view name
    for i in range(20): # note this is a safer way to avoid infinite loops!
        try:
            view.Name = new_name
            # print ('{} renamed to {}'.format(old_name, new_name))
            break # only need this break because we're using the for loop to escape infinite loops!
        except:
            # this could probably be a forms.alert() to say that view name already exists,
            # but instead we'll just add a dummy character to the end
            # print ("The view named " + new_name + " already exists! Please start again.")
            new_name += '*'
t.Commit() #🔒