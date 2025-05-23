#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from workflow import Workflow
from libs.parser import Parser
from libs.options import Options

# GitHub repo for self-updating
UPDATE_SETTINGS = {'github_slug': 'harrtho/alfred-cheat-sheets'}

# GitHub Issues
HELP_URL = 'https://github.com/harrtho/alfred-cheat-sheets/issues'

# Icon shown if a newer version is available
ICON_UPDATE = 'update-available.png'

def main(wf):

    # Notify user if update is available
    # ------------------------------------------------------------------
    if wf.update_available:
        wf.add_item('Workflow Update is Available',
                    '↩ or ⇥ to install',
                    autocomplete='workflow:update',
                    valid=False,
                    icon=ICON_UPDATE)

    # Try to read configuration from local disk
    config = wf.stored_data("configuration")
    if config is None:
        Options.warning("Didn't find your configuration", "Please supply your cheat sheets path using 'cheatconfig ~/your/path'", wf)
        wf.send_feedback()
        return -1

    parser = Parser(config.getPath())
    # Note: by pasing workflow as a variable, its state is changed in Options.py logic
    options = Options(parser, wf)

    # Query is whatever comes after "cheat". Stored in one single variable
    query = "" if len(wf.args) == 0 else wf.args[0]
    # Split the query into two parts: sheetName and searchTerm
    query_tokens = query.strip().split(" ")
    query_tokens = [i.strip() for i in query_tokens if i != ""]

    # If the query is empty, show available sheets
    if len(query_tokens) == 0:
        options.showAvailable()
        wf.send_feedback()
        return None
    # If the query is "--search" or "-s", show hint for global search
    elif len(query_tokens) == 1 and query_tokens[0] in ("--search", "-s"):
        Options.hint("Globally searching for ...?", "In global mode", wf)
        wf.send_feedback()
        return None
    # If the query is a global search, create a search term
    elif query_tokens[0] in ("--search", "-s"):
        sheetName = None
        searchTerm = ''.join(query_tokens[1:])
    # Search for a sheet name and a search term
    else:
        sheets_tokens = [i.split(" ") for i in parser.availableSheets()]
        sheetName = None
        searchTerm = None
        search_term_index = 0
        # Iterate over all available sheets sorted by length.
        # This is to find the longest sheet name that matches the query
        # and to avoid false positives.
        # For example, if the query is "Fancy Query" and there are sheets "Fancy"
        # and "Fancy Query", we want to match "Fancy Query" and not "Fancy".
        # This is to avoid false positives.
        for sheet_tokens in sorted(sheets_tokens, key=len):
            count_tokens = len(sheet_tokens)

            for index, query_token in enumerate(query_tokens):
                if query_token != sheet_tokens[index]:
                    break

                if index == count_tokens - 1:
                    search_term_index = index + 1
                    sheetName = ' '.join(sheet_tokens)
                    wf.logger.debug(f"found sheet name '{sheetName}' in query '{query}'")
                    break

        if sheetName is None:
            options.showAvailable(' '.join(query_tokens))
            wf.send_feedback()
            return None
        # If there is still more than one option as sheet name, show available sheets
        elif len(options.filterSheetName(' '.join(query_tokens))) - 1 > 0:
            options.showAvailable(' '.join(query_tokens))
            searchTerm = ' '.join(query_tokens[search_term_index:])
            wf.logger.debug(f"extract search term '{searchTerm}' from query '{query}'")
        elif len(query_tokens[search_term_index:]) == 0:
            options.list(sheetName)
            wf.send_feedback()
            return None
        else:
            searchTerm = ' '.join(query_tokens[search_term_index:])
            wf.logger.debug(f"extract search term '{searchTerm}' from query '{query}'")

    options.searchInSheetByKeyword(sheetName, searchTerm)
    wf.send_feedback()
    return None


if __name__ == "__main__":
    wf = Workflow(update_settings=UPDATE_SETTINGS,
                  help_url=HELP_URL)
    sys.exit(wf.run(main))
