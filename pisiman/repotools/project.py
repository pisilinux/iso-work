#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import re
import hashlib
import platform
import piksemel

import packages
from repotools.packages import PackageCollection, PackageSet


# no i18n yet
def _(x):
    return x


# Find out python version
PYTHON_VER = ".".join(platform.python_version_tuple()[0:2])

QT_PREFIX = "usr"
if os.path.exists("/usr/lib/qt5/libQtCore.so"):
    QT_PREFIX += "/lib/qt5"

# paketlerde kırılmalara sebep olmaması için değiştirildi
# default_live_exclude_list = """
# lib/rcscripts/
# usr/lib/python%s/lib-tk/
# usr/lib/python%s/idlelib/
# usr/lib/python%s/bsddb/test/
# usr/lib/python%s/lib-old/
# usr/lib/python%s/test/
# usr/lib/klibc/include/
# usr/share/aclocal/
# usr/share/info/
# usr/share/sip/
# usr/share/man/
# usr/share/groff/
# usr/share/dict/
# var/db/pisi/
# var/cache/pisi/archives/
# var/tmp/pisi/
# var/pisi/
# tmp/pisi-root/
# var/log/comar.log
# var/log/pisi.log
# root/.bash_history
# """ % ((PYTHON_VER,)*5)
# var/cache/pisi/packages/

default_live_exclude_list = """
var/db/pisi/
var/cache/pisi/archives/
var/tmp/pisi/
var/pisi/
tmp/pisi-root/
var/log/comar.log
var/log/pisi.log
root/.bash_history
"""

# default_install_exclude_list = """
# lib/rcscripts/
# usr/lib/cups/
# usr/lib/python%s/lib-tk/
# usr/lib/python%s/idlelib/
# usr/lib/python%s/bsddb/test/
# usr/lib/python%s/lib-old/
# usr/lib/python%s/test/
# usr/lib/python%s/site-packages/PyQt5/QtAssistant.so
# usr/lib/python%s/site-packages/PyQt5/QtDesigner.so
# usr/lib/python%s/site-packages/PyQt5/QtHelp.so
# usr/lib/python%s/site-packages/PyQt5/QtNetwork.so
# usr/lib/python%s/site-packages/PyQt5/QtOpenGL.so
# usr/lib/python%s/site-packages/PyQt5/QtScript.so
# usr/lib/python%s/site-packages/PyQt5/QtSql.so
# usr/lib/python%s/site-packages/PyQt5/QtTest.so
# usr/lib/python%s/site-packages/PyQt5/QtWebKit.so
# usr/lib/python%s/site-packages/PyQt5/QtXml.so
# usr/lib/python%s/site-packages/PyQt5/QtXmlPatterns.so
# usr/lib/klibc/include/
# usr/lib/syslinux/
# usr/share/aclocal/
# usr/share/cups/
# usr/share/alsa
# usr/share/doc/
# usr/share/gfxtheme/
# usr/share/info/
# usr/share/sip/
# usr/share/man/
# usr/share/groff/
# usr/share/dict/
# var/db/pisi/
# var/lib/pisi/
# var/cache/pisi/packages/
# var/cache/pisi/archives/
# var/tmp/pisi/
# var/pisi/
# tmp/pisi-root/
# var/log/comar.log
# var/log/pisi.log
# root/.bash_history
# """ % ((PYTHON_VER,)*16)

default_install_exclude_list = """
var/db/pisi/
var/cache/pisi/archives/
var/tmp/pisi/
var/pisi/
tmp/pisi-root/
var/log/comar.log
var/log/pisi.log
root/.bash_history
"""

default_install_glob_excludes = (
    # ("usr/lib/python%s/" % PYTHON_VER, "*.pyc"),
    # ("usr/lib/python%s/" % PYTHON_VER, "*.pyo"),
    # ("usr/lib/pardus/", "*.pyc"),
    # ("usr/lib/pardus/", "*.pyo"),
    # ("usr/lib/", "*.a"),
    # ("usr/lib/", "*.la"),
    # ("lib/", "*.a"),
    # ("lib/", "*.la"),
    ("var/db/comar/", "__db*"),
    ("var/db/comar/", "log.*"),
    # ("%s/lib/" % QT_PREFIX, "libphononexperimental.so*"),
    # ("%s/lib/" % QT_PREFIX, "libphonon.so*"),
    # ("%s/lib/" % QT_PREFIX, "libqca.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQt3Support.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtAssistantClient.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtCLucene.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtDBus.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtDesignerComponents.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtDesigner.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtHelp.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtMultimedia*"),
    # ("%s/lib/" % QT_PREFIX, "libQtNetwork.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtOpenGL.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtScript.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtScriptTools.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtSql.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtTapioca.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtTelepathyClient.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtTest.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtUiTools.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtWebKit.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtXmlPatterns.so*"),
    # ("%s/lib/" % QT_PREFIX, "libQtXml.so*"),
)

default_live_glob_excludes = (
    # ("usr/lib/python%s/" % PYTHON_VER, "*.pyc"),
    # ("usr/lib/python%s/" % PYTHON_VER, "*.pyo"),
    # ("usr/lib/pardus/", "*.pyc"),
    # ("usr/lib/pardus/", "*.pyo"),
    # ("usr/lib/", "*.a"),
    # ("usr/lib/", "*.la"),
    # ("lib/", "*.a"),
    # ("lib/", "*.la"),
    ("var/db/comar/", "__db*"),
    ("var/db/comar/", "log.*"),
    # ("var/lib/pisi/index/", "*"),
    # ("var/lib/pisi/info", "*"),
    # ("var/lib/pisi/package", "*"),
    # ("var/cache/pisi", "*.cache"),
)


class ExProject(Exception):
    pass


class ExProjectMissing(Exception):
    pass


class ExProjectBogus(Exception):
    pass

# Project class


class Project:
    def __init__(self):
        self.reset()

    def reset(self):
        self.filename = None
        self.title = ""
        self.work_dir = ""
        self.release_files = ""
        self.repo_uri = ""
        self.live_repo_uri = ""
        self.type = "install"
        self.squashfs_comp_type = "xz"
        self.extra_params = ""
        self.plugin_package = ""
        self.default_language = None
        self.selected_languages = []
        self.selected_components = []
        self.selected_packages = []
        self.all_packages = []
        self.package_collections = []
        self.missing_packages = []
        self.missing_components = []
        self.selected_install_image_components = []
        self.selected_install_image_packages = []
        self.all_install_image_packages = []
        self.use_project_dir_as_output_dir = True
        self.iso_output_dir = ""

    def guessReleaseFiles(self):
        if "project-files" in self.filename:
            # Obeys to the uludag/trunk/distribution hierarchy, nice.
            releaseFiles = self.filename.split("project-files/")[0]+"media-content"
            if os.path.exists(releaseFiles):
                return releaseFiles

    def open(self, filename):
        # Open and parse project file filename
        try:
            doc = piksemel.parse(filename)
        except OSError, e:
            if e.errno == 2:
                raise ExProjectMissing
            raise
        except piksemel.ParseError:
            raise ExProjectBogus
        if doc.name() != "PardusmanProject":
            raise ExProjectBogus

        self.reset()
        self.filename = filename

        # Try to guess releaseFiles location
        self.release_files = self.guessReleaseFiles()

        # Fill in the properties from XML file
        self.title = doc.getTagData("Title")
        self.type = doc.getAttribute("type")
        self.squashfs_comp_type = doc.getAttribute("compression")

        self.plugin_package = doc.getTagData("PluginPackage")
        if not self.plugin_package:
            self.plugin_package = ""
        if not self.release_files:
            self.release_files = doc.getTagData("ReleaseFiles")
        self.extra_params = doc.getTagData("ExtraParameters")
        if not self.extra_params:
            self.extra_params = ""
        self.work_dir = doc.getTagData("WorkDir")
        if not self.work_dir:
            self.work_dir = ""
        self.live_repo_uri = doc.getTagData("LiveRepo")
        if not self.live_repo_uri:
            self.live_repo_uri = ""


        self.iso_output_dir = doc.getTagData("IsoOutputDir")
        # print("iso_output_dir:", self.iso_output_dir)
        if not self.iso_output_dir:
            self.iso_output_dir = ""
            self.all_install_image_packages = True
        else:
            self.use_project_dir_as_output_dir = bool(doc.getTag("IsoOutputDir").getAttribute("use-project-dir"))


        def __packageSelection(node):
            # Fill in the packages
            selectedComponents = [ ]
            selectedPackages = [ ]
            allPackages = [ ]
            if node:
                repoURI = node.getAttribute("repo_uri")
                for tag in node.tags("SelectedComponent"):
                    selectedComponents.append(tag.firstChild().data())
                for tag in node.tags("SelectedPackage"):
                    selectedPackages.append(tag.firstChild().data())
                for tag in node.tags("Package"):
                    allPackages.append(tag.firstChild().data())
                # print repoURI, "\n", selectedComponents, "\n", selectedPackages, "\n", allPackages
                return (repoURI, selectedComponents,
                    selectedPackages, allPackages)
            return None

        def __collectionTranslations(node):
            # Fill collection translations
            translations = {}
            if node:
                for translation in node.tags("Translation"):
                    translations[translation.getAttribute("language")] = (
                        unicode(translation.getTagData("Title")),
                        unicode(translation.getTagData("Description")))
                return translations
            return None

        def __languageSelection(node):
            # Fill the languages
            defaultLanguage = None
            selectedLanguages = []

            if node:
                defaultLanguage = node.getAttribute("default_language")
                for tag in node.tags("Language"):
                    selectedLanguages.append(tag.firstChild().data())

                if defaultLanguage not in selectedLanguages:
                    selectedLanguages.append(defaultLanguage)

                return (defaultLanguage, selectedLanguages)

            return None

        collectionsTag = doc.getTag("PackageCollections")
        if collectionsTag:
            for collection in collectionsTag.tags("PackageCollection"):
                default = collection.getAttribute("default")
                if not default:
                    default = ""

                # Reads Collection identifiers
                id = collection.getTagData("Id")
                icon = collection.getTagData("Icon")

                # Reads Collection Translations
                translations = __collectionTranslations(collection.getTag("Translations"))

                # Reads Collection Selected Packages
                uri, selectedcomponents, selectedpackages, allPackages = __packageSelection(collection.getTag("PackageSelection"))
                packages = PackageSet(uri, selectedcomponents, selectedpackages, allPackages)

                self.package_collections.append(PackageCollection(id, icon, translations, packages, default))

            # Hack for now.Change After multi repository support
            self.repo_uri = self.package_collections[0].packages.repoURI

            for collection in self.package_collections:
                collection.packages.selectedComponents.sort()
                collection.packages.selectedPackages.sort()
                collection.packages.allPackages.sort()
        else:
            packageSelectionTag = doc.getTag("PackageSelection")
            if packageSelectionTag:
                self.repo_uri, self.selected_components, self.selected_packages, self.all_packages = __packageSelection(packageSelectionTag)

            self.selected_components.sort()
            self.selected_packages.sort()
            self.all_packages.sort()

        languageSelectionTag = doc.getTag("LanguageSelection")
        if languageSelectionTag:
            self.default_language, self.selected_languages = __languageSelection(languageSelectionTag)

        installImagePackagesTag = doc.getTag("InstallImagePackages")
        if installImagePackagesTag:
            uri, \
            self.selected_install_image_components, \
            self.selected_install_image_packages, \
            self.all_install_image_packages = __packageSelection(installImagePackagesTag)

            self.selected_install_image_components.sort()
            self.selected_install_image_packages.sort()
            self.all_install_image_packages.sort()
            self.selected_components += self.selected_install_image_components
            self.selected_components.sort()
            self.selected_packages += self.selected_install_image_packages
            self.selected_packages.sort()

    def save(self, filename=None):
        # Save the data into filename as pardusman project file
        doc = piksemel.newDocument("PardusmanProject")

        doc.setAttribute("type", self.type)
        doc.setAttribute("compression", str(self.squashfs_comp_type))

        if self.title:
            doc.insertTag("Title").insertData(self.title)
        if self.work_dir:
            doc.insertTag("WorkDir").insertData(self.work_dir)
        if self.release_files:
            doc.insertTag("ReleaseFiles").insertData(self.release_files)
        if self.plugin_package:
            doc.insertTag("PluginPackage").insertData(self.plugin_package)
        if self.extra_params:
            doc.insertTag("ExtraParameters").insertData(self.extra_params)
        if self.live_repo_uri:
            doc.insertTag("LiveRepo").insertData(self.live_repo_uri)

        iso_output = doc.insertTag("IsoOutputDir")
        iso_output.insertData(self.iso_output_dir)
        print(self.iso_output_dir)

        if self.use_project_dir_as_output_dir:
            #doc.insertTag("UseProjectDir").insertData(self.use_project_dir_as_output_dir)
            iso_output.setAttribute("use-project-dir", "True")
        else:
            iso_output.setAttribute("use-project-dir", "")


        if self.package_collections:
            collections = doc.insertTag("PackageCollections")
            for collection in self.package_collections:
                packageCollection = collections.insertTag("PackageCollection")
                # Writes if collection is default
                if collection.default:
                    packageCollection.setAttribute("default", collection.default)

                # Writes Collection identifiers
                packageCollection.insertTag("Id").insertData(collection._id)
                packageCollection.insertTag("Icon").insertData(collection.icon)

                # Writes Translations
                translations = packageCollection.insertTag("Translations")
                for key, item in collection.translations.items():
                    translation = translations.insertTag("Translation")
                    translation.setAttribute("language", key)
                    translation.insertTag("Title").insertData(item[0])
                    translation.insertTag("Description").insertData(item[1])

                # Writes Packages
                packageSelection = packageCollection.insertTag("PackageSelection")
                # FIXME: ilker manap, self.repo_uri almasi gerek.
                packageSelection.setAttribute("repo_uri", self.repo_uri)
                for item in collection.packages.selectedComponents:
                    packageSelection.insertTag("SelectedComponent").insertData(item)
                for item in collection.packages.selectedPackages:
                    packageSelection.insertTag("SelectedPackage").insertData(item)
                for item in collection.packages.allPackages:
                    packageSelection.insertTag("Package").insertData(item)

                packageSelection = doc.insertTag("InstallImagePackages")
                for item in collection.packages.selectedComponents:
                    packageSelection.insertTag("SelectedComponent").insertData(item)
                for item in collection.packages.selectedPackages:
                    packageSelection.insertTag("SelectedPackage").insertData(item)
                for item in collection.packages.allPackages:
                    packageSelection.insertTag("Package").insertData(item)

        else:
            self.selected_components.sort()
            self.selected_packages.sort()
            self.all_packages.sort()

            package_selection = doc.insertTag("PackageSelection")
            package_selection.setAttribute("repo_uri", self.repo_uri)

            # Insert components if any
            for item in self.selected_components:
                package_selection.insertTag("SelectedComponent").insertData(item)

            for item in self.selected_packages:
                package_selection.insertTag("SelectedPackage").insertData(item)

            for item in self.all_packages:
                package_selection.insertTag("Package").insertData(item)


        if self.all_install_image_packages:
            self.selected_install_image_components.sort()
            self.selected_install_image_packages.sort()
            self.all_install_image_packages.sort()

            package_selection = doc.insertTag("InstallImagePackages")

            # Insert components if any
            for item in self.selected_install_image_components:
                package_selection.insertTag("SelectedComponent").insertData(item)

            for item in self.selected_install_image_packages:
                package_selection.insertTag("SelectedPackage").insertData(item)

            for item in self.all_install_image_packages:
                package_selection.insertTag("Package").insertData(item)

            inst = doc.insertTag("installationPackages")
            inst.insertTag("peri").insertData(item)

        if self.default_language:
            # Set the default language
            langs = doc.insertTag("LanguageSelection")
            langs.setAttribute("default_language", self.default_language)

            # Insert other supported languages if any
            for item in self.selected_languages:
                langs.insertTag("Language").insertData(item)

        # Write the file
        if not filename:
            filename = self.filename
        f = file(filename, "w")
        f.write(doc.toPrettyString())
        f.close()

    def exclude_list(self):
        import fnmatch

        def _glob_exclude(lst, excludes):
            image_dir = self.image_dir()
            for exc in excludes:
                path = os.path.join(image_dir, exc[0])
                for root, dirs, files in os.walk(path):
                    for name in files:
                        if fnmatch.fnmatch(name, exc[1]):
                            lst.append(os.path.join(root[len(image_dir)+1:], name))

        if self.type == "install":
            temp = default_install_exclude_list.split()
            _glob_exclude(temp, default_install_glob_excludes)
        else:
            temp = default_live_exclude_list.split()
            _glob_exclude(temp, default_live_glob_excludes)
        return temp

    def _get_dir(self, name, clean=False):
        dirname = os.path.join(self.work_dir, name)
        if os.path.exists(dirname):
            if clean:
                os.system('rm -rf "%s"' % dirname)
                os.makedirs(dirname)
        else:
            os.makedirs(dirname)
        return dirname

    def get_repo(self, console=None, update_repo=False):
        cache_dir = self._get_dir("repo_cache")
        repo = packages.Repository(self.repo_uri, cache_dir)
        repo.parse_index(console, update_repo)
        self.find_all_packages(repo)
        return repo

    def get_missing(self):
        return self.missing_components, self.missing_packages

    def find_all_packages(self, repo):
        self.missing_packages = []
        self.missing_components = []
        packages = []
        self.all_packages = []

        def collect(name):
            if name not in repo.packages:
                if name not in self.missing_packages:
                    self.missing_packages.append(name)
                return
            p = repo.packages[name]
            if name in packages:
                return
            packages.append(name)
            for dep in p.depends:
                collect(dep)

        if self.package_collections:
            for collection in self.package_collections:
                packages = []
                for component in collection.packages.selectedComponents:
                    if component not in repo.components:
                        if component not in self.missing_components:
                            self.missing_components.append(component)
                        return
                    for package in repo.components[component]:
                        collect(package)

                for package in collection.packages.selectedPackages:
                    collect(package)

                packages.sort()
                collection.packages.allPackages = packages
            self.all_packages.extend(packages)
        else:
            for component in self.selected_components:
                if component not in repo.components:
                    if component not in self.missing_components:
                        self.missing_components.append(component)
                    return
                for package in repo.components[component]:
                    collect(package)

            for package in self.selected_packages:
                collect(package)

            packages.sort()
            self.all_packages = packages

        self.all_packages.sort()

        # Find all install image packages
        packages = []
        self.all_install_image_packages = []

        for component in self.selected_install_image_components:
            if component not in repo.components:
                if component not in self.missing_components:
                    self.missing_components.append(component)
                return
            for package in repo.components[component]:
                collect(package)

        for package in self.selected_install_image_packages:
            collect(package)

        packages.sort()
        self.all_install_image_packages = packages

    def image_repo_dir(self, clean=False):
        return self._get_dir("image_repo", clean)

    def image_dir(self, clean=False):
        return self._get_dir("image", clean)

    def image_file(self):
        return os.path.join(self.work_dir, "pisi.sqfs")

    def install_repo_dir(self, clean=False):
        return self._get_dir("install_repo", clean)

    def efi_tmp_path_dir(self, clean=False):
        return self._get_dir("efi_tmp", clean)

    def iso_dir(self, clean=False):
        return self._get_dir("iso", clean)

    def iso_file(self, clean=True):
        filename = self.title.replace(" ", "-")
        filename = re.sub("[()]", "", filename)
        if self.use_project_dir_as_output_dir:
            path = os.path.join(self.work_dir, "%s.iso" % filename)
        else:
            path = os.path.join(self.iso_output_dir, "%s.iso" % filename)

        if clean and os.path.exists(path):
            os.unlink(path)
        return path

    def display_manager(self):
        for dm in ["sddm", "lxdm", "lightdm", "gdm", "xdm"]:
            if dm in self.all_install_image_packages:
                return dm

        return None
