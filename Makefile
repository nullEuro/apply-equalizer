NAME = apply-equalizer
PREFIX = /usr/share/$(NAME)
SCRIPT = $(NAME).py
STARTER = $(NAME).desktop
AUTOSTART_DIR = /etc/xdg/autostart

install:
	mkdir -p $(PREFIX)
	cp -u $(SCRIPT) $(PREFIX)
	cp -u $(STARTER) $(AUTOSTART_DIR)
	cp -u --preserve=mode $(NAME) /usr/bin
	
clean:
	rm $(PREFIX)/$(SCRIPT)
	rmdir $(PREFIX)
	rm $(AUTOSTART_DIR)/$(STARTER)
	rm /usr/bin/$(NAME)
