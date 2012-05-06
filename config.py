#!/usr/bin/env python
# encoding: utf-8
"""
config.py - general configuration sample for gaetk

Created by Maximillian Dornseif on 2010-09-28.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

# pylint: disable=C0103

# importing lib automatically extends sys.path
import lib
lib.imported = True

import os

template_dirs = []
template_dirs.append(os.path.join(os.path.dirname(__file__), 'templates'))


import logging
import warnings


# Die Parameternamen sind vorgegeben, da können wir nichts verbessern.
# pylint: disable=W0613,W0622,R0913
def _customwarn(message, category, filename, lineno, file=None, line=None):
    """Ensure that warning-messages go to the AppEngine log"""
    logging.warn(warnings.formatwarning(message, category, filename, lineno))
# pylint: enable=W0613,W0622,R0913


warnings.showwarning = _customwarn
warnings.filterwarnings("once")

def main():
    """show path for usage in scripts"""
    import sys
    print ':'.join(sys.path)

if __name__ == '__main__':
    main()
