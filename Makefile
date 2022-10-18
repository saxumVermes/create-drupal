.PHONY: install

install:
	rm -f /usr/local/bin/drupal
	ln -s $$PWD/drupal /usr/local/bin/drupal