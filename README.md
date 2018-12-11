# pseud

Notes:

1. Using QEMU on windows to emulate RPi
  a. qemu-system-arm -kernel kernel-qemu-4.4.13-jessie -cpu arm1176 -m 256 -M versatilepb -serial stdio -append "root=/dev/sda2 panic=1 rootfstype=ext4 rw" -drive "file=2018-11-13-raspbian-stretch.img" -net user,hostfwd=tcp::10022-:22 -net nic
  b. qemu-img.exe resize -f raw vm\2018-11-13-raspbian-stretch.img +2G
  c. $ sudo fdisk /dev/sda
     Print the partition table ("p"). Take note of the starting block of the main partition
     Delete the main partition ("d"). Should be partition 2.
     Create (n)ew partition. (P)rimary. Position (2)
     Start block should be the same as start block from the original partition
     Size should be the full size of the image file (just press "enter")
     Now write the partition table (w)
     Reboot (shutdown -r now).
     > sudo resize2fs /dev/sda2
2. Installed needed python3 libraries: ($ pip3 install selenium bs4)
3. Identify path to chromedriver (install if necessary: https://www.raspberrypi.org/forums/viewtopic.php?t=194176)
