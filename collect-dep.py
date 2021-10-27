#!/usr/bin/env python3
# Copyright (c) 2021 Phi srl

import sys
import os
import odoo
from functools import reduce

# usage:
# . venv/bin/activate
# collect-dep.py --addons-path=...

if __name__ == "__main__":
    args = sys.argv[1:]

    odoo.tools.config._parse_config(args)
    odoo.modules.initialize_sys_path()
    available_modules = set(odoo.modules.get_modules())
    required_modules = dict()
    for module in available_modules:
        required_modules[module] = set(odoo.modules.load_information_from_description_file(module).get("depends"))
    missing_modules = reduce(set.union, required_modules.values(), set()) - available_modules

    for missing in missing_modules:
       for module, requirements in required_modules.items():
            if missing in requirements:
               print("{0} required by {1}".format(missing, module))
