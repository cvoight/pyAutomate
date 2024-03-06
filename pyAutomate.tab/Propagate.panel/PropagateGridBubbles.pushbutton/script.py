# -*- coding: utf-8 -*-

from Autodesk.Revit import DB
from pyrevit import revit, forms

from pyAutomate.helpers import *

grids = SortByName(ElementsOfClass(DB.Grid))
views = SortByName(ElementsOfClass(DB.ViewPlan))
description = "Propagate Grid Bubbles"

try:
    with revit.Transaction(description):
        selected_views = forms.SelectFromList.show(
            views,
            title=description,
            button_name="Select Views",
            name_attr="Name",
            multiselect=True,
        )
        end_zero_grids = forms.SelectFromList.show(
            grids,
            title=description,
            button_name="Select Grids to Show End Zero",
            name_attr="Name",
            multiselect=True,
        )
        end_one_grids = forms.SelectFromList.show(
            grids,
            title=description,
            button_name="Select Grids to Show End One",
            name_attr="Name",
            multiselect=True,
        )
        for view in selected_views:
            for grid in grids:
                grid.HideBubbleInView(DB.DatumEnds.End0, view)
                grid.HideBubbleInView(DB.DatumEnds.End1, view)
                if grid in end_zero_grids:
                    grid.ShowBubbleInView(DB.DatumEnds.End0, view)
                if grid in end_one_grids:
                    grid.ShowBubbleInView(DB.DatumEnds.End1, view)
except Exception:
    pass

revit.uidoc.RefreshActiveView()
