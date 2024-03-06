# -*- coding: utf-8 -*-

from Autodesk.Revit import DB
from pyrevit import revit, forms

from pyAutomate.helpers import *

views = SortByName(ElementsOfClass(DB.ViewPlan))
description = "Propagate Crop Region"

try:
    with revit.Transaction(description):
        template_view = forms.SelectFromList.show(
            views,
            title=description,
            button_name="Select Template View",
            name_attr="Name",
        )
        selected_views = forms.SelectFromList.show(
            views,
            title=description,
            button_name="Select Views",
            name_attr="Name",
            multiselect=True,
        )
        [crop_shape] = template_view.GetCropRegionShapeManager().GetCropShape()
        for view in selected_views:
            view.CropBoxActive = True
            view.CropBoxVisible = True
            view.GetCropRegionShapeManager().SetCropShape(crop_shape)
except Exception:
    pass

revit.uidoc.RefreshActiveView()
