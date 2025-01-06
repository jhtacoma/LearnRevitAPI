# -*- coding: utf-8 -*-
__title__   = "Button 1"
__doc__     = """Version = 1.0

By Jamie Hutchings, building on templates by Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *

#.NET Imports
import clr

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


def get_id_for_filter_from_name (filter_name):
    # all_available_vfs_in_project = FilteredElementCollector(doc).OfClass(ParameterFilterElement).ToElements()
    for vf in all_available_vfs_in_project:
        # print ("vf.Name is " + vf.Name + ", comparing to " + filter_name)
        if vf.Name == filter_name:
            return vf.Id

solid_fpattern_reference = find_solid_fillpat()


JH_vf_specs_DICT = [
                        { "name" : "JH Ceilings",
                           "ost category" : BuiltInCategory.OST_Ceilings,
                           "transparency" : 80
                           },
                        { "name" : "JH Doors",
                           "ost category" : BuiltInCategory.OST_Doors,
                           "transparency" : 50
                           },
                        { "name" : "JH Floors",
                           "ost category" : BuiltInCategory.OST_Floors,
                           "transparency" : 80
                           },
                        { "name" : "JH Roofs",
                           "ost category" : BuiltInCategory.OST_Roofs,
                           "transparency" : 80
                           },
                        { "name" : "JH Structural Columns",
                           "ost category" : BuiltInCategory.OST_StructuralColumns,
                           "colour" : Color (0,213,213),
                           "transparency" : 0 # remember, 0 transparency means it's 100% visible!
                           },
                        { "name" : "JH Structural Foundations",
                           "ost category" : BuiltInCategory.OST_StructuralFoundation,
                           "colour" : Color (225,73,0),
                           "transparency" : 0 # remember, 0 transparency means it's 100% visible!
                           },
                        { "name" : "JH Structural Framing",
                           "ost category" : BuiltInCategory.OST_StructuralFraming,
                           "colour" : Color (202,004,251),
                           "transparency" : 0 # remember, 0 transparency means it's 100% visible!
                           },
                        {"name" : "JH Walls",
                           "ost category" : BuiltInCategory.OST_Walls,
                           "transparency" : 60
                           },
                        {"name" : "JH Windows",
                           "ost category" : BuiltInCategory.OST_Windows,
                           "transparency" : 80
                           },
                         ]

# print (JH_vf_specs_DICT [1] ["name"])

#🤖 Automate Your Boring Work Here
with Transaction (doc, 'Create ViewFilter') as t:
    active_view = doc.ActiveView
    turn_filters_on = False # start by assuming we're turning off the filters (if they exist)

    for currentFilter in JH_vf_specs_DICT:
        t.Start()

        # First: assume a blank slate, i.e. that none of the JH filters have ever been created in this project
        try:
            # I will only use a single category at a time -- that is, I don't want to apply a particular filter to both walls and floors, for example;
            # so this is a little ungainly, but necessary apparently!
            categories = List [ElementId]()
            currentCategory = currentFilter ['ost category'] # i.e. BuiltInCategory.OST_Walls
            categories.Add(ElementId(currentCategory))

            # print ("about to CREATE filter " + currentFilter['name'])
            # Create the filter (so it becomes available to all views potentially)
            view_filter = ParameterFilterElement.Create(doc, currentFilter['name'], categories)

            # Since if the above code ran successfully, it means that at least one of the JH filters
            # had NOT previously been applied to this view, which implies that we're turning ON
            # all these filters, we'll set that toggle now:
            turn_filters_on = True

        except:
            # print ("XX except: looks like " + currentFilter['name'] + " already existed in project")
            pass

        # Note that this list of filters (and its names and ids) is *NOT* what you see when you click
        # the Filters tab of View Graphics; it's what you see if, on that tab, you click Add or Edit/New!
        # In other words, these are all the filters that EXIST in the entire project; whether or not they
        # have been APPLIED to the current view, *or* even if applied, whether or not they are
        # actually ENABLED is another matter!
        all_available_vfs_in_project = FilteredElementCollector(doc).OfClass(ParameterFilterElement).ToElements()


        # Next, maybe the filter exists in the project, but hasn't been added to this view
        try:
            # view_filter = ParameterFilterElement.Create(doc, currentFilter['name'], categories)
            for i in all_available_vfs_in_project:
                if i.Name == currentFilter['name']:
                    # print ("--about to ADD " + currentFilter['name'] + " to the current view")
                    active_view.AddFilter(i.Id)

            # As in the previous 'try' code block, f the above code ran successfully, it means that at least one of the JH filters
            # had NOT previously been applied to this view, which implies that we're turning ON
            # all these filters. Therefore we'll set that toggle now:
            turn_filters_on = True

        except:
            # print ("--XX except: looks like " + currentFilter['name'] + " had already been attached to this view")
            pass

        try:
            override_settings = OverrideGraphicSettings ()
            try:
                currentColour = currentFilter ['colour']
                override_settings.SetSurfaceForegroundPatternId(solid_fpattern_reference.Id)
                override_settings.SetSurfaceForegroundPatternColor(currentColour)
                override_settings.SetCutLineColor(currentColour)
            except:
                pass
            try:
                currentTransparency = currentFilter ['transparency']
                override_settings.SetSurfaceTransparency(currentTransparency)
            except:
                pass

            # print ("----about to ENABLE the filter " + currentFilter ['name'])
            target_id = get_id_for_filter_from_name (currentFilter['name'])         # WHY IS IT FAILING HERE???? THIS TRIGGERS THE 'except' :(
            active_view.SetFilterOverrides(target_id, override_settings)

        except:
            # print ("----XX except: looks like filter " + currentFilter ['name'] + " already enabled")
            pass

        t.Commit()


    # By this point, all the filters have been created and applied to the current view (or they already
    # existed and we just made sure they were applied) -- but we still need to figure out if we're turning them
    # on or off; our logic is that if we find even one filter is currently off, we'll turn
    # all of them back on again; otherwise (i.e. all of them are on) we'll turn them off.
    if turn_filters_on == False:
        for currentFilter in JH_vf_specs_DICT:
            for i in all_available_vfs_in_project:
                if i.Name == currentFilter['name']:
                    if active_view.GetIsFilterEnabled(i.Id) == False:
                        turn_filters_on = True
                        break

    # Now all that's left is to toggle their visibility accordingly:
    t.Start()
    for currentFilter in JH_vf_specs_DICT:
        for i in all_available_vfs_in_project:
            # print ("here, i.Name is " + i.Name)
            if i.Name == currentFilter['name']:
                # print ("about to turn " + currentFilter ['name'] + " to " + str(turn_filters_on))
                active_view.SetIsFilterEnabled(i.Id, turn_filters_on)
    t.Commit ()


# THESE RULES, AND THE USE OF ElementParameterFilter, ARE NOT NECESSARY IF WE'RE APPLYING A FILTER TO
# AN ENTIRE CLASS OF ELEMENTS, SUCH AS ALL COLUMNS, ALL WALLS, ETC.
# If we only want it to apply to all walls, or all columns, etc., then we don't need any ElementParameterFilter, and
# when we call ParameterFilterElement() we only need to pass the first 3 parameters, since the 4th won't apply