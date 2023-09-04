# domotica_config

Remember in setup
	sudo -s
	cp config.txt /boot
	cp root.bashrc /root/.bashrc
	cp homeassistant.service --> /lib/systemd/system
	systemctl start homeassistant.service
	systemctl enable homeassistant.service
	cp jellyfin.service --> /lib/systemd/system
	systemctl start jellyfin.service
	systemctl enable jellyfin.service
	cp shairport-sync.service --> /lib/systemd/system
	cp shairport-sync.service --> /lib/systemd/system
	systemctl start shairport-sync.service
	systemctl enable shairport-sync.service

remember in homeassistant:

	ln -s casa.storage .storage
	ln -s case.config active

	ln -s piso.storage .storage
	ln -s piso.config active
	
