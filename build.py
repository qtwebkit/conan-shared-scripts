#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import copy
import platform
import os
import shutil

from cpt.ci_manager import CIManager
from cpt.packager import ConanMultiPackager
from cpt.printer import Printer

def parse_args():
    parser = argparse.ArgumentParser(description='Build package from conan-center-index')
    parser.add_argument('package_name', type=str, nargs=1, help='Name of package in conan-center-index repository')
    parser.add_argument('package_version', type=str, nargs=1, help='Package version to build (must be present in config.yml of recipe)')
    parser.add_argument('--shared', action="store_true", help='Build shared libraries')
    parser.add_argument('--static', action="store_true", help='Build static libraries')
    return parser.parse_args()


def move_files_from_recipe(package_name):
    os.chdir(os.path.dirname(__file__))
    recipe_path = os.path.join("conan-center-index", "recipes", package_name, "all")
    for f in os.listdir(recipe_path):
        shutil.move(os.path.join(recipe_path, f), f)


def is_tag():
    printer = Printer()
    ci_manager = CIManager(printer)
    return ci_manager.is_tag()


def set_variables():
    os.environ["CONAN_USERNAME"] = "qtproject"
    os.environ["CONAN_LOGIN_USERNAME"] = "qtbot"
    os.environ["CONAN_ARCHS"] = "x86,x86_64"
    os.environ["CONAN_VISUAL_RUNTIMES"] = "MD,MDd"
    os.environ["CONAN_REVISIONS_ENABLED"] = "1"

    production_repo = "https://api.bintray.com/conan/qtproject/conan@True@qtproject"
    testing_repo = "https://api.bintray.com/conan/qtproject/conan-testing@True@qtproject-testing"

    if is_tag():
        os.environ["CONAN_UPLOAD"] = production_repo
        os.environ["CONAN_REMOTES"] = production_repo
    else:
        os.environ["CONAN_UPLOAD"] = testing_repo
        os.environ["CONAN_REMOTES"] = ", ".join([testing_repo, production_repo])


if __name__ == "__main__":
    args = parse_args()
    package_name = args.package_name[0]
    package_version = args.package_version[0]
    package_reference = package_name + "/" + package_version
    move_files_from_recipe(package_name)
    set_variables()

    builder = ConanMultiPackager(reference=package_reference)
    builder.add_common_builds()

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
