# cache/dto/DTOManager.py
#
# This module provides the mechanism to manage Data transfer objects (DTO), for conversion of data into JSON and other formats
# This is initialized during initialization of cache configuration
#
# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# 
# Maintained By: dan@reciprocitylabs.com
#


"""
    DTOManager provides the encapsulation to Data Transfer Objects (DTO)

"""

from collection import OrderedList

class DTOManager
  config = None
  dtoList = OrderedList()

  def __init__(self):
    pass

  def setConfig(self, config):
    self.config = config

  def getDTOs(self):
    return None

  def setDTOs(self, dto)
    return None

  def removeDTO(self, dto): 
   return None
