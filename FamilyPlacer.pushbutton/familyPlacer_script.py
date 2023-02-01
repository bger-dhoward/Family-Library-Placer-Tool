__title__ = "Place\nFamilies"
__doc__ = "Autoplace all non-hosted families of X type"
__author__ = "D. Howard, Ballinger"

from Autodesk.Revit.DB import *
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

doc = __revit__.ActiveUIDocument.Document
nonStruct = DB.Structure.StructuralType.NonStructural

family_types = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_SpecialityEquipment).WhereElementIsElementType()

family_names = {}

for fam in family_types:
    if fam.FamilyName in family_names:
        family_names[fam.FamilyName].append(fam)
    else:
        family_names[fam.FamilyName] = [fam]
        

x_start = 0
y_start = 0
x_current = 0
y_current = 0
z = 0

x_offset = 10
y_offset = 20

t = Transaction(doc, "Array all families of X type")
t.Start()

acceptable_placements = [
    FamilyPlacementType.OneLevelBased,
    ]
    
hosted_fams = []

for name, fams in sorted(family_names.items()):
    for fam in fams:
        if fam.Family.FamilyPlacementType in acceptable_placements:
            fam.Activate()
            pt = XYZ(x_current, y_current, z)
            inst = doc.Create.NewFamilyInstance(pt, fam, nonStruct)
            x_current += x_offset
        else:
            hosted_fams.append(name)
            break
    
    x_current = x_start
    y_current -= y_offset

t.Commit()

unplaced_number = len(hosted_fams)
placed_number = len(family_names) - unplaced_number

note = "{placed_number} non-hosted families placed.\n{unplaced_number} familes are hosted and were not automatically placed.\nUnplaced familes:\n---".format(placed_number=placed_number, unplaced_number=unplaced_number)
unplaced_str = "\n--- ".join(hosted_fams)

forms.alert("Specialty Equipment Placed",
    sub_msg = note + unplaced_str,
    title="Familes Placed",
    )

# print("The following families are hosted and cannot be placed automatically with the script:     Sorry :-(")
# for name in hosted_fams:
    # print(name)