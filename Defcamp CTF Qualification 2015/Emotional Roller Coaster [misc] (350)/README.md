# Emotional Roller Coaster (Misc 350)

## Problem

Are you a good listener? Expect us!

_This time you're the target. :-)_

## Solution

Credit: [@emedvedev](https://github.com/emedvedev)

It's a great forensics challenge and also a lot of fun. Although not particuarly hard, it's very creative and nicely layered. ![](emotions/hiro.gif?raw=true) Let's begin!

![](emotions/goodluck.gif?raw=true)

#### 1. The query

"A good listener" and "this time you're the target" in the description, along with the fact that nothing else is given, points us in the direction of traffic capture: somebody will probably try to attack your machine or send requests to it. ![](emotions/idea.gif?raw=true) DCTF has a VPN network for challenges, so it's safe to assume that this one will involve our VPN connection. Let's fire up Wireshark, capture all VPN traffic and see whatever it is we're the "target" of. ![](emotions/nerd.gif?raw=true)

![](wireshark1.png?raw=true)

Here it is. We really are good listeners, aren't we? ![](emotions/donttellanyone.gif?raw=true)

#### 2. The response

The request is an MX (mail) query to a DNS server: it asks our machine to resolve `dctfu2126.1337.def`. Let's fire up a DNS server and actually resolve the query; DNSmasq does this job quite well and it's incredibly easy to set up. ![](emotions/dancing.gif?raw=true)

```
$ dnsmasq --address=/dctfu2126.1337.def/10.20.8.95 --mx-host=dctfu2126.1337.def --mx-target=10.20.8.95
```

That's it, now your machine is a DNS server. ![](emotions/cool.gif?raw=true)

#### 3. The message

Let's see what happens after we send the response:

![](wireshark2.png?raw=true)

Logically enough, since we answered that our machine is a mail server, we're seeing an SMTP request to port 25 now. Let's fire up a catch-all SMTP server, and capture whatever the message is. ![](emotions/bringiton.gif?raw=true) I'm using `MockSMTP` on OS X (you have to start it with `sudo` to make it listen on port 25), but if you're running another OS, I bet you can find a lot of software if you just google "mock SMTP" or "catch-all SMTP". Here we go:

![](mocksmtp1.png?raw=true)

"Almost there," they said. Don't trust the guys. ![](emotions/angry.gif?raw=true)

#### 4. The attachment

Attached to the e-mail is a packet capture file, [ftps.pcap](ftps.pcap). Let's fire up Wireshark again:

![](wireshark3.png?raw=true)

Is it a bird? Is it a plane? It's an SMB session! ![](emotions/biggrin.gif?raw=true) We'll use Wireshark's convenient SMB object extraction to see what's in there:

![](wireshark4.png?raw=true)

Now we have an archive, [emotions.zip](emotions.zip). Is the flag there? Well, not quite yet. ![](emotions/idontknow.gif?raw=true)

#### 5. The emotions

We have 96 amazing animated emoticons in the archive, which is a reward good enough by itself, of course, because emoticons are just like glitter: they're awesome and everybody loves them. I even took the liberty of sprinkling some across this whole write-up ![](emotions/blushing.gif?raw=true), as you might have noticed (or not—I was being very subtle).

There's a `flag.gif` in the archive, so let's take a look:

![](emotions/flag.gif?raw=true)

Aside from being awesome, the image is completely uneventful. Opening it in hex editor doesn't show much except it's an ordinary gif (duh ![](emotions/straightface.gif?raw=true)) with metadata `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`.

This metadata bit looks interesting, so we'll take a look at other files, too. Let's use `exiftool` on some random emoticons:

```
$ exiftool thumbsdown.gif
ExifTool Version Number         : 10.00
File Name                       : thumbsdown.gif
Directory                       : .
File Size                       : 6.9 kB
File Modification Date/Time     : 2015:10:03 03:11:14+06:00
File Access Date/Time           : 2015:10:04 15:27:04+06:00
File Inode Change Date/Time     : 2015:10:04 06:00:23+06:00
File Permissions                : rwxrwxrwx
File Type                       : GIF
File Type Extension             : gif
MIME Type                       : image/gif
GIF Version                     : 89a
Image Width                     : 28
Image Height                    : 18
Has Color Map                   : Yes
Color Resolution Depth          : 6
Bits Per Pixel                  : 6
Background Color                : 63
Animation Iterations            : Infinite
XMP Toolkit                     : Image::ExifTool 9.46
Camera Model Name               : zyy7mY2/Rx1LP5jYtGa3G2j8y9mM7w9i3eGf012vsdc3fcyqRr9w+8ZyGds4uMwAA
Frame Count                     : 20
Duration                        : 4.95 s
Image Size                      : 28x18
Megapixels                      : 0.000504
```

Notice the "Camera Model Name" field: if you're reading this, chances are you know Base64 when you see it. ![](emotions/raisedeyebrow.gif?raw=true)

#### 6. The flag

Decode a few Base64 messages, and you'll see they all appear to be parts of some binary file. ![](emotions/thinking.gif?raw=true) Let's just concat all the emoticons into one big file and see what happens:

```
$ exiftool *.gif | grep Camera | cut -c 35- > misc350.base
$ cat misc350.base | base64 -D > misc350.bin
```

![](hex1.png?raw=true)

We're definitely on the right track with this: notice the `PK..` (`50 4B 01 02`): it's a clear indicator of a ZIP archive. However, the order in which we concatenated Base64 strings (it's the filename by default) is clearly wrong beause the file is scrambled. Hmmm, what might be the correct sorting method? ![](emotions/silly.gif?raw=true)

Let's take a look at our decoded `misc350.base`: one line clearly stands out. Meet Billy:

![](emotions/billy.gif?raw=true)

Unlike all his emoticon friends with 65-byte Base64-encoded strings in their metadata, Billy only has 29 bytes (don't worry, Billy, size doesn't matter ![](emotions/heehee.gif?raw=true)), so this truncated string should be in the end of our file. Let's sort files and look for the sorting method where Billy comes last. ![](emotions/winking.gif?raw=true)

After some trial-and-error the method turns out to be modification date: do `ls -tlr` and you'll see that `billy.gif` is the last one on the list. Now let's recreate the archive:

```
$ exiftool `ls -tr` | grep Camera | cut -c 35- | base64 -D > misc350.zip
```

And here's the flag, waiting patiently for you in `sol/flag`, wanting so desperately to be found:

```
DCTF{e4045481e906132b24c173c5ee52cd1e}
```

Congratulations! It was a great run.

![](emotions/alien.gif?raw=true)
![](emotions/angel.gif?raw=true)
![](emotions/angry.gif?raw=true)
![](emotions/applause.gif?raw=true)
![](emotions/april.gif?raw=true)
![](emotions/atwitsend.gif?raw=true)
![](emotions/battingeyelashes.gif?raw=true)
![](emotions/bee.gif?raw=true)
![](emotions/biggrin.gif?raw=true)
![](emotions/bighug.gif?raw=true)
![](emotions/billy.gif?raw=true)
![](emotions/blushing.gif?raw=true)
![](emotions/bringiton.gif?raw=true)
![](emotions/brokenheart.gif?raw=true)
![](emotions/bug.gif?raw=true)
![](emotions/callme.gif?raw=true)
![](emotions/chatterbox.gif?raw=true)
![](emotions/chicken.gif?raw=true)
![](emotions/clown.gif?raw=true)
![](emotions/coffee.gif?raw=true)
![](emotions/confused.gif?raw=true)
![](emotions/cool.gif?raw=true)
![](emotions/cow.gif?raw=true)
![](emotions/cowboy.gif?raw=true)
![](emotions/cry.gif?raw=true)
![](emotions/dancing.gif?raw=true)
![](emotions/daydreaming.gif?raw=true)
![](emotions/devil.gif?raw=true)
![](emotions/doh.gif?raw=true)
![](emotions/donttellanyone.gif?raw=true)
![](emotions/drooling.gif?raw=true)
![](emotions/feelingbeatup.gif?raw=true)
![](emotions/flag.gif?raw=true)
![](emotions/frustrated.gif?raw=true)
![](emotions/goodluck.gif?raw=true)
![](emotions/happy.gif?raw=true)
![](emotions/heehee.gif?raw=true)
![](emotions/hiro.gif?raw=true)
![](emotions/hurryup.gif?raw=true)
![](emotions/hypnotized.gif?raw=true)
![](emotions/idea.gif?raw=true)
![](emotions/idontknow.gif?raw=true)
![](emotions/kiss.gif?raw=true)
![](emotions/laughing.gif?raw=true)
![](emotions/liar.gif?raw=true)
![](emotions/loser.gif?raw=true)
![](emotions/lovestruck.gif?raw=true)
![](emotions/moneyeyes.gif?raw=true)
![](emotions/monkey.gif?raw=true)
![](emotions/nailbiting.gif?raw=true)
![](emotions/nerd.gif?raw=true)
![](emotions/notlistening.gif?raw=true)
![](emotions/nottalking.gif?raw=true)
![](emotions/notworthy.gif?raw=true)
![](emotions/noxxx.gif?raw=true)
![](emotions/ohgoon.gif?raw=true)
![](emotions/onthephone.gif?raw=true)
![](emotions/party.gif?raw=true)
![](emotions/peacesign.gif?raw=true)
![](emotions/phbbbbt.gif?raw=true)
![](emotions/pig.gif?raw=true)
![](emotions/praying.gif?raw=true)
![](emotions/pumpkin.gif?raw=true)
![](emotions/puppydogeyes.gif?raw=true)
![](emotions/raisedeyebrow.gif?raw=true)
![](emotions/rockon.gif?raw=true)
![](emotions/rollingeyes.gif?raw=true)
![](emotions/rollingonthefloor.gif?raw=true)
![](emotions/rose.gif?raw=true)
![](emotions/sad.gif?raw=true)
![](emotions/shameonyou.gif?raw=true)
![](emotions/sick.gif?raw=true)
![](emotions/sigh.gif?raw=true)
![](emotions/silly.gif?raw=true)
![](emotions/skull.gif?raw=true)
![](emotions/sleepy.gif?raw=true)
![](emotions/smug.gif?raw=true)
![](emotions/star.gif?raw=true)
![](emotions/straightface.gif?raw=true)
![](emotions/surprise.gif?raw=true)
![](emotions/talktothehand.gif?raw=true)
![](emotions/thinking.gif?raw=true)
![](emotions/thumbsdown.gif?raw=true)
![](emotions/thumbsup.gif?raw=true)
![](emotions/timeout.gif?raw=true)
![](emotions/tongue.gif?raw=true)
![](emotions/waiting.gif?raw=true)
![](emotions/wasntme.gif?raw=true)
![](emotions/wave.gif?raw=true)
![](emotions/whew.gif?raw=true)
![](emotions/whistling.gif?raw=true)
![](emotions/whistling2.gif?raw=true)
![](emotions/winking.gif?raw=true)
![](emotions/worried.gif?raw=true)
![](emotions/yawn.gif?raw=true)
![](emotions/yinyang.gif?raw=true)
