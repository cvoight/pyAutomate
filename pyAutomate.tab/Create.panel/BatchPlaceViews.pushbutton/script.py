# -*- coding: utf-8 -*-

from Autodesk.Revit import DB
from pyrevit import revit, forms
from pyrevit import script

from pyAutomate.helpers import *

logger = script.get_logger()


class BatchPlaceViewsWindow(forms.WPFWindow):
    def __init__(self, xaml_source):
        self._sheets = ElementsOfClass(DB.ViewSheet)
        sheets = [
            SheetItem(s) for s in sorted(self._sheets, key=lambda s: s.SheetNumber)
        ]
        self._template_sheet = forms.SelectFromList.show(
            sheets,
            title="Batch Place Views",
            button_name="Select Template Sheet",
        )
        forms.WPFWindow.__init__(self, xaml_source)
        self.sheet_view_pairs.Focus()

    def _process_textbox(self):
        try:
            return {
                k: v
                for k, v in [
                    s.split(None, 1)
                    for s in filter(
                        None,
                        map(str.strip, str(self.sheet_view_pairs.Text).splitlines()),
                    )
                ]
            }
        except Exception as range_err:
            logger.error(range_err)
            return False

    def place_views_on_sheets(self, sender, args):
        self.Close()

        views = ElementsOfClass(DB.ViewPlan)
        if self._template_sheet:
            viewports = self._template_sheet.GetAllViewports()
            viewport = revit.doc.GetElement(viewports[0])
            outline = viewport.GetBoxOutline()
            typeId = viewport.GetTypeId()
        else:
            outline = None

        try:
            with revit.Transaction("Place Views on Sheets"):
                for key, value in self._process_textbox().items():
                    [sheet] = [s for s in self._sheets if s.SheetNumber == key]
                    [view] = [v for v in views if v.Name == value]
                    if DB.Viewport.CanAddViewToSheet(revit.doc, sheet.Id, view.Id):
                        titleblock = (
                            DB.FilteredElementCollector(revit.doc, sheet.Id)
                            .OfCategory(DB.BuiltInCategory.OST_TitleBlocks)
                            .FirstElement()
                        )
                        maximum = titleblock.BoundingBox[sheet].Max
                        minimum = titleblock.BoundingBox[sheet].Min
                        center = maximum.Subtract(minimum).Divide(2)
                        vp = DB.Viewport.Create(revit.doc, sheet.Id, view.Id, center)
                        if outline:
                            o = vp.GetBoxOutline()
                            vp.SetBoxCenter(
                                DB.XYZ(
                                    center.X
                                    + (outline.MaximumPoint.X - o.MaximumPoint.X),
                                    center.Y
                                    + (outline.MinimumPoint.Y - o.MinimumPoint.Y),
                                    0,
                                )
                            )
                            vp.ChangeTypeId(typeId)
        except Exception:
            pass


BatchPlaceViewsWindow("BatchPlaceViewsWindow.xaml").show(modal=True)
