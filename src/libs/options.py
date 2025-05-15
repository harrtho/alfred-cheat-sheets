#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from workflow.workflow import ICON_HELP as WARNINGICON
from workflow.workflow import ICON_NOTE as HINT


# Switches that autually controls the workflow behavior
class Options:

    LARGETEXTPATTERN = "{}\n\n{}"

    def __init__(self, parser, wf):
        self._parser = parser
        self._wf = wf
        return None

    def searchInSheetByKeyword(self, sheetName, keyword):
        if sheetName is None:
            ret = self._parser.searchAcrossAll(keyword, self._wf)
        else:
            if sheetName not in self._parser.availableSheets():
                Options.warning("Cheat sheet not found.", "", self._wf)
                return None
            ret = self._parser.searchInSheet(keyword, sheetName, self._wf)
        if ret == []:
            Options.warning(f"Not found in {sheetName}", f"No match found for search {keyword}", self._wf)
            return None
        for item in ret:
            self._wf.add_item(
                    title=item["command"],
                    subtitle=item["comment"],
                    copytext=item.get("command"),
                    valid=True,
                    arg=item.get("command"),
                    largetext=self.LARGETEXTPATTERN.format(item.get("command"), item.get("comment"))
                    ).add_modifier(
                    'cmd',
                    subtitle="Open in editor",
                    valid=True,
                    arg=self._parser._sheetMapping.get(sheetName))
        return None

    def list(self, sheetName):
        ret = self._parser.list(sheetName)
        if ret == []:
            Options.hint("Empty cheatsheet", "", self._wf)
        for item in ret:
            self._wf.add_item(
                    title=item.get("command"),
                    subtitle=item.get("comment"),
                    valid=True,
                    copytext=item.get("command"),
                    arg=item.get("command"),
                    largetext=self.LARGETEXTPATTERN.format(item.get("command"), item.get("comment"))
                    ).add_modifier(
                    'cmd',
                    subtitle="Open in editor",
                    valid=True,
                    arg=self._parser._sheetMapping.get(sheetName))
        return None

    def showAvailable(self, sheetName=""):
        ret = self.filterSheetName(sheetName)
        if ret == []:
            Options.warning("Cheat sheet not found.", "", self._wf)
            return None
        for sheet in ret:
            sheet_path, sheet_name = os.path.split(sheet)
            self._wf.add_item(
                    title=sheet_name,
                    subtitle=sheet_path,
                    autocomplete=f"{sheet} ",
                    largetext=sheet
                    ).add_modifier(
                    'cmd',
                    subtitle="Open in editor",
                    valid=True,
                    arg=self._parser._sheetMapping.get(sheet))
        return None

    def filterSheetName(self, query):
        names = self._parser.availableSheets()
        return self._wf.filter(query, names)

    @staticmethod
    def warning(msg, subtitle, wf):
        wf.warn_empty(
                title=msg,
                subtitle=subtitle,
                icon=WARNINGICON,
                )
        return None

    @staticmethod
    def hint(msg, subtitle, wf):
        wf.warn_empty(
                title=msg,
                subtitle=subtitle,
                icon=HINT,
                )
        return None
