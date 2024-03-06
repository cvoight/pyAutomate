# -*- coding: utf-8 -*-

from Autodesk.Revit import DB
from pyrevit import revit, forms

from pyAutomate.helpers import *

sheets = [
    SheetItem(s)
    for s in sorted(ElementsOfClass(DB.ViewSheet), key=lambda s: s.SheetNumber)
]

description = "Propagate View Location"

try:
    with revit.Transaction(description):
        template_sheet = forms.SelectFromList.show(
            sheets,
            title=description,
            button_name="Select Template Sheet",
        )
        selected_sheets = forms.SelectFromList.show(
            sheets,
            title=description,
            button_name="Select Target Views",
            multiselect=True,
        )
        viewports = template_sheet.GetAllViewports()
        viewport = revit.doc.GetElement(viewports[0])
        center = viewport.GetBoxCenter()
        outline = viewport.GetBoxOutline()
        typeId = viewport.GetTypeId()
        for sheet in selected_sheets:
            vps = sheet.GetAllViewports()
            vp = revit.doc.GetElement(vps[0])
            vp.SetBoxCenter(center)
            vp.ChangeTypeId(typeId)

except Exception:
    pass

revit.uidoc.RefreshActiveView()
