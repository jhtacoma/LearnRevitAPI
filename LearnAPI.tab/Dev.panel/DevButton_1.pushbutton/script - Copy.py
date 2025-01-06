# -*- coding: utf-8 -*-
__title__   = "Button 1"
__doc__     = """Version = 1.0
Date    = 15.06.2024
________________________________________________________________
Description:

This is the placeholder for a .pushbutton
You can use it to start your pyRevit Add-In

________________________________________________________________
How-To:

1. [Hold ALT + CLICK] on the button to open its source folder.
You will be able to override this placeholder.

2. Automate Your Boring Work ;)

________________________________________________________________
TODO:
[FEATURE] - Describe Your ToDo Tasks Here
________________________________________________________________
Last Updates:
- [15.06.2024] v1.0 Change Description
- [10.06.2024] v0.5 Change Description
- [05.06.2024] v0.1 Change Description 
________________________________________________________________
Author: Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *

#.NET Imports
import clr

# from lib.Samples.CreateElements import active_view

# from lib.Samples.ViewsSheets import all_available_vfs_in_project, all_available_vf_names, rule_1, view_filter, override_settings, \
#     active_view

clr.AddReference('System')
from System.Collections.Generic import List
from pyrevit import revit, DB



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


def find_solid_fillpat():
    '''
    We need to locate which of the many fill patterns defined in the project represents the 'Solid' drafting fill pattern,
    so that we can reference it and set various overrides to that particular pattern.

    In theory, a project might not have such a pattern defined, and so code below could break when trying to set an element's
    fill pattern id to it -- but that's bound to be quite rare, and it clutters and confuses the code to constantly test
    for the fill pattern id's existence (in my opinion!).
    '''
    existing_pats = DB.FilteredElementCollector(revit.doc)\
                      .OfClass(DB.FillPatternElement)\
                      .ToElements()
    for pat in existing_pats:
        fpat = pat.GetFillPattern()
        if fpat.IsSolidFill and fpat.Target == DB.FillPatternTarget.Drafting:
            return pat


def get_id_from_name (elementsToSearch, targetName = ''):
    for i in elementsToSearch:
        if i.Name == targetName:
            return i.Id
    return False



solid_fpattern_reference = find_solid_fillpat()

# Note that this list of filters (and its names and ids) is *NOT* what you see when you click
# the Filters tab of View Graphics; it's what you see if, on that tab, you click Add or Edit/New!
# In other words, these are all the filters that EXIST in the entire project; whether or not they
# have been APPLIED to the current view, *or* even if applied, whether or not they are
# actually ENABLED is another matter!
all_available_vfs_in_project = FilteredElementCollector(doc).OfClass(ParameterFilterElement).ToElements()
all_available_vf_names = [f.Name for f in all_available_vfs_in_project]
all_available_vf_ids = [f.Id for f in all_available_vfs_in_project]



JH_vf_specs_DICT = [{ "name" : "JH Walls",
                           "ost category" : BuiltInCategory.OST_Walls,
                           "colour" : Color (255,0,0),
                           "transparency" : 50
                           },
                        { "name" : "JH Columns",
                           "ost category" : BuiltInCategory.OST_StructuralColumns,
                           "colour" : Color (0,213,213),
                           "transparency" : 0 # remember, 0 transparency means it's 100% visible!
                           },
                         ]

# print (JH_vf_specs_DICT [1] ["name"])

#🤖 Automate Your Boring Work Here
with Transaction (doc, 'Create ViewFilter') as t:
    active_view = doc.ActiveView
    turn_filters_on = False # start by assuming we're turning off the filters (if they exist)
    for currentFilter in JH_vf_specs_DICT:
        f_name = currentFilter ['name']
        print ("checking f_name " + f_name)
        # print (all_available_vf_names)
        if f_name not in all_available_vf_names: # if we haven't created this filter yet
            print ("filter " + f_name + " not found, so must create")
            turn_filters_on = True # we'll turn on all filters if even one single filter doesn't exist
            new_filter_name = currentFilter['name']

            t.Start()

            currentColour = currentFilter ['colour']
            currentTransparency = currentFilter ['transparency']
            override_settings = OverrideGraphicSettings ()
            override_settings.SetSurfaceForegroundPatternId(solid_fpattern_reference.Id)
            override_settings.SetSurfaceForegroundPatternColor(currentColour)
            override_settings.SetCutLineColor(currentColour)
            override_settings.SetSurfaceTransparency(currentTransparency)

            # # apply the override to an active view
            # print ("adding filter " + view_filter.Id + " now")
            # active_view.AddFilter(view_filter.Id)
            # active_view.SetFilterOverrides(view_filter.Id, override_settings)

            t.Commit ()


    # Now we'll make sure all the JH filters are APPLIED to the current view, just in case one or more
    # might have been removed by the user

    for currentFilter in JH_vf_specs_DICT:
        try:
            t.Start()
            # I will only use a single category at a time -- that is, I don't want to apply a particular filter to both walls and floors, for example;
            # so this is a little ungainly, but necessary apparently!
            categories = List [ElementId]()
            currentCategory = currentFilter ['ost category'] # i.e. BuiltInCategory.OST_Walls
            categories.Add(ElementId(currentCategory))

            view_filter = ParameterFilterElement.Create(doc, currentFilter['name'], categories)
            active_view.AddFilter(view_filter.Id)
            active_view.SetFilterOverrides(view_filter.Id, override_settings)

            # If the above code ran successfully, it means that at least one of the JH filters
            # had NOT previously been applied to this view, which implies that we're turning ON
            # all these filters. Therefore we'll set that toggle now:
            turn_filters_on = True
            t.Commit()

        except:
            print ("filter " + currentFilter ['name'] + " already applied")

    # By this point, all the filters have been created and applied to the current view (or they already
    # existed and we just made sure they were applied). All that's left is to toggle their visibility
    # accordingly:
    t.Start()
    for i in all_available_vfs_in_project:
        if i.Name == f_name:
            active_view.SetIsFilterEnabled(i.Id, turn_filters_on)
    t.Commit ()

    t.Start()
    for i in all_available_vfs_in_project:
        if i.Name == f_name:
            active_view.SetIsFilterEnabled(i.Id, turn_filters_on)
    # # apply the override to an active view
    # print ("adding filter " + view_filter.Id + " now")
    # active_view.AddFilter(view_filter.Id)
    # active_view.SetFilterOverrides(view_filter.Id, override_settings)
    t.Commit()
    # t.Start()
    #
    # active_view.SetIsFilterEnabled(get_id_from_name(all_available_vfs_in_project, currentFilter ['name']), turn_filters_on)
    # # for i in all_available_vfs_in_project:
    # #     if i.Name == f_name:
    # #         active_view.SetIsFilterEnabled(i.Id, turn_filters_on)
    # t.Commit()
    '''
    Next is to determine the code to have this actually colourize the things I want to -- columns, framing, etc, floors & walls;
    First, for view-graphics:
        Ceilings:
            surface
                80% transparency
        Doors:
            surface
                50% transparency
        Floors:
            surface
                80% transparency
        Roofs:
            surface
                80% transparency
        Walls:
            surface:
                60% transparency
    Then, for filters:
        Structural columns:
            surface
                patterntype solid fill
                color blue
            cut
                patterntype solid fill
                color blue
        Structural foundations:
            surface
                patterntype solid fill
                color orange (225-73-00)
            cut
                patterntype solid fill
                color orange (225-73-00)
        Structural framing:
            surface
                patterntype solid fill
                color fucsia (202-004-00)
            cut
                patterntype solid fill
                color fucsia (202-004-00)          
    
        
    then refactor to condense...
    '''


categories = List [ElementId]()
categories.Add(ElementId(BuiltInCategory.OST_Walls))

# # check function of wall, ie exterior, soffit
# pvp = ParameterValueProvider (ElementId(BuiltInParameter.FUNCTION_PARAM)) # like saying ParameterValueProvider (theObject.howDoesObjectFunction)
# rule_1 = FilterIntegerRule (pvp, FilterNumericEquals(), int(WallFunction.Exterior))
#
# #rule_1 = ParameterFilterRuleFactory.CreateEqualsRule(ElementId(BuiltInParameter.FUNCTION_PARAM), int(WallFunction.Exterior))
#
#
# pvp = ParameterValueProvider (ElementId(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)) # like saying ParameterValueProvider (theObject.howDoesObjectFunction)
# print ("pvp is " + str(pvp.Get


# THESE RULES, AND THE USE OF ElementParameterFilter, ARE NOT NECESSARY IF WE'RE APPLYING A FILTER TO
# AN ENTIRE CLASS OF ELEMENTS, SUCH AS ALL COLUMNS, ALL WALLS, ETC.
# If we only want it to apply to all walls, or all columns, etc., then we don't need any ElementParameterFilter, and
# when we call ParameterFilterElement() we only need to pass the first 3 parameters, since the 4th won't apply

# check function of wall, ie exterior, soffit
# pvp = ParameterValueProvider (ElementId(BuiltInParameter.FUNCTION_PARAM)) # like saying ParameterValueProvider (theObject.howDoesObjectFunction)
# rule_1 = FilterIntegerRule (pvp, FilterNumericEquals(), int(WallFunction.Exterior))

# remember, some of the next line could be thought of as CreateEqualsRule (FUNCTION_PARAM, "exterior")
# rule_1 = ParameterFilterRuleFactory.CreateEqualsRule(ElementId(BuiltInParameter.FUNCTION_PARAM), int(WallFunction.Exterior))

# some of the next line could be thought of as CreateEqualsRule (INSTANCE_COMMENTS, "xxx")
# note also that 'ALL_MODEL_INSTANCE_COMMENTS' is a stupid name! Best to ignore the 'ALL_MODEL' prefix :o
# rule_2 = ParameterFilterRuleFactory.CreateEqualsRule(ElementId(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS),'xxx')

# rules = List [FilterRule] ([rule_1, rule_2])

# filter out the subset of walls we're interested in -- the Exterior ones commented 'xxx';
# wall_filter = ElementParameterFilter (rules)


# create a View Filter that will be 'run' an all our 'categories', and which will only match according to the wall_filter;
# it's like we run it through two filters; first through 'categories', so it only applies to walls in general (in this case)
# next, through 'wall_filter' which says "for everything in categories, only look at whatever meets our wall_filter rules";
# ParameterFilterElement is essentially the coded equivalent of an actual View Filter
# view_filter = ParameterFilterElement.Create(doc, new_filter_name, categories, wall_filter)
# view_filter = ParameterFilterElement.Create(doc, new_filter_name, categories)

#==================================================
#🚫 DELETE BELOW
# from Snippets._customprint import kit_button_clicked    # Import Reusable Function from 'lib/Snippets/_customprint.py'
# kit_button_clicked(btn_name=__title__)                  # Display Default Print Message
