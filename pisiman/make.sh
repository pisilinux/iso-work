#!/bin/sh

function make {
  if [ $# -eq 0 ]; then
    echo "Ui dosyaları python koduna dönüştürülüyor..."
    py2uic5 -o gui/ui/main.py gui/ui/main.ui
    py2uic5 -o gui/ui/mainv2.py gui/ui/mainv2.ui
    py2uic5 -o gui/ui/languages.py gui/ui/rawlanguages.ui
    py2uic5 -o gui/ui/packages.py gui/ui/packages.ui
    py2uic5 -o gui/ui/packagecollection.py gui/ui/packagecollection.ui
    py2rcc5 -o gui/ui/raw_rc.py gui/ui/raw.qrc

    # install required packages
    if [ -f required_packages.txt ]; then
      echo "gerekli paketler pisi ile kuruluyor..."
      sudo pisi it $(cat required_packages.txt)
    fi


  # elif [ [ $# -eq 1 ] && [ [ $1 == "clean" ] || [ $1 == "c" ] ] ]; then
  elif [[ ( $# -eq 1  && $1 == "clean" ) || ( $# -eq 1  && $1 == "c" ) ]]; then
    echo "temizleme işlemi başlatıldı"
    find .  -name *.pyc | xargs rm -rf
    rm -rf gui/ui/main.py
    rm -rf gui/ui/mainv2.py
    rm -rf gui/ui/languages.py
    rm -rf gui/ui/packages.py
    rm -rf gui/ui/packagecollection.py
    rm -rf gui/ui/raw_rc.py
    rm -f .firstRun
  else
    echo "Kullanım: "
    echo "    $0 [clean]"
    echo "    clean: oluşturulan dosyaları siler"
    exit 1
  fi

  echo "işlem tamamlandı."
}


if [ "${BASH_SOURCE[0]}" -ef "$0" ]
then
  if [ $# -eq 0 ]; then
    make
  else
    make $1
  fi
fi
