# -*- coding: utf-8 -*-

__title__ = "requestions"
__version__ = "0.0.1"
__build__ = 0x000001
__author__ = "Bryan Bishop <kanzure@gmail.com>"
__license__ = "BSD"
__copyright__ = "Copyright 2013 Bryan Bishop <kanzure@gmail.com>"

from . import utils

from .io import (
    write_request,
    write_response,
    read_request,
    read_response,
)
