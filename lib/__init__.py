#!/usr/bin/env python
# encoding: utf-8
"""Bindet die Abhängigkeiten ein."""

import os.path
import site

site.addsitedir(os.path.dirname(__file__))