BTKNM (BlueTooth Keyboard aNd Mouse)
====================================

Expose local keyboard and mouse as 
Bluetooth HID device.

Requirements
------------

Bluez 5.x
Python 3.6+
dbus-python
python-evdev

Setup
-----

(for Arch Linux)

### Install Packages

```
$ sudo pacman -S bluez bluez-utils python python-dbus python-evdev
```

### Configure Bluez

```
$ sudo systemctl edit bluetooth.service
...
$ cat /etc/systemd/system/bluetooth.service.d/override.conf
[Service]
ExecStart=
ExecStart=/usr/lib/bluetooth/bluetoothd -p time
ExecStartPost=/usr/bin/btmgmt power on
$ sudo systemctl enable --now bluetooth.service
```

### Running program

```
$ sudo ./btk.py

```

### Pairing

```
$ bluetoothctl
...
[bluetooth]# power on
Changing power on succeeded
[CHG] Controller XX:XX:XX:XX:XX:XX Powered: yes
[bluetooth]# scan on
Discoverty started
[CHG] Controller XX:XX:XX:XX:XX:XX Discovering: yes
[bluetooth]# trust ZZ:ZZ:ZZ:ZZ:ZZ:ZZ
[CHG] Device ZZ:ZZ:ZZ:ZZ:ZZ:ZZ Trusted: yes
Changing ZZ:ZZ:ZZ:ZZ:ZZ:ZZ trust succeeded
[bluetooth]# pair ZZ:ZZ:ZZ:ZZ:ZZ:ZZ
...
[agent] Confirm passkey 123123 (yes/no): yes
...
```
