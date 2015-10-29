# Dr. Bob

## Problem

There are elections at the moment for the representative of the students and the winner will be announced tomorrow by the head of elections Dr. Bob. The local schoolyard gang is gambling on the winner and you could really use that extra cash. Luckily, you are able to hack into the mainframe of the school and get a copy of the virtual machine that is used by Dr. Bob to store the results. The desired information is in the file /home/bob/flag.txt, easy as that.

[mega.nz mirror](https://mega.nz/#!qoUDxYrB!W-C6vZxiulkaZ9ONWbyohCpAOfRbLtvHIgIICvjeZWk) (598.6 MB)

## Solution

Credit: [@emedvedev](https://github.com/emedvedev), [@gellin](https://github.com/gellin), [@johndearman](https://github.com/johndearman)

Firstly, let's examine the archive we're given:

```
./home
./home/dr_bob
./home/dr_bob/.VirtualBox
./home/dr_bob/.VirtualBox/compreg.dat
./home/dr_bob/.VirtualBox/Machines
./home/dr_bob/.VirtualBox/Machines/Safe
./home/dr_bob/.VirtualBox/Machines/Safe/Logs
./home/dr_bob/.VirtualBox/Machines/Safe/Logs/VBox.log
./home/dr_bob/.VirtualBox/Machines/Safe/Logs/VBox.log.1
./home/dr_bob/.VirtualBox/Machines/Safe/Logs/VBox.log.2
./home/dr_bob/.VirtualBox/Machines/Safe/Safe.vbox
./home/dr_bob/.VirtualBox/Machines/Safe/Safe.vbox-prev
./home/dr_bob/.VirtualBox/Machines/Safe/Safe.vdi
./home/dr_bob/.VirtualBox/Machines/Safe/Snapshots
./home/dr_bob/.VirtualBox/Machines/Safe/Snapshots/2015-09-26T13-33-10-508528000Z.sav
./home/dr_bob/.VirtualBox/selectorwindow.log
./home/dr_bob/.VirtualBox/selectorwindow.log.1
./home/dr_bob/.VirtualBox/VBoxSVC.log
./home/dr_bob/.VirtualBox/VBoxSVC.log.1
./home/dr_bob/.VirtualBox/VBoxSVC.log.2
./home/dr_bob/.VirtualBox/VBoxSVC.log.3
./home/dr_bob/.VirtualBox/VBoxSVC.log.4
./home/dr_bob/.VirtualBox/VirtualBox.xml
./home/dr_bob/.VirtualBox/VirtualBox.xml-prev
./home/dr_bob/.VirtualBox/xpti.dat
```

There's a `.VirtualBox` dir containing not just the box image, but config files and a snapshot along with it. Given you already have VirtualBox installed, move `Machines/Safe` to your VirtualBox dir. Restore the snapshot:

![](login.png?raw=true)

Login prompt with seemingly no way around it. Let's reboot the machine:

![](passphrase.png?raw=true)

Now the nature of the challenge becomes more clear: we have a [LUKS](https://en.wikipedia.org/wiki/Linux_Unified_Key_Setup)-encrypted hard drive with no knowledge of the passphrase or a login prompt with the drive already mounted but no knowledge of the password.

PLOT TWIST! There are actually two ways to solve this challenge, and we'll explore both.

### Logging in

Let's think about the login prompt: since it's a virtual machine, we have complete control over the unencrypted files, and from the previous steps we can see that only `/home` is encrypted. One of these files we have complete control over? `/etc/shadow`.

That's what a typical `/etc/shadow` entry containing a password hash looks like:

```
smithj:Ep6mckrOLChF.:10063:0:99999:7:::
```

Let's look for strings formatted like this inside our `.vdi` drive image, find out what the password hash for `root` is and replace it with our own hash of a known password. It can be done with a hex editor which is comfortable with lookups inside a 1.78 GB disk image (I use _Synalyze It!_ on OS X), as well as your typical command-line tools. For the sake of brevity I'll use the latter:

Generating a hash for a known password:

```
$ mkpasswd -m sha-512 mynewpassword saltsalt
$6$saltsalt$ZzMhzEvGVJfYqywGstIsbfPRf7x0n1km8ZHJAmnFZ3juwus6rwrvnLbtcRCFsRd.gH8pbMZlTEtEHyOSNmOyT0
```

Searching for the root password to replace:

```
$ strings Safe.vdi | grep root: | grep :::
root:$6$pBOgEWfD$vKmHQo3cYURAjB50meHPQw1MvDBKBSuqLj53rPeLCc23l26L1YRuJTfu.KV1KDXb/1ekrvb4EBRZt.xuKRRER0:16699:0:99999:7:::
[...]
```

Replacing every occurrence of the root password hash with ours:

```
$ LANG=C sed -i -e 's/$6$pBOgEWfD$vKmHQo3cYURAjB50meHPQw1MvDBKBSuqLj53rPeLCc23l26L1YRuJTfu\.KV1KDXb\/1ekrvb4EBRZt\.xuKRRER0/$6$saltsalt$ZzMhzEvGVJfYqywGstIsbfPRf7x0n1km8ZHJAmnFZ3juwus6rwrvnLbtcRCFsRd.gH8pbMZlTEtEHyOSNmOyT0/g' Safe.vdi
```

All that's left is restoring the snapshot and logging in as `root:mynewpassword`. We're in!

![](in.png?raw=true)

### Breaking the encryption

The other way of recovering the flag is more complicated but also more exciting. Well, everything with "breaking" and "encryption" in a sentence is exciting _a priori_, but we'll also get to play with memory dumps, which is always fun.

This solution is based on the fact is that the drive is already decrypted in the snapshot, which means that the decryption key is stored somewhere in memory. We'll get a memdump with the VirtualBox management tool:

```
$ vboxmanage debugvm "Safe" dumpguestcore --filename safe.elf
```

The tool of choice for examining memory dumps is [Volatility](http://www.volatilityfoundation.org), and I encourage you to play with it and find out how much data you can actually salvage from a dump (spoiler alert: a variety of passwords and keys including `sshd` hostkeys, process list, open files and their content, and a lot more), but in this case we need something very specific: an AES key for LUKS encryption. We'll use [aeskeyfind](https://citp.princeton.edu/research/memory/code/):

```
$ ./aeskeyfind safe.elf
1fab015c1e3df9eac8728f65d3d16646
Keyfind progress: 100%
```

Simple as that. The key we've recovered is a master key: we can easily set a new passphrase with it. We'll reset the root password first: boot by appending `init=/bin/bash` to the Grub entry.

![](grub.png?raw=true)

Remove the root password from `/etc/shadow`, reboot, load the OS ignoring the encrypted drive passphrase prompt. Almost done: now we just need to write our master key to a file and use it to set a new passphrase.

```
# echo 1fab015c1e3df9eac8728f65d3d16646 | xxd -r -p > key
# cryptsetup luksAddKey --master-key-file key /dev/vg/home
Enter new passphrase for key slot:
Verify passphrase:
```

Issue another reboot and enter your new passphrase when prompted. That's it!

![](in2.png?raw=true)

### One more thing

One last tiny part of the challenge: there's no flag when you `cat` the file.

![](noflag.png?raw=true)

Don't worry: it's just hidden with a carriage return char. Open the file in a text editor and you're good. :)

![](flag.png?raw=true)

Solved! 10/10, would analyze again.
