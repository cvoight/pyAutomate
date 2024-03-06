# -*- coding: utf-8 -*-

from Autodesk.Revit import DB
from pyrevit import revit, forms
from pyrevit.coreutils import increment_str

from pyAutomate.helpers import *

view_family_types = [
    t
    for t in DB.FilteredElementCollector(doc).OfClass(DB.ViewFamilyType).ToElements()
    if t.ViewFamily
    in {
        DB.ViewFamily.CeilingPlan,
        DB.ViewFamily.FloorPlan,
        DB.ViewFamily.AreaPlan,
        DB.ViewFamily.StructuralPlan,
    }
]

description = "Batch Create Views"

try:
    with revit.Transaction(description):
        selected_view_family = forms.SelectFromList.show(
            view_family_types,
            title=description,
            name_attr="FamilyName",
            button_name="Select Plan Type",
        )
        selected_view_templates = forms.select_viewtemplates(title=description)
        selected_levels = forms.select_levels(title=description)
        for view_template in selected_view_templates:
            for level in selected_levels:
                created_view = DB.ViewPlan.Create(
                    revit.doc, selected_view_family.Id, level.Id
                )
                name = "{}_{}".format(level.Name, view_template.Name)
                names = {v.Name for v in ElementsOfClass(DB.View)}
                created_view.Name = safe_name(name, names)
                created_view.ViewTemplateId = view_template.Id
except Exception:
    pass

revit.uidoc.RefreshActiveView()
