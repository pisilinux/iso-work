#!/bin/sh

efi_path="efi/EFI/boot/grubx64.efi"
theme="pisilinux"

usage (){
  echo "Usage:"
  echo "  -t: theme name"
  echo "  -e: efi path"
}

while getopts ":t:e:" opt; do
  case $opt in
    t)
      theme=$OPTARG
      ;;
    e)
      efi_path=$OPTARG
      ;;
    \?)
      usage
      exit 0
      ;;
    *)
      echo "Invalid Opriton" >&2
      usage
      exit 1
      ;;
  esac
done

# grub2-kbdcomp -o tr.gkb tr
# grub2-kbdcomp -o en.gkb en

# grub2-mkstandalone --locale-directory=/boot/grub2/locale/ -d /usr/lib/grub/x86_64-efi/ -O x86_64-efi --themes="pisi" -o $efi_path "boot/grub/grub.cfg=./grub.cfg" -v
# grub2-mkstandalone -d /usr/lib/grub/x86_64-efi/ -O x86_64-efi --fonts="/boot/grub2/fonts/unicode.pf2" --locale-directory=/usr/share/locale/ --themes=$theme -o $efi_path "boot/grub/grub.cfg=./grub.cfg" -v
  grub2-mkstandalone -d /usr/lib/grub/x86_64-efi/ -O x86_64-efi --fonts="/boot/grub2/fonts/unicode.pf2" --themes=$theme -o $efi_path "boot/grub/grub.cfg=./grub.cfg" -v
