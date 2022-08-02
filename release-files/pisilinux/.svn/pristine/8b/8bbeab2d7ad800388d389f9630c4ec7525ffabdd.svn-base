all:
	echo " ********************   Please make sure that python-beautifulsoup and publican are installed! **************** "; \
	publican build --formats=html-single --langs=all; \
	for lang_dir in tmp/*; do \
	    lang=$$(basename $$lang_dir); \
	    index=$$lang_dir/html-single/index.html; \
	    python remove-title.py $$index > ../media-content/release-notes/releasenotes-$${lang/-*/}.html; \
	done; \
	[ -d ../media-content/release-notes/Common_Content ] || mkdir -p ../media-content/release-notes/Common_Content; \
	rsync -avz --exclude=.svn tmp/en-US/html-single/Common_Content/ ../media-content/release-notes/Common_Content/

update-po:
	publican update_pot
	publican update_po --langs=all

clean:
	rm -rf tmp
