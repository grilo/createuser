#!/usr/bin/env python

import masking.generator.base
import masking.locale.name


class Name(masking.generator.base.Type):

    def __init__(self, country, value):
        super(Name, self).__init__(country, value)
