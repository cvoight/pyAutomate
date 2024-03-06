# -*- coding: utf-8 -*-

from pyrevit import DB, revit, forms

description = "Set Text Width"

try:
    with revit.Transaction(description):
        selection = (
            revit.get_selection()
            if not revit.get_selection().is_empty
            else revit.pick_elements()
        )
        width = forms.ask_for_number_slider(
            default=6, min=1, title="Choose Text Width (in)"
        )
        for element in selection:
            if isinstance(element, DB.TextNote):
                element.Width = width / 12
except Exception:
    pass

revit.uidoc.RefreshActiveView()
