# pseud

Notes:

1. Using QEMU on windows to emulate RPi
  a. qemu-system-arm -kernel kernel-qemu-4.4.13-jessie -cpu arm1176 -m 256 -M versatilepb -serial stdio -append "root=/dev/sda2 panic=1 rootfstype=ext4 rw" -drive "file=2018-11-13-raspbian-stretch.img" -net user,hostfwd=tcp::10022-:22 -net nic
2. Installed needed python3 libraries: ($ pip3 install selenium bs4)
3. Identify path to chromedriver (install if necessary: https://www.raspberrypi.org/forums/viewtopic.php?t=194176)
