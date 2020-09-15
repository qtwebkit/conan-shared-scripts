#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import copy
import platform
import os
import shutil

from bincrafters import build_template_default

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build package from conan-center-index')
    parser.add_argument('package_name', type=str, nargs=1, help='Name of package in conan-center-index repository')
    parser.add_argument('--shared', action="store_true", help='Build shared libraries')
    parser.add_argument('--static', action="store_true", help='Build static libraries')
    args = parser.parse_args()

    package_name = args.package_name[0]

    os.system("git submodule update --init conan-center-index")
    subdir = "conan-center-index/recipes/{}/all".format(package_name)
    for f in os.listdir(subdir):
        shutil.move(os.path.join(subdir, f), f)

    builder = build_template_default.get_builder(pure_c=True)

    items = []
    for item in builder.items:
        if item.options[package_name + ":shared"]:
            if args.shared:
                items.append(item)
        else:
            if args.static:
                items.append(item)
    builder.items = items

    builder.run()
