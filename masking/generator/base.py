#!/usr/bin/env python

class Type(object):

    def __init__(self, country, value):
        self.country = country
        self.value = value

    @property
    def mask(self):
        """
            This property should be overridden by each implementation.
        """
        return self.value
