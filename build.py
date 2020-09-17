#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import configparser
import copy
import platform
import os
import shutil

from conans import tools
from cpt.ci_manager import CIManager
from cpt.packager import ConanMultiPackager
from cpt.printer import Printer

def parse_args():
    parser = argparse.ArgumentParser(description='Build package from conan-center-index')
    parser.add_argument('--shared', action="store_true", help='Build shared libraries')
    parser.add_argument('--static', action="store_true", help='Build static libraries')
    return parser.parse_args()


def parse_config():
    config = configparser.ConfigParser()
    config.read('build.cfg')
    if not config.has_section('package'):
        raise Exception("Malformed build.cfg: [package] section is missing")

    package = config['package']
    if 'name' in package and 'version' in package:
        return package

    raise Exception('Malformed build.cfg: "name" and "version" options in [package] section are mandatory')


def apply_patches(patch_dir, target_dir):
    if os.path.isdir(patch_dir):
        for f in sorted(os.listdir(patch_dir)):
            patch_path = os.path.join(patch_dir, f)
            print(f"Applying {patch_path} to {target_dir}...")
            tools.patch(base_path=target_dir, patch_file=patch_path)


def move_files_from_recipe(package_name, recipe_subdir):
    recipe_dir = f"{os.path.dirname(__file__)}/conan-center-index/recipes/{package_name}/{recipe_subdir}"
    for f in os.listdir(recipe_dir):
        shutil.move(os.path.join(recipe_dir, f), f)


def is_tag():
    printer = Printer()
    ci_manager = CIManager(printer)
    return ci_manager.is_tag()


def set_env_variable_if_undefined(var, value):
    if not var in os.environ:
        os.environ[var] = value
    print(f"Environment: {var} = {os.environ[var]}")


def set_variables():
    set_env_variable_if_undefined("CONAN_USERNAME", "qtproject")
    set_env_variable_if_undefined("CONAN_LOGIN_USERNAME", "qtbot")
    set_env_variable_if_undefined("CONAN_ARCHS", "x86,x86_64")
    set_env_variable_if_undefined("CONAN_VISUAL_RUNTIMES", "MD,MDd")
    set_env_variable_if_undefined("CONAN_REVISIONS_ENABLED", "1")

    production_repo = "https://api.bintray.com/conan/qtproject/conan@True@qtproject"
    testing_repo = "https://api.bintray.com/conan/qtproject/conan-testing@True@qtproject-testing"

    if is_tag():
        set_env_variable_if_undefined("CONAN_UPLOAD", production_repo)
        set_env_variable_if_undefined("CONAN_REMOTES", production_repo)
        set_env_variable_if_undefined("CONAN_CHANNEL", "stable")
    else:
        set_env_variable_if_undefined("CONAN_UPLOAD", testing_repo)
        set_env_variable_if_undefined("CONAN_REMOTES", f"{testing_repo}, {production_repo}")


if __name__ == "__main__":
    args = parse_args()
    package = parse_config()
    package_name = package.get('name')
    package_version = package.get('version')
    recipe_subdir = package.get('recipe_subdir', 'all')

    apply_patches("patches", f"{os.path.dirname(__file__)}/conan-center-index")
    move_files_from_recipe(package_name, recipe_subdir)
    set_variables()

    builder = ConanMultiPackager(reference=f"{package_name}/{package_version}")
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
