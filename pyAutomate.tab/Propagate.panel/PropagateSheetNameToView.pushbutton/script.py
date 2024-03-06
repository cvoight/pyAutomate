# -*- coding: utf-8 -*-

from Autodesk.Revit import DB
from pyrevit import revit, forms

from pyAutomate.helpers import *

views = [
    ViewPlanTitleItem(v)
    for v in
    # SortByName(ElementsOfClass(DB.ViewPlan))
    sorted(
        ElementsOfClass(DB.ViewPlan),
        key=lambda v: v.get_Parameter(
            DB.BuiltInParameter.VIEWPORT_SHEET_NUMBER
        ).AsString(),
    )
    if v.get_Parameter(DB.BuiltInParameter.VIEWPORT_SHEET_NUMBER).AsString()
    and v.get_Parameter(DB.BuiltInParameter.VIEW_DESCRIPTION).AsString() == ""
]

description = "Propagate Sheet Name"

try:
    with revit.Transaction(description):
        selected_views = forms.SelectFromList.show(
            views,
            title=description,
            button_name="Select Views",
            multiselect=True,
        )
        for view in selected_views:
            name = view.get_Parameter(
                DB.BuiltInParameter.VIEWPORT_SHEET_NAME
            ).AsString()
            view.get_Parameter(DB.BuiltInParameter.VIEW_DESCRIPTION).Set(name)

except Exception:
    pass

revit.uidoc.RefreshActiveView()
