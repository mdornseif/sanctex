#!/usr/bin/env python
# encoding: utf-8

# created november 2009 by danielroseman for Hudora GmbH

from django.core.management import execute_manager

import settings # Assumed to be in the same directory.

if __name__ == "__main__":
    execute_manager(settings)