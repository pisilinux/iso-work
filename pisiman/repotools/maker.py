#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import sys
import stat
import time
import dbus
import glob
import shutil
import hashlib
import tempfile

from repotools.utility import xterm_title, wait_bus

#
# Utilities
#

def run(cmd, ignore_error=False):
    print cmd
    ret = os.system(cmd)
    if ret and not ignore_error:
        print "%s returned %s" % (cmd, ret)
        sys.exit(1)

def connectToDBus(path):
    global bus
    bus = None
    for i in range(20):
        try:
            print("trying to start dbus..")
            bus = dbus.bus.BusConnection(address_or_type="unix:path=%s/run/dbus/system_bus_socket" % path)
            break
        except dbus.DBusException:
            time.sleep(1)
            print("wait dbus for 1 second...")
    if bus:
        return True
    return False

def chroot_comar(image_dir):
    if os.fork() == 0:
        # Workaround for creating ISO's on 2007 with PiSi 2.*
        # Create non-existing /var/db directory before running COMAR
        try:
            os.makedirs(os.path.join(image_dir, "var/db"), 0700)
        except OSError:
            pass
        os.chroot(image_dir)
        if not os.path.exists("/var/lib/dbus/machine-id"):
            run("/usr/bin/dbus-uuidgen --ensure")

        run("/sbin/start-stop-daemon -b --start --pidfile /run/dbus/pid --exec /usr/bin/dbus-daemon -- --system")
        sys.exit(0)
    wait_bus("%s/run/dbus/system_bus_socket" % image_dir)

def get_exclude_list(project):
    exc = project.exclude_list()[:]
    image_dir = project.image_dir()
    path = image_dir + "/boot"
    for name in os.listdir(path):
        if name.startswith("kernel") or name.startswith("initramfs"):
            exc.append("boot/" + name)
    return exc

#
# Grub related stuff
#

def generate_grub_conf(project, kernel, initramfs):
    print "Generating grub.conf files..."
    xterm_title("Generating grub.conf files")

    image_dir = project.image_dir()
    iso_dir = project.iso_dir()

    grub_dict = {}
    grub_dict["kernel"] = kernel
    grub_dict["initramfs"] = initramfs
    grub_dict["title"] = project.title
    grub_dict["exparams"] = project.extra_params or ''

    path = os.path.join(image_dir, "usr/share/grub/templates")
    dest = os.path.join(iso_dir, "boot/grub")
    for name in os.listdir(path):
        if name.startswith("menu"):
            data = file(os.path.join(path, name)).read()
            f = file(os.path.join(dest, name), "w")
            f.write(data % grub_dict)
            f.close()

def setup_grub(project):
    image_dir = project.image_dir()
    iso_dir = project.iso_dir()
    kernel = ""
    initramfs = ""

    # Setup dir
    path = os.path.join(iso_dir, "boot/grub")
    if not os.path.exists(path):
        os.makedirs(path)

    def copy(src, dest):
        run('cp -P "%s" "%s"' % (src, os.path.join(iso_dir, dest)))

    # Copy the kernel and initramfs
    path = os.path.join(image_dir, "boot")
    for name in os.listdir(path):
        if name.startswith("kernel") or name.startswith("initramfs") or name.endswith(".bin"):
            if name.startswith("kernel"):
                kernel = name
            elif name.startswith("initramfs"):
                initramfs = name
            copy(os.path.join(path, name), "boot/" + name)

    #??and the other files
    path = os.path.join(image_dir, "boot/grub")
    for name in os.listdir(path):
        copy(os.path.join(path, name), "boot/grub/" + name)

    # Generate the config file
    generate_grub_conf(project, kernel, initramfs)

def generate_isolinux_conf(project):
    print "Generating isolinux config files..."
    xterm_title("Generating isolinux config files")

    dict = {}
    dict["title"] = project.title
    dict["exparams"] = project.extra_params or ''
    dict["rescue_template"] = ""

    image_dir = project.image_dir()
    iso_dir = project.iso_dir()

    lang_default = project.default_language
    lang_all = project.selected_languages

    if project.type != "live":
        dict["rescue_template"] = """
label rescue
    kernel /boot/kernel
    append initrd=/boot/initrd yali=rescue %(exparams)s
""" % dict

    isolinux_tmpl = """
prompt 1
timeout 200

ui gfxboot.c32 /boot/isolinux/init

label pisilinux
    kernel /boot/kernel
    append initrd=/boot/initrd %(exparams)s

%(rescue_template)s

label harddisk
    localboot 0x80

label memtest
    kernel /boot/memtest

label hardware
    kernel hdt.c32
"""

    # write isolinux.cfg
    dest = os.path.join(iso_dir, "boot/isolinux/isolinux.cfg")
    data = isolinux_tmpl % dict

    f = file(dest, "w")
    f.write(data % dict)
    f.close()

    # write gfxboot config for title
    data = file(os.path.join(image_dir, "usr/share/gfxtheme/pisilinux/install/gfxboot.cfg")).read()
    f = file(os.path.join(iso_dir, "boot/isolinux/gfxboot.cfg"), "w")
    f.write(data % dict)
    f.close()

    if len(lang_all) and lang_default != "":
        langdata = ""

        if not lang_default in lang_all:
            lang_all.append(lang_default)

        lang_all.sort()

        for i in lang_all:
            langdata += "%s\n" % i


        # write default language
        f = file(os.path.join(iso_dir, "boot/isolinux/lang"), "w")
        f.write("%s\n" % lang_default)
        f.close()

        # FIXME: this is the default language selection, make it selectable
        # when this file does not exist, isolinux pops up language menu
        if os.path.exists(os.path.join(iso_dir, "boot/isolinux/lang")):
            os.unlink(os.path.join(iso_dir, "boot/isolinux/lang"))

        # write available languages
        f = file(os.path.join(iso_dir, "boot/isolinux/languages"), "w")
        f.write(langdata)
        f.close()


def setup_isolinux(project):
    print "Generating isolinux files..."
    xterm_title("Generating isolinux files")

    image_dir = project.image_dir()
    iso_dir = project.iso_dir()
    repo = project.get_repo()

    # Setup dir
    path = os.path.join(iso_dir, "boot/isolinux")
    if not os.path.exists(path):
        os.makedirs(path)

    def copy(src, dest):
        run('cp -P "%s" "%s"' % (src, os.path.join(iso_dir, dest)))

    # Copy the kernel and initramfs
    path = os.path.join(image_dir, "boot")
    for name in os.listdir(path):
        if name.startswith("kernel") or name.startswith("initramfs") or name.endswith(".bin"):
            if name.startswith("kernel"):
                copy(os.path.join(path, name), "boot/kernel")
            elif name.startswith("initramfs"):
                copy(os.path.join(path, name), "boot/initrd")

    tmplpath = os.path.join(image_dir, "usr/share/gfxtheme/pisilinux/install")
    dest = os.path.join(iso_dir, "boot/isolinux")
    for name in os.listdir(tmplpath):
        if name != "gfxboot.cfg":
            copy(os.path.join(tmplpath, name), dest)

    # copy config and gfxboot stuff
    generate_isolinux_conf(project)

    # we don't use debug anymore for the sake of hybrid
    copy(os.path.join(image_dir, "usr/lib/syslinux/isolinux.bin"), "%s/isolinux.bin" % dest)
    copy(os.path.join(image_dir, "usr/lib/syslinux/hdt.c32"), dest)
    copy(os.path.join(image_dir, "usr/lib/syslinux/gfxboot.c32"), dest)
    copy(os.path.join(image_dir, "usr/share/misc/pci.ids"), dest)

    kernel_version = open(os.path.join(image_dir, "etc/kernel/kernel")).read()
    #copy(os.path.join(image_dir, "lib/modules/%s/modules.pcimap" % kernel_version), dest)
    copy(os.path.join(image_dir, "boot/memtest"), os.path.join(iso_dir, "boot"))

#
# Image related stuff
#

def setup_live_kdm(project):
    image_dir = project.image_dir()
    kdmrc_path = os.path.join(image_dir, "etc/X11/kdm/kdmrc")
    if os.path.exists(kdmrc_path):
        lines = []
        for line in open(kdmrc_path, "r").readlines():
            if line.startswith("#AutoLoginEnable"):
                lines.append("AutoLoginEnable=true\n")
            elif line.startswith("#AutoLoginUser"):
                lines.append("AutoLoginUser=pisi\n")
            elif line.startswith("#ServerTimeout="):
                lines.append("ServerTimeout=60\n")
            else:
                lines.append(line)
        open(kdmrc_path, "w").write("".join(lines))
    else:
        print "*** %s doesn't exist, setup_live_kdm() returned" % kdmrc_path

def setup_live_policykit_conf(project):
    policykit_conf_tmpl = """[Live CD Rules]
Identity=unix-user:pisi
Action=*
ResultAny=yes
ResultInactive=yes
ResultActive=yes
"""

    # Write PolicyKit.conf
    image_dir = project.image_dir()
    # make sure etc/polkit-1/localauthority/90-mandatory.d directory exists
    os.makedirs(os.path.join(image_dir, "etc/polkit-1/localauthority/90-mandatory.d"), 0644)
    dest = os.path.join(image_dir, "etc/polkit-1/localauthority/90-mandatory.d/livecd.pkla")

    f = file(dest, "w")
    f.write(policykit_conf_tmpl)
    f.close()

def copyPisiIndex(project):
    image_dir = project.image_dir()
    if project.package_collections:
        destination = os.path.join(image_dir, "usr/share/yali/data")
        collectionDir = os.path.join(destination, "index")
        collectionFile = os.path.join(destination, "index/collection.xml")
        run('mkdir -p %s' % collectionDir)
        run('cp -PR "%s" "%s"' % (os.path.join(project.install_repo_dir(), "collection.xml"), collectionDir))
        run('sha1sum "%s" > "%s"' % (collectionFile, "%s.sha1sum" % collectionFile))

        for collection in project.package_collections:
            source = os.path.join(project.install_repo_dir(), "%s-index.xml.bz2" % collection._id)
            run('cp -PR "%s" "%s"' % (source, collectionDir))
            run('sha1sum "%s" > "%s"' % (source, "%s.sha1sum" % os.path.join(collectionDir, os.path.basename(source))))
            #run('cp -PR "%s" "%s"' % (os.path.join(os.getcwd(), "icons", collection.icon), collectionDir))
            #print('cp -PR "%s" "%s"' % (source, collectionDir))
            #print('sha1sum "%s" > "%s"' % (source, "%s.sha1sum" % os.path.join(collectionDir,os.path.basename(source))))
            #print('cp -PR "%s" "%s"' % (collection.icon, collectionDir))

    # Copy All Collection Packages index as pisi index dvd and default cd installation
    yali_data_dir = os.path.join(image_dir, "usr/share/yali/data")
    if not os.path.exists(yali_data_dir):
        print "Creating data directory for YALI..."
        run('mkdir -p %s' % yali_data_dir)
    path = os.path.join(image_dir, "usr/share/yali/data/%s" % os.path.basename(project.repo_uri))
    repo = os.path.join(project.work_dir, "repo_cache/%s" % os.path.basename(project.repo_uri))

    run('cp -PR "%s" "%s"' % (repo, path))
    run('sha1sum "%s" > "%s"' % (repo, "%s.sha1sum" % path))
    print('cp -PR "%s" "%s"' % (repo, path))
    print('sha1sum "%s" > "%s"' % (repo, "%s.sha1sum" % path))

def install_packages(project):
    image_dir = project.image_dir()
    path = os.path.join(image_dir, "var/lib/pisi/package")
    print "len(project.all_packages:%s" % len(project.all_packages)
    run('pisi --yes-all --ignore-comar --ignore-dependency --ignore-file-conflicts -D"%s" it %s ' % (image_dir, " ".join(project.all_packages)))
    # --ignore-dep added to avoid dependencies re not in system.base like exceptions
    #for name in project.all_packages:
        #flag = True
        #if os.path.exists(path):
            #for avail in os.listdir(path):
                #if avail.startswith(name) and avail[len(name)] == "-":
                    #flag = False
        #if flag:
            #run('pisi --yes-all --ignore-comar --ignore-file-conflicts -D"%s" it %s ' % (image_dir, name))
     ##commented from "for line" above
def squash_image(project):
    image_dir = project.image_dir()
    image_file = project.image_file()

    print "squashfs image dir%s" % image_dir
    if not image_dir.endswith("/"):
        image_dir += "/"
    print "later squashfs image dir%s" % image_dir
    temp = tempfile.NamedTemporaryFile()
    f = file(temp.name, "w")
    f.write("\n".join(get_exclude_list(project)))
    f.close()

    mksquashfs_cmd = 'mksquashfs "%s" "%s" -noappend -comp %s -ef "%s"' % (image_dir, image_file, project.squashfs_comp_type, temp.name)
    run(mksquashfs_cmd)

#
# Operations
#

def make_repos(project):
    print "Preparing image repo..."
    xterm_title("Preparing repo")

    try:
        repo = project.get_repo()
        repo_dir = project.image_repo_dir(clean=True)
        if project.type == "install":
            imagedeps = project.all_install_image_packages or repo.full_deps("yali")
            xterm_title("Preparing image repo for installation")
        else:
            imagedeps = project.all_packages
            xterm_title("Preparing image repo for live")

        repo.make_local_repo(repo_dir, imagedeps)

        if project.type == "install":
            xterm_title("Preparing installination repo")
            print "Preparing installation repository..."

            repo_dir = project.install_repo_dir(clean=True)
            if project.package_collections:
                all_packages = []
                for collection in project.package_collections:
                    all_packages.extend(collection.packages.allPackages)
                    # Making repos and index files per collection
                    repo.make_local_repo(repo_dir, collection.packages.allPackages, collection._id)

                repo.make_local_repo(repo_dir, all_packages)
                repo.make_collection_index(repo_dir, project.package_collections, project.default_language)
                print "Preparing collections project file"
            else:
                repo.make_local_repo(repo_dir, project.all_packages)

    except KeyboardInterrupt:
        print "Keyboard Interrupt: make_repo() cancelled."
        sys.exit(1)

def check_file(repo_dir, name, _hash):
    path = os.path.join(repo_dir, name)
    if not os.path.exists(path):
        print "\nPackage missing: %s" % path
        return
    data = file(path).read()
    cur_hash = hashlib.sha1(data).hexdigest()
    if cur_hash != _hash:
        print "\nWrong hash: %s" % path

def check_repo_files(project):
    print "Checking image repo..."
    xterm_title("Checking image repo")

    try:
        repo = project.get_repo()
        repo_dir = project.image_repo_dir()
        if project.type == "install":
            imagedeps = project.all_install_image_packages or repo.full_deps("yali")
        else:
            imagedeps = project.all_packages
        i = 0
        for name in imagedeps:
            i += 1
            sys.stdout.write("\r%-70.70s" % "Checking %d of %s packages" % (i, len(imagedeps)))
            sys.stdout.flush()
            pak = repo.packages[name]
            check_file(repo_dir, pak.uri, pak.sha1sum)
        sys.stdout.write("\n")

        if project.type == "install":
            repo_dir = project.install_repo_dir()
            i = 0
            for name in project.all_packages:
                i += 1
                sys.stdout.write("\r%-70.70s" % "Checking %d of %s packages" % (i, len(project.all_packages)))
                sys.stdout.flush()
                pak = repo.packages[name]
                check_file(repo_dir, pak.uri, pak.sha1sum)
        sys.stdout.write("\n")
    except KeyboardInterrupt:
        print "Keyboard Interrupt: check_repo() cancelled."
        sys.exit(1)

def make_image(project):
    global bus

    print "Preparing install image..."
    xterm_title("Preparing install image")

    try:
        repo = project.get_repo()
        repo_dir = project.image_repo_dir()
#        image_file = project.image_file()

        image_dir = project.image_dir()
        run('umount %s/proc' % image_dir, ignore_error=True)
        run('umount %s/sys' % image_dir, ignore_error=True)
        image_dir = project.image_dir(clean=True)
        run('pisi --yes-all -D"%s" ar pisilinux-install %s --ignore-check' % (image_dir, repo_dir + "/pisi-index.xml.bz2"))
        if project.type == "install":
            if project.all_install_image_packages:
                install_image_packages = " ".join(project.all_install_image_packages)
            else:
                install_image_packages = " ".join(repo.full_deps("yali"))
            run('pisi --yes-all --ignore-comar --ignore-dep -D"%s" it %s' % (image_dir, install_image_packages))
            if project.plugin_package:
                plugin_package = project.plugin_package
                run('pisi --yes-all --ignore-comar -D"%s" it %s' % (image_dir, plugin_package))
        else:
            install_packages(project)

        def chrun(cmd):
            run('chroot "%s" %s' % (image_dir, cmd))


        # FIXME: we write static initramfs.conf for live systems for now, hopefully we will make it dynamic later on
        # Note that this must be done before configure pending for the mkinitramfs use it
        f = file(os.path.join(image_dir, "etc/initramfs.conf"), "w")
        f.write("liveroot=LABEL=PisiLive\n")
        f.close()

        os.mknod("%s/dev/null" % image_dir, 0666 | stat.S_IFCHR, os.makedev(1, 3))
        os.mknod("%s/dev/console" % image_dir, 0666 | stat.S_IFCHR, os.makedev(5, 1))
        os.mknod("%s/dev/random" % image_dir, 0666 | stat.S_IFCHR, os.makedev(1, 8))
        os.mknod("%s/dev/urandom" % image_dir, 0666 | stat.S_IFCHR, os.makedev(1, 9))

        path = "%s/usr/share/baselayout/" % image_dir
        path2 = "%s/etc" % image_dir
        for name in os.listdir(path):
            run('cp -p "%s" "%s"' % (os.path.join(path, name), os.path.join(path2, name)))
        run('/bin/mount --bind /proc %s/proc' % image_dir)
        run('/bin/mount --bind /sys %s/sys' % image_dir)

        #chrun("ln -s /dev/shm /run/shm")
        chrun("/sbin/ldconfig")
        chrun("/sbin/update-environment")
        chroot_comar(image_dir)
        chrun("/usr/bin/pisi configure-pending baselayout")

        chrun("/usr/bin/pisi configure-pending")
        # Disable Nepomuk in live CDs
        if project.type == "live":
            try:
                os.unlink("%s/usr/share/autostart/nepomukserver.desktop" % image_dir)
            except OSError:
                pass

        if project.type == "install":
            # FIXME: Do not hard code installer name
            dm_config ="DISPLAY_MANAGER=yali"

            # Write default display manager config
            image_dir = project.image_dir()
            #dest = os.path.join(image_dir, "etc/conf.d/xdm")
            dest = os.path.join(image_dir, "etc/default/xdm")

            f = file(dest, "w")
            f.write(dm_config)
            f.close()

        connectToDBus(image_dir)

        obj = bus.get_object("tr.org.pardus.comar", "/package/baselayout")

        obj.setUser(0, "", "", "", "pisilinux", "", dbus_interface="tr.org.pardus.comar.User.Manager")
        if project.type != "install":
            obj.addUser(1000, "pisi", "Pisi Linux", "/home/pisi", "/bin/bash", "pisilinux", ["wheel", "users", "lp", "lpadmin", "cdrom", "floppy", "disk", "audio", "video", "power", "dialout"], [], [], dbus_interface="tr.org.pardus.comar.User.Manager")

        path1 = os.path.join(image_dir, "usr/share/baselayout/inittab.live")
        path2 = os.path.join(image_dir, "etc/inittab")
        os.unlink(path2)
        run('mv "%s" "%s"' % (path1, path2))


        if project.type != "install" and ("kde-workspace" in project.all_packages):
            setup_live_kdm(project)
            setup_live_policykit_conf(project)

        if project.type == "install":
            copyPisiIndex(project)

        # Make sure environment is updated regardless of the booting system, by setting comparison
        # files' atime and mtime to UNIX time 1

        os.utime(os.path.join(image_dir, "etc/profile.env"), (1, 1))

        #chrun('killall comar')
        run('umount %s/proc' % image_dir)
        run('umount %s/sys' % image_dir)
        chrun("rm -rf /run/dbus/*")
    except KeyboardInterrupt:
        print "Keyboard Interrupt: make_image() cancelled."
        sys.exit(1)

def generate_sort_list(iso_dir):
    # Sorts the packages in repo_dir according to their size
    # mkisofs sort_file format:
    # filename   weight
    # where filename is the whole name of a file/directory and the weight is a whole
    # number between +/- 2147483647. Files will be sorted with the highest weights first
    # and lowest last. The CDs are written from the middle outwards.
    # High weighted files will be nearer to the inside of the CD.
    # Highest weight -> nearer to the inside,
    # lowest weight -> outwards
    packages = glob.glob("%s/repo/*.pisi" % iso_dir)
    package_list = dict([(k, os.stat(k).st_size) for k in packages]).items()
    package_list.sort(key=lambda x: x[1], reverse=True)

    for i in xrange(len(packages)):
        package_list.insert(i, (package_list.pop(i)[0], 100+10*i))

    # Move baselayout to the top
    for p in package_list:
        if "baselayout" in p[0]:
            package_list.insert(0, package_list.pop(package_list.index(p)))

    return package_list


def make_iso(project):
    print "Preparing ISO..."
    xterm_title("Preparing ISO")

    sort_cd_layout = False

    try:
        iso_dir = project.iso_dir(clean=True)
        iso_file = project.iso_file(clean=True)
        #image_dir = project.image_dir()
        image_file = project.image_file()
        image_path = os.path.join(iso_dir, "boot")

        if not os.path.exists(image_path):
            os.makedirs(image_path)
        os.link(image_file, os.path.join(iso_dir, "boot/pisi.sqfs"))

        def copy(src, dest):
            dest = os.path.join(iso_dir, dest)

            if os.path.isdir(src):
                shutil.copytree(src, dest, ignore=shutil.ignore_patterns(".svn"))
            else:
                shutil.copy2(src, dest)

        if project.release_files:
            # Allow ~ usage in project xml files
            path = os.path.expanduser(project.release_files)
            for name in os.listdir(path):
                if name != ".svn":
                    copy(os.path.join(path, name), name)

        # setup_grub(project)
        setup_isolinux(project)

        if project.type == "install":
            run('ln -s "%s" "%s"' % (project.install_repo_dir(), os.path.join(iso_dir, "repo")))

        publisher="Pisi GNU/Linux http://www.pisilinux.org"
        application="Pisi GNU/Linux Live Media"
        label="PisiLive"

        the_sorted_iso_command='genisoimage -f -sort %s/repo/install.order -J -r -l -V "%s" -o "%s" -b boot/isolinux/isolinux.bin -c boot/isolinux/boot.cat -boot-info-table \
-uid 0 -gid 0 -udf -allow-limited-size -iso-level 3 -input-charset utf-8 -no-emul-boot -boot-load-size 4 \
-publisher "%s" -A "%s"  %s' % (iso_dir, label, iso_file, publisher, application, iso_dir)

        the_iso_command='genisoimage -f -J -r -l -V "%s" -o "%s" -b boot/isolinux/isolinux.bin -c boot/isolinux/boot.cat -boot-info-table \
-uid 0 -gid 0 -udf -allow-limited-size -iso-level 3 -input-charset utf-8 -no-emul-boot -boot-load-size 4 \
-publisher "%s" -A "%s"  %s' % (label, iso_file, publisher, application, iso_dir)

        # Generate sort_list for mkisofs and YALI
        # Disabled for now
        if sort_cd_layout:
            sorted_list = generate_sort_list(iso_dir)
            if sorted_list:
                open("%s/repo/install.order" % iso_dir, "w").write("\n".join(["%s %d" % (k,v) for (k,v) in sorted_list]))
                run(the_sorted_iso_command)

        else:
            run(the_iso_command)
        # convert iso to a hybrid one
        run("isohybrid %s" % iso_file)

    except KeyboardInterrupt:
        print "Keyboard Interrupt: make_iso() cancelled."
        sys.exit(1)
