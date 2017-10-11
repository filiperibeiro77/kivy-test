NAME=kivy-camera
VERSION=0.1

DIRS=etc lib bin sbin share
INSTALL_DIRS=`find $(DIRS) -type d 2>/dev/null`
INSTALL_FILES=`find $(DIRS) -type f 2>/dev/null`
DOC_FILES=*.md *.txt

SHARE_DIR=$(PREFIX)/share/$(NAME)

PKG_DIR=pkg
PKG_NAME=$(NAME)-$(VERSION)
PKG=$(PKG_DIR)/$(PKG_NAME).tar.gz
SIG=$(PKG_DIR)/$(PKG_NAME).asc

PREFIX?=/usr/local
DOC_DIR=$(PREFIX)/share/doc/$(PKG_NAME)

pkg:
	mkdir -p $(PKG_DIR)

$(PKG): pkg
	git archive --output=$(PKG) --prefix=$(PKG_NAME)/ HEAD

build: $(PKG)

$(SIG): $(PKG)
	gpg --sign --detach-sign --armor $(PKG)

sign: $(SIG)

clean:
	rm -f $(PKG) $(SIG)

all: $(PKG) $(SIG)

test:

tag:
	git tag v$(VERSION)
	git push --tags

release: $(PKG) $(SIG) tag

install:
	mkdir -p $(SHARE_DIR)
	cp main.py camera.png camera.kv wrapper.py $(SHARE_DIR)
	chmod 755 $(SHARE_DIR)/wrapper.py
	ln -fs $(SHARE_DIR)/wrapper.py $(PREFIX)/bin/$(NAME)

uninstall:
	rm -R $(SHARE_DIR)
	rm $(PREFIX)/bin/$(NAME)

.PHONY: build sign clean test tag release install uninstall all
