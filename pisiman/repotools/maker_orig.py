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
import subprocess

# import pathlib2

from repotools.utility import xterm_title, wait_bus

#
# Utilities
#


def run_batch(cmd, shell=True, env=os.environ.copy()):
    proc = subprocess.Popen(
        cmd, shell=shell, env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    out, err = proc.communicate()

    return (proc.returncode, out, err)


def run(cmd, ignore_error=False):
    print(cmd)
    ret = os.system(cmd)
    if ret and not ignore_error:
        print("%s returned %s" % (cmd, ret))
        sys.exit(1)


def bind(path="dev", project):
    image_dir = project.image_dir()
    iso_dir = project.iso_dir()
    overlay_dir = "{}/overlay".format(iso_dir)
    if not os.path.exists(overlay_dir):
        os.makedirs(overlay_dir)
    run('/bin/mount -t overlay overlay -o lowerdir=/{path},upperdir={overlay_dir}/upper_{path},workdir={overlay_dir}/work_{path} {image_dir}/{path}'.format(overlay_dir, path, image_dir))

def unbind(path, project):
    image_dir = project.image_dir()
    run('/bin/umount  {image_dir}/{path}'.format(path, image_dir))

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
            os.makedirs(os.path.join(image_dir, "var/db"), 0o700)
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
    # image_dir = project.image_dir()
    # path = image_dir + "/boot"
    # for name in os.listdir(path):
    #     if name.startswith("kernel") or name.startswith("initramfs"):
    #         exc.append("boot/" + name)
    return exc


# efi için dosyaların eklenmesi
def setup_efi(project):
    image_dir = project.image_dir()
    iso_dir = project.iso_dir()

    def copy(src, dest):
        run('cp -PR "%s" "%s"' % (src, os.path.join(iso_dir, dest)))

    path = "./data/efi"
    for name in os.listdir(path):
        copy(os.path.join(path, name), name)

    copy("./data/isomounts", "pisi")

    path = os.path.join(image_dir, "boot")
    for name in os.listdir(path):
        if name.startswith("kernel") or name.startswith("initr") or name.endswith(".bin"):
        # if name.startswith("kernel") or name == "initrd":
            if name.startswith("kernel"):
                copy(os.path.join(path, name), "EFI/pisi/kernel.efi")
            elif name.startswith("initr"):
                copy(os.path.join(path, name), "EFI/pisi/initrd.img")


# def mkinitcpio(project, prog="mkinitcpio"):
def mkinitcpio(project):
    try:
        image_dir = project.image_dir()
        # iso_dir = project.iso_dir()

        run('umount %s/dev' % image_dir, ignore_error=True)
        run('umount %s/proc' % image_dir, ignore_error=True)
        run('umount %s/sys' % image_dir, ignore_error=True)

        def chrun(cmd):
            run('chroot "%s" %s' % (image_dir, cmd))

        def copy2(src, dest):
            run('cp -PR "%s" "%s"' % (src, os.path.join(image_dir, dest)))

        # initcpio
        rep = project.get_repo()
        print("mkinitcpio" in project.all_install_image_packages)
        # print(rep.packages.keys())
        if "mkinitcpio" in project.all_install_image_packages:
            prog = "mkinitcpio"
            binary = os.path.join("/usr/bin", prog)
            config_path = "/etc/mkinitcpio-live.conf"
            extra_args = " -g /boot/initrd"
            path = "./data/initcpio"
            copy2(path, "usr/lib")
            copy2("./data/mkinitcpio-live.conf", "etc")
        elif "mkinitramfs" in project.all_install_image_packages:
            prog = "mkinitramfs"
            binary = os.path.join("/sbin", prog)
            config_path = "/etc/initramfs.conf"
            extra_args = ""
            # FIXME: init dosyası mkinitramfs paketindeki ile değiştirilmeli
            copy2("./data/initramfs", "lib")

        # path = os.path.join(image_dir, "boot/pisi")
        # if not os.path.exists(path):
        #    os.makedirs(path)

        run('/bin/mount --bind /dev %s/dev' % image_dir)
        run('/bin/mount --bind /proc %s/proc' % image_dir)
        run('/bin/mount --bind /sys %s/sys' % image_dir)


        kernel_version = rep.packages['kernel'].version

        chrun(" ".join([binary, "-k", kernel_version,
                       "-c %s" % config_path, extra_args]))
        # FIXME: kurulmuş sistem init dosyalarını yalı oluşturmalı
        # ???
        # if prog == "mkinitcpio":
        #     chrun(" ".join([binary, "-k", kernel_version, "-g",
        #                 "/boot/initramfs-%s-fallback.img" % kernel_version,
        #                 "-S", "autodetect"]))
        #     # bu kısım yalıya taşınmalı
        #     chrun(" ".join([binary, "-k", kernel_version,
        #                 "-c", "/etc/mkinitcpio.conf",
        #                 "-g", "/boot/initramfs-%s.img" % kernel_version]))

        run('umount %s/dev' % image_dir)
        run('umount %s/proc' % image_dir)
        run('umount %s/sys' % image_dir)
    except KeyboardInterrupt:
        print("Keyboard Interrupt: make_image() cancelled.")
        sys.exit(1)

#
# Grub related stuff
#


def generate_grub_conf(project, kernel, initramfs):
    print("Generating grub.conf files...")
    xterm_title("Generating grub.conf files")

    image_dir = project.image_dir()
    iso_dir = project.iso_dir()

    grub_dict = {}
    grub_dict["kernel"] = kernel
    grub_dict["initramfs"] = initramfs
    grub_dict["title"] = project.title
    grub_dict["exparams"] = project.extra_params or ''

    path = os.path.join(image_dir, "usr/share/grub/templates")
    dest = os.path.join(iso_dir, "pisi/boot/grub")
    for name in os.listdir(path):
        if name.startswith("menu"):
            data = open(os.path.join(path, name)).read()
            f = open(os.path.join(dest, name), "w")
            f.write(data % grub_dict)
            f.close()


def setup_grub(project):
    image_dir = project.image_dir()
    iso_dir = project.iso_dir()
    kernel = ""
    initramfs = ""

    # Setup dir
    path = os.path.join(iso_dir, "pisi/boot/grub")
    if not os.path.exists(path):
        os.makedirs(path)

    def copy(src, dest):
        run('cp -P "%s" "%s"' % (src, os.path.join(iso_dir, dest)))

    # Copy the kernel and initramfs
    path = os.path.join(image_dir, "boot")
    for name in os.listdir(path):
        if name.startswith("kernel") or name.startswith("initramfs") or name.startswith("initrd") or name.endswith(".bin"):
            if name.startswith("kernel"):
                kernel = name
            elif name.startswith("initramfs"):
                initramfs = name
            elif name.startswith("initrd"):
                initramfs = name
            copy(os.path.join(path, name), "pisi/boot/" + name)
    # and the other files
    path = os.path.join(image_dir, "pisi/boot/grub")
    for name in os.listdir(path):
        copy(os.path.join(path, name), "boot/grub/" + name)

    # Generate the config file
    generate_grub_conf(project, kernel, initramfs)


def generate_isolinux_conf(project):
    print("Generating isolinux config files...")
    xterm_title("Generating isolinux config files")

    dict = {}
    dict["title"] = project.title
    dict["exparams"] = project.extra_params or ''
    dict["rescue_template"] = ""

    if "mkinitcpio" in project.all_install_image_packages:
        dict['exparams'] += " misobasedir=pisi misolabel=pisilive overlay=free"

    image_dir = project.image_dir()
    iso_dir = project.iso_dir()

    lang_default = project.default_language
    lang_all = project.selected_languages

    if project.type != "live":
        dict["rescue_template"] = """
label rescue
    kernel /pisi/boot/kernel
    append initrd=/pisi/boot/initrd yali=rescue %(exparams)s
""" % dict
    else:
        dict['exparams'] += "mudur=livecd"

    isolinux_tmpl = """
default start
implicit 1
ui gfxboot bootlogo
prompt   1
timeout  200

label %(title)s
    kernel /pisi/boot/kernel
    append initrd=/pisi/boot/initrd %(exparams)s

%(rescue_template)s

label harddisk
    localboot 0x80

label memtest
    kernel /pisi/boot/memtest

label hardware
    kernel hdt.c32
"""

    # write isolinux.cfg
    dest = os.path.join(iso_dir, "isolinux/isolinux.cfg")
    data = isolinux_tmpl % dict

    f = open(dest, "w")
    f.write(data % dict)
    f.close()

    # write gfxboot config for title
    data = open(os.path.join(image_dir, "usr/share/gfxtheme/pisilinux/install/gfxboot.cfg")).read()
    f = open(os.path.join(iso_dir, "isolinux/gfxboot.cfg"), "w")
    f.write(data % dict)
    f.close()

    if len(lang_all) and lang_default != "":
        langdata = ""

        if lang_default not in lang_all:
            lang_all.append(lang_default)

        lang_all.sort()

        for i in lang_all:
            langdata += "%s\n" % i

        # write default language
        f = open(os.path.join(iso_dir, "isolinux/lang"), "w")
        f.write("%s\n" % lang_default)
        f.close()

        # FIXME: this is the default language selection, make it selectable
        # when this file does not exist, isolinux pops up language menu
        if os.path.exists(os.path.join(iso_dir, "isolinux/lang")):
            os.unlink(os.path.join(iso_dir, "isolinux/lang"))

        # write available languages
        f = open(os.path.join(iso_dir, "isolinux/languages"), "w")
        f.write(langdata)
        f.close()


def setup_isolinux(project):
    print("Generating isolinux files...")
    xterm_title("Generating isolinux files")

    image_dir = project.image_dir()
    iso_dir = project.iso_dir()
    repo = project.get_repo()

    # Setup dir
    path = os.path.join(iso_dir, "isolinux")
    if not os.path.exists(path):
        os.makedirs(path)

    path = os.path.join(iso_dir, "pisi/boot")
    if not os.path.exists(path):
        os.makedirs(path)

    def copy(src, dest):
        run('cp -P "%s" "%s"' % (src, os.path.join(iso_dir, dest)))

    # Copy the kernel and initramfs
    path = os.path.join(image_dir, "boot")
    for name in os.listdir(path):
        print(name)
        if name.startswith("kernel") or name.startswith("initr") or name.endswith(".bin"):
        # if name.startswith("kernel") or name == "initrd":
            if name.startswith("kernel"):
                copy(os.path.join(path, name), "pisi/boot/kernel")
            # elif name == "initrd":  # or name.startswith("initramfs"):
            elif name == "initrd" or name.startswith("initramfs"):
                copy(os.path.join(path, name), "pisi/boot/initrd")

    tmplpath = os.path.join(image_dir, "usr/share/gfxtheme/pisilinux/install")
    dest = os.path.join(iso_dir, "isolinux")
    for name in os.listdir(tmplpath):
        if name != "gfxboot.cfg":
            copy(os.path.join(tmplpath, name), dest)

    # copy config and gfxboot stuff
    generate_isolinux_conf(project)

    # we don't use debug anymore for the sake of hybrid
    copy(os.path.join(image_dir, "usr/lib/syslinux/bios/isolinux.bin"), "%s/isolinux.bin" % dest)
    copy(os.path.join(image_dir, "usr/lib/syslinux/bios/isohdpfx.bin"), "%s/isohdpfx.bin" % dest)
    copy(os.path.join(image_dir, "usr/lib/syslinux/bios/hdt.c32"), dest)

    # for boot new syslinux
    copy(os.path.join(image_dir, "usr/lib/syslinux/bios/ldlinux.c32"), dest)
    copy(os.path.join(image_dir, "usr/lib/syslinux/bios/libcom32.c32"), dest)
    copy(os.path.join(image_dir, "usr/lib/syslinux/bios/libutil.c32"), dest)
    copy(os.path.join(image_dir, "usr/lib/syslinux/bios/vesamenu.c32"), dest)
    copy(os.path.join(image_dir, "usr/lib/syslinux/bios/libmenu.c32"), dest)
    copy(os.path.join(image_dir, "usr/lib/syslinux/bios/libgpl.c32"), dest)

    copy(os.path.join(image_dir, "usr/lib/syslinux/bios/gfxboot.c32"), dest)
    copy(os.path.join(image_dir, "usr/share/misc/pci.ids"), dest)

    kernel_version = open(os.path.join(image_dir, "etc/kernel/kernel")).read()
    # copy(os.path.join(image_dir, "lib/modules/%s/modules.pcimap" % kernel_version), dest)
    copy(os.path.join(image_dir, "boot/memtest"), os.path.join(iso_dir, "pisi/boot"))


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
        print("*** %s doesn't exist, setup_live_kdm() returned" % kdmrc_path)

## KONTROL EDİLECEK
## squash_image içinden kaldırılacak!
# def setup_live_sddm(project):
#     import ConfigParser
#     image_dir = project.image_dir()
#
#     try:
#         sddm_file = "%s/etc/sddm.conf" % image_dir
#         sddm_conf = ConfigParser.ConfigParser(allow_no_value=True)
#         sddm_conf.optionxform = str
#
#         sddm_conf.read(sddm_file)
#         sddm_conf.set("Autologin", "User", "pisi")
#         sddm_conf.set("Autologin", "Session", "plasma.desktop")
#         for s in sddm_conf.sections():
#             print(sddm_conf.items(s, raw=True))
#         dosya = open(sddm_file, "w")
#         sddm_conf.write(dosya)
#     except Exception as e:
#         print("sddm ayarları değiştirilemedi")
#         print("Hata:", e)
#     finally:
#         dosya.close()
#
#     # try:
#     #     if not os.path.exists("{}/etc/sddm.conf.d".format(image_dir)):
#     #         shutil.copytree("data/kde_conf/sddm.conf.d",
#     #                         "{}/etc/sddm.conf.d".format(image_dir))
#     # except Exception as e:
#     #     print("sddm ayarı kopyalanamadı")
#     #     print("Hata:", e)
#     #     sys.exit(1)

# FIXME: bu yapıandırma liveconfig isinli sqfs dosyasına aktarılacak!
def setup_live_sddm(project):
    image_dir = project.image_dir()
    sddmconf_path = os.path.join(image_dir, "etc/sddm.conf")
    if os.path.exists(sddmconf_path):
        lines = []
        for line in open(sddmconf_path, "r").readlines():
            if line.startswith("User="):
                lines.append("User=pisi\n")
            elif line.startswith("Session="):
                # lines.append("Session=/usr/share/xsessions/plasma-mediacenter\n") #this code may be have an error
                lines.append("Session=plasma.desktop\n")
            # elif line.startswith("#ServerTimeout="):
            #    lines.append("ServerTimeout=60\n")
            else:
                lines.append(line)
        open(sddmconf_path, "w").write("".join(lines))
    else:
        print("*** {} doesn't exist, setup_live_sddm() returned".format(
            sddmconf_path))

# FIXME: bu yapıandırma liveconfig isinli sqfs dosyasına aktarılacak!
def setup_live_lxdm(project):
    image_dir = project.image_dir()
    lxdmconf_path = os.path.join(image_dir, "etc/lxdm/lxdm.conf")
    if os.path.exists(lxdmconf_path):
        lines = []
        for line in open(lxdmconf_path, "r").readlines():
            if line.startswith("# autologin=") or line.startswith("autologin="):
                lines.append("autologin=pisi\n")
            elif line.startswith("session="):
                if os.path.exists("%s/usr/bin/mate-session" % image_dir):
                    lines.append("session=/usr/bin/mate-session\n")
                elif os.path.exists("%s/usr/bin/startxfce4" % image_dir):
                    lines.append("session=/usr/bin/startxfce4\n")
            else:
                lines.append(line)
        open(lxdmconf_path, "w").write("".join(lines))
    else:
        print("*** {} doesn't exist, setup_live_lxdm() returned".format(
            lxdmconf_path))


def setup_live_dm(project, dm):
    if dm == "sddm":
        setup_live_sddm(project)
    elif dm == "lxdm":
        setup_live_lxdm(project)


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
    os.makedirs(os.path.join(image_dir, "etc/polkit-1/localauthority/90-mandatory.d"), 0o644)
    dest = os.path.join(image_dir, "etc/polkit-1/localauthority/90-mandatory.d/livecd.pkla")

    f = open(dest, "w")
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
            # run('cp -PR "%s" "%s"' % (os.path.join(os.getcwd(), "icons", collection.icon), collectionDir))
            # print('cp -PR "%s" "%s"' % (source, collectionDir))
            # print('sha1sum "%s" > "%s"' % (source, "%s.sha1sum" % os.path.join(collectionDir,os.path.basename(source))))
            # print('cp -PR "%s" "%s"' % (collection.icon, collectionDir))

    # Copy All Collection Packages index as pisi index dvd and default cd installation
    yali_data_dir = os.path.join(image_dir, "usr/share/yali/data")
    if not os.path.exists(yali_data_dir):
        print("Creating data directory for YALI...")
        run('mkdir -p %s' % yali_data_dir)
    path = os.path.join(image_dir, "usr/share/yali/data/%s" % os.path.basename(project.repo_uri))
    repo = os.path.join(project.work_dir, "repo_cache/%s" % os.path.basename(project.repo_uri))

    run('cp -PR "%s" "%s"' % (repo, path))
    run('sha1sum "%s" > "%s"' % (repo, "%s.sha1sum" % path))
    print('cp -PR "%s" "%s"' % (repo, path))
    print('sha1sum "%s" > "%s"' % (repo, "%s.sha1sum" % path))


def install_packages(project):
    image_dir = project.image_dir()
    # path = os.path.join(image_dir, "var/lib/pisi/package")

    # print("len(project.all_packages:%s" % len(project.all_install_image_packages))
    if 'Calamares' in project.all_packages:
        packages = project.all_packages
    else:
        packages = project.all_install_image_packages  # or repo.full_deps("yali")
    run('pisi --yes-all --ignore-comar --ignore-dependency \
        --ignore-file-conflicts -D"%s" it %s \
        ' % (image_dir, " ".join(packages)))
    # --ignore-dep added to avoid dependencies re not in system.base like exceptions
    # for name in project.all_packages:
    #     flag = True
    #     if os.path.exists(path):
    #         for avail in os.listdir(path):
    #             if avail.startswith(name) and avail[len(name)] == "-":
    #                 flag = False
    #     if flag:
    #         run('pisi --yes-all --ignore-comar --ignore-file-conflicts -D"%s" it %s ' % (image_dir, name))
    # commented from "for line" above

def squash_live_config_image(project):
    work_dir = project.work_dir
    image_dir = project.image_dir()
    config_image_dir = os.path.join(work_dir, "config_image")

    if not os.path.exists(config_image_dir):
        os.makedirs(config_image_dir)


    if project.type == "live":
        # cp2skel("./data/yali/yali.desktop", ".config/autostart")
        shutil.copy("./data/yali/yali.desktop",
                    "{}/usr/share/applications/".format(config_image_dir))
        # shutil.copy("./data/yali/yali.desktop",
        #             "{}/home/pisi/.config/autostart/".format(config_image_dir))
        shutil.copy("./data/yali/org.pisilinux.yali.policy",
                    "{}/usr/share/polkit-1/actions/".format(config_image_dir))
        shutil.copy("./data/yali/yali-rescue.desktop",
                    "{}/usr/share/applications/".format(config_image_dir))

        repo = project.get_repo()
        kernel_version = repo.packages['kernel'].version
        autoload_module = "{}/etc/modules.autoload.d/kernel-{}".format(
            config_image_dir, ".".join(kernel_version.split(".")[:2]))

        with open(autoload_module, "w") as autoloads:
            autoloads.write("vfat\n")

        # kurulumda sorun olmaması için değişiklik yapılan paketler tekrar
        # yüklenecek
        print("baselayout package copy to image_dir")
        baselayout_uri = repo.packages["baselayout"].uri
        if not os.path.exists("%s/var/cache/pisi/packages" % repo.cache_dir):
            os.makedirs("%s/var/cache/pisi/packages" % repo.cache_dir)

        os.system("cp -rf %s/%s %s/var/cache/pisi/packages/" % (repo.cache_dir, baselayout_uri, config_image_dir))
        # os.system("cp -rf %s/%s %s/var/cache/pisi/packages/" % (repo.cache_dir, repo.packages['kernel'].uri, config_image_dir))

        # kde yapılandırması ================================================
        if 'plasma-workspace' in project.all_install_image_packages:
            os.system("cp -rf ./data/kde_conf/.config {}/home/pisi".format(config_image_dir))
            os.system("cp -rf ./data/kde_conf/.local {}/home/pisi".format(config_image_dir))
            os.system("cp -rf ./data/kde_conf/xdg/ {}/etc/".format(config_image_dir))
            # os.system("cp -rf ./data/kde_config/.config {}/home/pisi".format(config_image_dir))
            # os.system("cp -rf ./data/kde_config/.local {}/home/pisi".format(config_image_dir))
            chrun("chown -R pisi:wheel /home/pisi/.config")
            chrun("chown -R pisi:wheel /home/pisi/.local")

            # os.system("cp -rf %s/%s %s/var/cache/pisi/packages/" % (repo.cache_dir, repo.packages['sddm'].uri, config_image_dir))

        # kde yapılandırması ================================================
        # setup_live_sddm(project)

        # display manager yapılandırması ====================================
        if project.display_manager() is not None:
            os.system("cp -rf {}/{} {}/var/cache/pisi/packages/".format(
                repo.cache_dir,
                repo.packages[project.display_manager()].uri,
                config_image_dir)
            )
        # display manager yapılandırması ====================================

        if project.type == "install":
            if os.path.exists("%s/run/livemedia" % image_dir):
                run("rm %s/run/livemedia" % image_dir)

            if os.path.exists("%s/home/pisi/.livemedia" % image_dir):
                run("rm %s/home/pisi/.livemedia" % image_dir)
        else:
            run("touch %s/run/livemedia" % image_dir)
            run("touch %s/home/pisi/.livemedia" % image_dir)


def resolve_repo_uri(text):
    """live image için eklenen repoları ayrıştırır"""
    number = 0
    splitted = []
    for t in  text.split(","):
        if len(t.split(":")) > 1:
            adres = t.split(":")

def squash_image(project):
    # mkinitcpio(project)

    image_dir = project.image_dir()
    image_file = project.image_file()

    def chrun(cmd):
        run('chroot "%s" %s' % (image_dir, cmd), ignore_error=True)

    def cp2skel(source, dest):
        if not os.path.exists("{}/etc/skel/{}".format(image_dir, dest)):
            os.makedirs("{}/etc/skel/{}".format(image_dir, dest))
            # pathlib2.Path("{}/etc/skel/{}".format(image_dir, dest)).mkdir(parents=True)
            # pass

        shutil.copy(source, "{}/etc/skel/{}".format(image_dir, dest))

    # FIXME: sonraki sürümlerde live dosyaları ve yapılandırması 2. bir
    # sqfs dosyasına yazılacak! bu sayede silme ya yeniden yapılandırma
    # işlemlerinin büyük bir kısmının yapılmasına gerek kalmayacak
    if project.type == "live":
        # cp2skel("./data/yali/yali.desktop", ".config/autostart")
        shutil.copy("./data/yali/yali.desktop",
                    "{}/usr/share/applications/".format(image_dir))
        # shutil.copy("./data/yali/yali.desktop",
        #             "{}/home/pisi/.config/autostart/".format(image_dir))
        shutil.copy("./data/yali/org.pisilinux.yali.policy",
                    "{}/usr/share/polkit-1/actions/".format(image_dir))
        shutil.copy("./data/yali/yali-rescue.desktop",
                    "{}/usr/share/applications/".format(image_dir))

        if os.path.exists("{}/etc/yali/".format(image_dir)):
            shutil.copy("./data/yali/repos.json",
                    "{}/etc/yali/".format(image_dir))

        repo = project.get_repo()
        kernel_version = repo.packages['kernel'].version
        autoload_module = "{}/etc/modules.autoload.d/kernel-{}".format(
            image_dir, ".".join(kernel_version.split(".")[:2]))
        with open(autoload_module, "w") as autoloads:
            autoloads.write("vfat\n")
        # kurulumda sorun olmaması için değişiklik yapılan paketler tekrar
        # yüklenecek
        print("baselayout package copy to image_dir")
        baselayout_uri = repo.packages["baselayout"].uri
        if not os.path.exists("%s/var/cache/pisi/packages" % repo.cache_dir):
            os.makedirs("%s/var/cache/pisi/packages" % repo.cache_dir)

        os.system("cp -rf %s/%s %s/var/cache/pisi/packages/" % (repo.cache_dir, baselayout_uri, image_dir))
        # os.system("cp -rf %s/%s %s/var/cache/pisi/packages/" % (repo.cache_dir, repo.packages['kernel'].uri, image_dir))

        # kde yapılandırması ================================================
        if 'plasma-workspace' in project.all_install_image_packages:
            os.system("cp -rf ./data/kde_conf/.config {}/home/pisi".format(image_dir))
            os.system("cp -rf ./data/kde_conf/.local {}/home/pisi".format(image_dir))
            os.system("cp -rf ./data/kde_conf/xdg/ {}/etc/".format(image_dir))
            # os.system("cp -rf ./data/kde_config/.config {}/home/pisi".format(image_dir))
            # os.system("cp -rf ./data/kde_config/.local {}/home/pisi".format(image_dir))
            chrun("chown -R pisi:wheel /home/pisi/.config")
            chrun("chown -R pisi:wheel /home/pisi/.local")

            # os.system("cp -rf %s/%s %s/var/cache/pisi/packages/" % (repo.cache_dir, repo.packages['sddm'].uri, image_dir))

        # kde yapılandırması ================================================
        # setup_live_sddm(project)

        # display manager yapılandırması ====================================
        if project.display_manager() is not None:
            os.system("cp -rf {}/{} {}/var/cache/pisi/packages/".format(
                repo.cache_dir,
                repo.packages[project.display_manager()].uri,
                image_dir)
            )
        # display manager yapılandırması ====================================

    # WARNING: bu adım sqfs kurulum ekleneceği için kaldırıldı
    # # paket listesi
    # # tüm paketleri kurmak yerine listedeki paketler kurulacak
    # # daha sonra paketler core ve ortam şeklinde ayrılabilir
    # packages_txt = "%s/usr/share/yali/install_packages.txt" % image_dir
    # # print(project.package_collections[0].packages.allPackages)
    # with open(packages_txt, "w") as _file:
    #     _file.write("\n".join(
    #         project.package_collections[0].packages.allPackages))

    # add repository to live image
    if project.type == "live":
        # print("="*80)
        # print(project.live_repo_uri)
        # print("="*80)
        if project.live_repo_uri:
            # run("cp /etc/resolv.conf {}/etc/".format(image_dir))
            # run('/bin/mount --bind /dev %s/dev' % image_dir)
            # run('/bin/mount --bind /proc %s/proc' % image_dir)
            # run('/bin/mount --bind /tmp %s/tmp' % image_dir)
            # run('/bin/mount --bind /sys %s/sys' % image_dir)
            repo_uris = resolve_repo_uri(project.live_repo_uri)

            run("pisi rr -dy -D'{}' live".format(image_dir), ignore_error=True)
            run("pisi ar -dy -D'{0}' live {1}".format(
                image_dir, project.live_repo_uri))
            run("pisi rr -dy -D'{}' pisilinux-install".format(
                image_dir), ignore_error=True)

            # run('umount %s/dev' % image_dir)
            # run('umount %s/proc' % image_dir)
            # run('umount %s/tmp' % image_dir)
            # run('umount %s/sys' % image_dir)
            # run("chroot '{0}' pisi rdb -dy".format(image_dir),
            #   ignore_error=True)

    if project.type == "install":
        if os.path.exists("%s/run/livemedia" % image_dir):
            run("rm %s/run/livemedia" % image_dir)

        if os.path.exists("%s/home/pisi/.livemedia" % image_dir):
            run("rm %s/home/pisi/.livemedia" % image_dir)
    else:
        run("touch %s/run/livemedia" % image_dir)
        run("touch %s/home/pisi/.livemedia" % image_dir)

    mkinitcpio(project)

    print("squashfs image dir%s" % image_dir)
    if not image_dir.endswith("/"):
        image_dir += "/"
    print("later squashfs image dir%s" % image_dir)
    temp = tempfile.NamedTemporaryFile()
    f = open(temp.name, "w")
    f.write("\n".join(get_exclude_list(project)))
    f.close()

    mksquashfs_cmd = 'mksquashfs "%s" "%s" -noappend -comp %s -ef "%s"' % (
        image_dir, image_file, project.squashfs_comp_type, temp.name)
    run(mksquashfs_cmd)
    with open(os.path.join(project.work_dir, "finished.txt"), 'w') as _file:
        _file.write("pack-live")


#
# Operations
#
def make_repos(project):
    print("Preparing image repo...")
    xterm_title("Preparing repo")

    try:
        repo = project.get_repo(update_repo=True)
        repo_dir = project.image_repo_dir(clean=True)
        if project.type == "install":
            imagedeps = project.all_install_image_packages or \
                repo.full_deps("yali")
            xterm_title("Preparing image repo for installation")
        else:
            if 'Calamares' in project.all_packages:
                imagedeps = project.all_packages
            else:
                imagedeps = project.all_install_image_packages
                # or repo.full_deps("yali")
            xterm_title("Preparing image repo for live")

        repo.make_local_repo(repo_dir, imagedeps)

        # if project.type == "install":
        xterm_title("Preparing installination repo")
        print("Preparing installation repository...")

        repo_dir = project.install_repo_dir(clean=True)
        if project.package_collections:
            all_packages = []
            for collection in project.package_collections:
                all_packages.extend(collection.packages.allPackages)
                # Making repos and index files per collection
                repo.make_local_repo(repo_dir, collection.packages.allPackages,
                                     collection._id)

            repo.make_local_repo(repo_dir, all_packages)
            repo.make_collection_index(repo_dir, project.package_collections,
                                       project.default_language)
            print("Preparing collections project file")
        else:
            repo.make_local_repo(repo_dir, project.all_packages)

        finished_path = os.path.join(project.work_dir, "finished.txt")
        with open(finished_path, 'w') as _file:
            _file.write("make-repo")
    except KeyboardInterrupt:
        print("Keyboard Interrupt: make_repo() cancelled.")
        sys.exit(1)


def check_file(repo_dir, name, _hash):
    path = os.path.join(repo_dir, name)
    if not os.path.exists(path):
        print("\nPackage missing: %s" % path)
        return
    data = open(path).read()
    cur_hash = hashlib.sha1(data).hexdigest()
    if cur_hash != _hash:
        print("\nWrong hash: %s" % path)
        return False
    return True


def check_repo_files(project):
    print("Checking image repo...")
    xterm_title("Checking image repo")

    try:
        repo = project.get_repo()
        repo_dir = project.image_repo_dir()
        if project.type == "install":
            imagedeps = project.all_install_image_packages or \
                repo.full_deps("yali")
        else:
            if 'Calamares' in project.all_packages:
                imagedeps = project.all_packages
            else:
                imagedeps = project.all_install_image_packages
                # or repo.full_deps("yali")

        deps = []
        for pack in imagedeps:
            for dep in list(repo.full_deps(pack)):
                if dep not in deps:
                    deps.append(dep)

        # print(len(deps))  # ## DİKKAT
        missing_pakc = []
        i = 0
        for name in imagedeps:
            i += 1
            sys.stdout.write("\r%-70.70s" % "Checking %d of %s packages" % (
                i, len(imagedeps)))
            sys.stdout.flush()
            pak = repo.packages[name]
            if not check_file(repo_dir, pak.uri, pak.sha1sum):
                missing_pakc.append(name)
        sys.stdout.write("\n")

        # if project.type == "install":
        repo_dir = project.install_repo_dir()
        i = 0
        for name in project.all_packages:
            i += 1
            sys.stdout.write("\r%-70.70s" % "Checking %d of %s packages" % (
                i, len(project.all_packages)))
            sys.stdout.flush()
            pak = repo.packages[name]
            if not check_file(repo_dir, pak.uri, pak.sha1sum):
                if name not in missing_pakc:
                    missing_pakc.append(name)

        sys.stdout.write("\n")

        if len(missing_pakc) > 0:
            missing = os.path.join(project.work_dir, "missing.txt")
            with open(missing, 'w') as _file:
                _file.write("\n".join(missing_pakc))
            print("Some packages has wrong hash")
            sys.exit(1)

        # finished_path = os.path.join(project.work_dir, "finished.txt")
        # with open(finished_path, 'w') as _file:
        #     _file.write("check-repo")
    except KeyboardInterrupt:
        print("Keyboard Interrupt: check_repo() cancelled.")
        sys.exit(1)


def make_image(project):
    global bus

    print("Preparing install image...")
    xterm_title("Preparing install image")

    try:
        repo = project.get_repo()
        repo_dir = project.image_repo_dir()
#        image_file = project.image_file()

        image_dir = project.image_dir()
        run('umount %s/proc' % image_dir, ignore_error=True)
        run('umount %s/sys' % image_dir, ignore_error=True)
        image_dir = project.image_dir(clean=True)
        run('pisi --yes-all -D"%s" ar pisilinux-install %s --ignore-check\
            ' % (image_dir, repo_dir + "/pisi-index.xml.bz2"))
        print("project type = ", project.type)
        if project.type == "install":
            if project.all_install_image_packages:
                install_image_packages = " ".join(
                    project.all_install_image_packages)
            else:
                install_image_packages = " ".join(repo.full_deps("yali"))
            run('pisi --yes-all --ignore-comar --ignore-dep -D"%s" it %s\
                ' % (image_dir, install_image_packages))
            if project.plugin_package:
                plugin_package = project.plugin_package
                run('pisi --yes-all --ignore-comar -D"%s" it %s' % (
                    image_dir, plugin_package))
        else:
            install_packages(project)

        def chrun(cmd):
            run('chroot "%s" %s' % (image_dir, cmd))

        # FIXME: we write static initramfs.conf for live systems for now,
        # hopefully we will make it dynamic later on
        # Note that this must be done before configure pending for the
        # mkinitramfs use it
        f = open(os.path.join(image_dir, "etc/initramfs.conf"), "w")
        # if project.type == "live":
        #     f.write("LIVE=1\n")
        f.write("liveroot=LABEL=PisiLive\n")
        f.close()

        os.mknod("%s/dev/null" % image_dir,
                 0o666 | stat.S_IFCHR, os.makedev(1, 3))
        os.mknod("%s/dev/console" % image_dir,
                 0o666 | stat.S_IFCHR, os.makedev(5, 1))
        os.mknod("%s/dev/random" % image_dir,
                 0o666 | stat.S_IFCHR, os.makedev(1, 8))
        os.mknod("%s/dev/urandom" % image_dir,
                 0o666 | stat.S_IFCHR, os.makedev(1, 9))

        path = "%s/usr/share/baselayout/" % image_dir
        path2 = "%s/etc" % image_dir
        for name in os.listdir(path):
            run('cp -p "%s" "%s"' % (
                os.path.join(path, name), os.path.join(path2, name)))
        run('/bin/mount --bind /proc %s/proc' % image_dir)
        run('/bin/mount --bind /sys %s/sys' % image_dir)

        # chrun("ln -s /dev/shm /run/shm")
        chrun("/sbin/ldconfig")
        chrun("/sbin/update-environment")
        chroot_comar(image_dir)
        chrun("/usr/bin/pisi configure-pending baselayout")

        # WARNING: anlık olarak çıktı vermesini sağla
        def chrun2(cmd, shell=True, env=os.environ.copy()):
            proc = subprocess.Popen(
                'chroot "{}" {}'.format(image_dir, cmd),
                shell=shell, env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            for line in iter(proc.stdout.readline, b''):
                try:
                    print(line[:-1])
                except Exception as e:
                    print(e)
            print(proc.stderr.read())
            proc.poll()
            return proc.returncode
            # return run_batch('chroot "%s" %s' % (image_dir, cmd))

        ret = chrun2("/usr/bin/pisi configure-pending -dv")
        print(ret)
        print("="*80)
        if ret != 0:
            chrun2("service dbus restart")
            chrun2("/usr/bin/pisi configure-pending -dv")

        # Disable Nepomuk in live CDs
        if project.type == "live":
            try:
                os.unlink(
                    "%s/usr/share/autostart/nepomukserver.desktop" % image_dir)
            except OSError:
                pass

        # FIXME: bu yapıandırma liveconfig isinli sqfs dosyasına aktarılacak!
        # -------------------------------------------------------------------
        # if project.type == "install":
        if "xdm" in project.all_install_image_packages:
            # FIXME: Do not hard code installer name
            dm_config = "DISPLAY_MANAGER=yali"

            # Write default display manager config
            image_dir = project.image_dir()
            # dest = os.path.join(image_dir, "etc/conf.d/xdm")
            dest = os.path.join(image_dir, "etc/default/xdm")

            f = open(dest, "w")
            f.write(dm_config)
            f.close()
        # -------------------------------------------------------------------

        connectToDBus(image_dir)

        obj = bus.get_object("tr.org.pardus.comar", "/package/baselayout")

        obj.setUser(0, "", "", "", "pisilinux", "",
                    dbus_interface="tr.org.pardus.comar.User.Manager")
        if project.type != "install":
            obj.addUser(1000, "pisi", "Pisi Linux", "/home/pisi", "/bin/bash",
                        "live", ["wheel", "users", "lp", "lpadmin", "cdrom",
                                 "floppy", "disk", "audio", "video", "power",
                                 "dialout"], [], [],
                        dbus_interface="tr.org.pardus.comar.User.Manager")

        # FIXME: bu yapıandırma liveconfig isinli sqfs dosyasına aktarılacak!
        # -------------------------------------------------------------------
        path1 = os.path.join(image_dir, "usr/share/baselayout/inittab.live")
        path2 = os.path.join(image_dir, "etc/inittab")
        os.unlink(path2)
        run('mv "%s" "%s"' % (path1, path2))

        # if project.type != "install" and ("sddm" in project.all_packages):
        if project.type != "install" and project.display_manager() is not None:
            # setup_live_sddm(project)  # setup_live_sddm olarak değiştirildi
            setup_live_dm(project, project.display_manager())
            setup_live_policykit_conf(project)
        # -------------------------------------------------------------------

        if project.type == "install":
            copyPisiIndex(project)

        # Make sure environment is updated regardless of the booting system,
        # by setting comparison
        # files' atime and mtime to UNIX time 1

        os.utime(os.path.join(image_dir, "etc/profile.env"), (1, 1))

        # chrun('killall comar')
        run('umount %s/proc' % image_dir)
        run('umount %s/sys' % image_dir)
        chrun("rm -rf /run/dbus/*")

        finished_path = os.path.join(project.work_dir, "finished.txt")
        with open(finished_path, 'w') as _file:
            _file.write("make-live")
    except KeyboardInterrupt:
        print("Keyboard Interrupt: make_image() cancelled.")
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


def load_grub_params(project, initcpio=False):
    image_dir = project.image_dir()
    ver = [ver for ver in project.title.split(" ") if len(ver.split(".")) > 1]
    grub_dir = "/grub/themes/pisilinux/"
    dir_ = "%s/usr/share" %image_dir + grub_dir
    pf2s = glob.glob1(dir_, "*.pf2")
    loadfonts = ["loadfont ($root)/boot" + grub_dir + f for f in pf2s ]
    loadfonts = "\n".join(loadfonts)

    grb=""
    try:
        dosya = open("%s/grub.cfg" % image_dir)
        grb = dosya.read()
    except:
        print("dosya okunurken hata oluştu")
        return False
    finally:
        dosya.close()

    try:
        if initcpio:
            initcpio = 'options misobasedir=pisi misolabel=pisilive overlay=free'
        else:
            initcpio = ''

        if len(ver) > 0:
            ver = ver[0]
        else:
            ver = "0.0"
        dosya = open("%s/grub.cfg" % image_dir, "w")
        dosya.write(grb % {'fonts': loadfonts,
        'initcpio': initcpio, 'version': ver})
    except:
        print("dosya yazma işleminde hata oluştu")
        return False
    finally:
        dosya.close()

def make_EFI(project, grub=True):

    work_dir = os.path.join(project.work_dir)
    img_dir = os.path.join(project.work_dir)
    # configdir = "./config"  # os.path.join(project.config_files)
    iso_dir = project.iso_dir()
    efi_tmp = project.efi_tmp_path_dir(clean=True)
    image_dir = project.image_dir()

    efi_path = os.path.join(iso_dir, "EFI")

    if not os.path.exists(efi_path):
        os.makedirs(efi_path)
        os.makedirs(os.path.join(efi_path, "boot"))

    run("rm -rf %s/efi.img" % work_dir)

    # grub ####################################################################
    if grub:
        def chrun(cmd):
            run('chroot "%s" %s' % (image_dir, cmd))

        run("cp data/mkgrubx64.sh %s/" % image_dir)
        run("cp data/grub.cfg.template %s/grub.cfg" % image_dir)

        if 'mkinitcpio' in project.all_install_image_packages:
            load_grub_params(project, True)
        else:
            load_grub_params(project)

        chrun("/mkgrubx64.sh -e /grubx64.efi")

        run("rm %s/mkgrubx64.sh" % image_dir)
        run("rm %s/grub.cfg" % image_dir)
    # grub ####################################################################

    run("dd if=/dev/zero bs=1M count=40 of=%s/efi.img" % work_dir)
    run("mkfs.vfat -n PisiLinux %s/efi.img" % work_dir)
    run("mount %s/efi.img %s" % (work_dir, efi_tmp))

    os.makedirs(os.path.join(efi_tmp, "EFI/boot"))
    # os.makedirs(os.path.join(efi_tmp, "boot/efi/"))

    # grub ####################################################################
    if grub:
        run("cp -rf %s/EFI %s/" % ("./data/efi_grub", efi_tmp),
            ignore_error=True)
        run("cp -rf %s/EFI %s/" % ("./data/efi_grub", iso_dir),
            ignore_error=True)
        run("cp %s/grubx64.efi %s/EFI/boot/bootx64.efi" % (image_dir, iso_dir),
            ignore_error=True)
        run("cp %s/grubx64.efi %s/EFI/boot/bootx64.efi" % (image_dir, efi_tmp),
            ignore_error=True)

        # run("cp %s/tr.gkb %s/EFI/boot/" % (image_dir, iso_dir),
        #   ignore_error=True)
        # run("cp %s/en.gkb %s/EFI/boot/" % (image_dir, iso_dir),
        #   ignore_error=True)

        run("rm %s/grubx64.efi" % image_dir)
        run("rm %s/EFI/boot/loader.efi" % iso_dir)
        # run("rm %s/EFI/boot/loader.efi" % efi_tmp)
        # grub ################################################################
    else:
        run("cp -r %s/EFI %s/" % (iso_dir, efi_tmp), ignore_error=True)
        run("cp -r %s/loader %s/" % (iso_dir, efi_tmp), ignore_error=True)

    run("umount %s" % efi_tmp, ignore_error=True)
    run("umount -l %s" % efi_tmp, ignore_error=True)


def make_iso(project, toUSB=False, dev="/dev/sdc1"):
    print("Preparing ISO...")
    xterm_title("Preparing ISO")

    sort_cd_layout = False

    try:
        iso_dir = project.iso_dir(clean=True)
        iso_file = project.iso_file(clean=True)
        work_dir = project.work_dir
        image_dir = project.image_dir()
        image_file = project.image_file()
        image_path = os.path.join(iso_dir, "pisi")

        if not os.path.exists(image_path):
            os.makedirs(image_path)
        print(image_file)
        os.link(image_file, os.path.join(iso_dir, "pisi/pisi.sqfs"))

        def copy(src, dest):
            dest = os.path.join(iso_dir, dest)

            if os.path.isdir(src):
                shutil.copytree(
                    src, dest, ignore=shutil.ignore_patterns(".svn"))
            else:
                shutil.copy2(src, dest)

        if project.release_files:
            # Allow ~ usage in project xml files
            path = os.path.expanduser(project.release_files)
            for name in os.listdir(path):
                if name != ".svn":
                    copy(os.path.join(path, name), name)

        rep = project.get_repo()

        def version(package, rep=rep):
            if package in rep.packages.keys():
                return rep.packages[package].version
            else:
                return "{%s}" % package

        try:
            print("release files formatting...")
            # set version to release templates
            release_ver = ""
            with open(os.path.join(image_dir, "etc/pisilinux-release")) as rel:
                release_ver = rel.read().split()[-1]

            path = os.path.join(iso_dir, "index.html")
            index_text = ""
            with open(path) as index:
                index_text = index.read()

            with open(path, "w") as index:
                index.write(index_text.replace("@release@", release_ver))

            import re
            path = os.path.join(iso_dir, "release-notes")
            for name in os.listdir(path):
                print("file formatting: {}".format(name))
                rel_text = ""
                with open(os.path.join(path, name), "r") as rel:
                    rel_text = rel.read()
                    res = re.findall(".*(\{.+\}).*", rel_text)

                    if len(res) == 0:
                        continue

                    fmt = {}
                    for t in res:
                        package = t[1:-1]
                        if package == "release":
                            fmt[package] = release_ver
                        else:
                            fmt[package] = version(package)

                rel_text = rel_text.format(**fmt)

                with open(os.path.join(path, name), "w") as rel:
                    rel.write(rel_text)

            del rep
            del index_text
            del rel_text
        except Exception as e:
            print("Paketlerin sürüm bilgisi işlenirken hata oluştu. Hata:", e)
        # setup_grub(project)
        setup_isolinux(project)
        setup_efi(project)
        make_EFI(project)
        copy("./data/.miso", "")
        run("cp -p %s/efi.img %s/." % (work_dir, iso_dir))
        run("mkdir %s/boot" % iso_dir)
        run("ln -s %(iso)s/pisi/pisi.sqfs %(iso)s/boot/pisi.sqfs" % {'iso': iso_dir})

        # INFO:
        # sqfs kurulum yapan yali için kaldırıldı

        # if project.type == "install":
        # if "Calamares" in project.all_packages:
        #     run("rm -rf %s/license" % iso_dir, ignore_error=True)
        #     run("rm -rf %s/release-notes" % iso_dir, ignore_error=True)
        # else:
        #     run('ln -s "%s" "%s"' % (
        #         project.install_repo_dir(), os.path.join(iso_dir, "repo")))

        publisher = "Pisi GNU/Linux http://www.pisilinux.org"
        application = "Pisi GNU/Linux Live Media"
        label = "PisiLive"

        the_sorted_iso_command = 'genisoimage -f -sort %s/repo/install.order \
        -J -r -l -V "%s" -o "%s" -b isolinux/isolinux.bin \
        -c isolinux/boot.cat -boot-info-table \
        -uid 0 -gid 0 -udf -allow-limited-size -iso-level 3 \
        -input-charset utf-8 -no-emul-boot -boot-load-size 4 \
        -eltorito-alt-boot -e EFI/pisi/initrd.img -no-emul-boot \
        -publisher "%s" -A "%s"  %s' % (
            iso_dir, label, iso_file, publisher, application, iso_dir)

        # the_iso_command = 'genisoimage -f -J -r -l -V "%s" -o "%s" \
        # -b isolinux/isolinux.bin -c isolinux/boot.cat \
        # -boot-info-table -uid 0 -gid 0 -allow-limited-size -iso-level 3 \
        # -input-charset utf-8 -no-emul-boot -boot-load-size 4 \
        # -eltorito-alt-boot -e efi.img -no-emul-boot \
        # -publisher "%s" -A "%s"  %s' % (label, iso_file, publisher,
        #   application, iso_dir)

        the_iso_command = 'xorriso -as mkisofs \
        -f  -V "%s"\
        -o "%s" \
        -isohybrid-mbr /usr/lib/syslinux/bios/isohdpfx.bin \
        -c isolinux/boot.cat \
        -b isolinux/isolinux.bin \
        -no-emul-boot -boot-load-size 4 -boot-info-table \
        -eltorito-alt-boot \
        -e efi.img \
        -no-emul-boot \
        -isohybrid-gpt-basdat \
        -publisher "%s" -A "%s"  %s' % (
            label, iso_file, publisher, application, iso_dir)

        # Generate sort_list for mkisofs and YALI
        # Disabled for now
        if sort_cd_layout:
            sorted_list = generate_sort_list(iso_dir)
            if sorted_list:
                open("%s/repo/install.order" % iso_dir, "w").write(
                    "\n".join(["%s %d" % (k, v) for (k, v) in sorted_list]))
                run(the_sorted_iso_command)
        else:
            run(the_iso_command)
        # convert iso to a hybrid one
        # run("isohybrid --uefi %s" % iso_file)
        # run("isohybrid %s -b %s" % (
        #   iso_file, "%s/usr/lib/syslinux/bios/isohdpfx.bin" % image_dir))

        with open(
                os.path.join(project.work_dir, "finished.txt"), 'w') as _file:
            _file.write("make-iso")
    except KeyboardInterrupt:
        print("Keyboard Interrupt: make_iso() cancelled.")
        sys.exit(1)
