#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import copy
import platform
import os
import shutil

from bincrafters import build_template_default

def parse_args():
    parser = argparse.ArgumentParser(description='Build package from conan-center-index')
    parser.add_argument('package_name', type=str, nargs=1, help='Name of package in conan-center-index repository')
    parser.add_argument('--shared', action="store_true", help='Build shared libraries')
    parser.add_argument('--static', action="store_true", help='Build static libraries')
    return parser.parse_args()


def move_files_from_recipe(package_name):
    os.chdir(os.path.dirname(__file__))
    recipe_path = os.path.join("conan-center-index", "recipes", package_name, "all")
    for f in os.listdir(recipe_path):
        shutil.move(os.path.join(recipe_path, f), f)


if __name__ == "__main__":
    args = parse_args()
    package_name = args.package_name[0]
    move_files_from_recipe(package_name)

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
