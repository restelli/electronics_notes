# SD cards in instrumentation

Using SD cards in lab instrumentation as boot drives for PSoC or embedded systems can be tricky since they are prone to fast wear off if not used properly. Here some notes I took while roubleshooting a faulty SD card from a red Pitaya board.

## lessons learned from sudded and frequent failure of SD cards

Yesterday we used the debug COM port of an unresponsive Red Pitaya to diagnose why it was not working and we found that the Linux kernel was going into a panic during booting. No wonder why the device was offline!
The cause of the kernel panic was that the SD card seemed to malfunction.
Our solution was to swap the SD card with another one, but I decided to investigate the faulty SD card to find out while it was broken.
I therefore mounted it on a Linux machine and found out that all the partitions were showing all the files.
While trying to run a check disk however I realized that the SD card was locked in read-only mode.
After a search online I found that when an SD card is at the end of life and it fails to write data it automatically locks up in order to preserve the user's precious data.

[Stack exchange blog about SD card failures in embedded systems](https://unix.stackexchange.com/questions/327863/fsck-wont-fsck-unable-to-set-superblock-flags)

One reason why the card could have failed prematurely is that the person that wrote the flash image on the card forgot to expand the ext4 partition from 3.5GB to the full 32GB of space available on the card. This can be done with GParted or, alternatively, and more easily by using command line tools available in the Red pitaya itself.
Instructions on how to do that are here:

[How to resize Red Pitaya SD cards: very impoartant!](https://redpitaya.readthedocs.io/en/latest/quickStart/SDcard/SDcard.html#resize-file-system)

And it all boils down to running the command /opt/redpitaya/sbin/resize.sh

I think that the main issue affecting your SD cards is that the expansion of the partition has not been done in your SD cards, therefore you should go ahead and run the command /opt/redpitaya/sbin/resize.sh in all your Red Pitayas.

One important take about the use of SD cards in lab equipment is that you should treat them as a consumable that after a few years of usage need to be replaced, therefore backing them up and having replacement at hand is a good thing to have.

Furthermore, there are lot of ways to increase the longevity of those cards.

1) Extend the partition size. I'm not sure if that affects the overprovisioning algorithm in the SD cards but it seems to me the right thing to do. Looking at forums it looks like that SD cards do not have very smart wear-leveling algorithms so limiting the size of a partition is likely forcing the OS to keep writing on the same space of the SD card quickly destroying it.
2) Buy large SD cards (and extend the partition) so that there it will take much more time to wear off the FLASH memory. 
3) Use additional tricks shown in the following thread:

[Raspberry Pi forum abou extending lifetime of SD cards](https://forums.raspberrypi.com/viewtopic.php?t=327484)

In particular I believe that creating a RAM disk for the logs and forcing the OS to keep files for a few minutes in cache before writing them on the card should enormously extend the lifetime of the SD card. It is as simple as editing the /etc/fstab file and reboot.

Finally, it is often possibile to extract data from a bricked SD card but one must be aware that files might be flagged as non readable therefore commands like `sudo chmod -R +r <your folder>` might be needed before compressing a folder copyed from the SD card.

