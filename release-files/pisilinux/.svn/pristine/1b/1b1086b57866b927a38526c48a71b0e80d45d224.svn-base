PM=${HOME}/pardusman/pardusman.py

all: install live

live: live64 live32

install: install64 install32

install64:
	${PM} make installation.xml

live64:
	${PM} make live.xml

install32:
	${PM} make installation-i686.xml

live32:
	${PM} make live-i686.xml

clean: clean32 clean64

clean32:
	rm -rf /tmp/pardusman-workdir/32

clean64:
	rm -rf /tmp/pardusman-workdir/64
