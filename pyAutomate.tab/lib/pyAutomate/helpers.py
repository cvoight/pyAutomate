from Autodesk.Revit import DB
from pyrevit.revit import doc
from pyrevit import forms
from re import split


class SheetItem(forms.TemplateListItem):
    @property
    def name(self):
        return "{} - {}".format(self.item.SheetNumber, self.item.Name)


class ViewPlanTitleItem(forms.TemplateListItem):
    @property
    def name(self):
        return "{} - {} ({})".format(
            self.item.get_Parameter(
                DB.BuiltInParameter.VIEWPORT_SHEET_NUMBER
            ).AsString(),
            self.item.Name,
            self.item.get_Parameter(DB.BuiltInParameter.VIEW_DESCRIPTION).AsString(),
        )


def ElementsOfCategory(c):
    return (
        DB.FilteredElementCollector(doc)
        .OfCategory(c)
        .WhereElementIsNotElementType()
        .ToElements()
    )


def ElementsOfClass(c):
    return (
        DB.FilteredElementCollector(doc)
        .OfClass(c)
        .WhereElementIsNotElementType()
        .ToElements()
    )


def ElementTypesOfClass(c):
    return (
        DB.FilteredElementCollector(doc)
        .OfClass(c)
        .WhereElementIsElementType()
        .ToElements()
    )


def SortByName(xs):
    # https://nedbatchelder.com/blog/200712/human_sorting.html#comment_7499
    cast = lambda s: int(s) if s.isdigit() else s
    return sorted(xs, key=lambda x: [cast(n) for n in split("([0-9]+)", x.Name)])


def safe_name(name, names):
    if name in names:
        return safe_name(increment_str(name), names)
    else:
        return name
