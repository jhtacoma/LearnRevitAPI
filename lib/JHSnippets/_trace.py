# -*- coding: utf-8 -*-

# imports
#==================================================
from Autodesk.Revit.DB import *

#variables
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document



# Reusable Snippets
def get_var_name(var):
    for name, value in globals().items():
        if value is var:
            return name
    return "[no name]"

def trace (the_var=None, the_var_name=''):
    """
    trace(the_var, the_var_name) is used to output basic variables to the screen for debugging.
    ARGUMENTS:
        the_var         the variable (i.e. a string, an integer, a list) whose value(s) you want to trace
        the_var_name    name of the variable for display purposes [optional]
    NOTE:
        if trace() is called with no arguments, a separator line will be added to the output window, like this:
        ==============================================
    """
    
    if the_var:
        which_type = str(type (the_var))
        # print ("• " + get_var_name(the_var) + " = " + str(the_var))
        if which_type == "<type 'list'>":
            print ("• [LIST] " + the_var_name + ":")
            for each_item_in_list in the_var:
                which_type = str(type(each_item_in_list))
                if which_type == "<type 'list'>":
                    print ("nested list! not going to parse!")
                elif which_type == "<type 'int'>":
                    print ("•• [INT] " + str(each_item_in_list))
                elif which_type == "<type 'str'>":
                    print ("•• [STR] " + str(each_item_in_list))
                elif which_type == "<type 'dict'>":
                    print ("nested dict! not going to parse")
                else:
                    print ("something else that's nested ... don't know and don't care!")
        elif which_type == "<type 'dict'>":
            print ("is dict")
        else:
            if len(the_var_name):
                the_var_name = the_var_name + ' = '
            if which_type == "<type 'int'>":
                print ("• [INT] " + the_var_name+ str(the_var))
            elif which_type == "<type 'str'>":
                print ("• [STR] " + the_var_name + str(the_var))
            else:
                print ("dunno")
    else: print ("==============================")