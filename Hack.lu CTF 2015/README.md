# PHP Golf

## Problem

Johnny B. Krad from your local schoolyard gang still thinks that you are a poser! Even if you could beat him in Perl golf, you probably can't in PHP golf...

[Link](https://school.fluxfingers.net:1521/golf/php/)

## Solution

Credit: [@emedvedev](https://github.com/emedvedev), @just.johnny

This is a sequel to the [Perl Golf](../Perl Golf [ppc] (75)/) challenge from the same CTF with considerably less solves. Let's open the link:

> Write a PHP program that takes a parameter as input and outputs a filtered version with alternating upper/lower case letters of the (english) alphabet. Non-letter characters have to be printed but otherwise ignored.
>
> - You have 1 second.
> - You have 62 (ASCII) chars.
> - Do not flood the server.
>
> ```
> Input   Hello World! Hallo Welt!
> Output  HeLlO wOrLd! HaLlO wElT!
> ```

A common approach to this challenge was piping the input through the previously obtained script from Perl Golf, which is hilarious. However, let's try a "clear" PHP-only approach.

We'll write a script similar to the Perl challenge: match every letter with a regex and iterate a counter, alternating uppercase and lowercase:

```
<?=preg_filter("/\pL/e","++\$i%2?ucfirst($0):lcfirst($0);",$argv[1]);
```

This script, mimicking our first Perl script, is working, but does not qualify: it's 69 characters long. Function names such as `preg_filter`, `ucfirst` and `lcfirst` are certainly not helping.

While we can't get rid of `preg_filter`, we can replace `ucfirst` and `lcfirst` with XOR:

```
<?=preg_filter("/\pL/e","++\$i%2?$0^" ":$0;",strtolower($argv[1]));
```

Still 67 characters, and we need 62. Can we do without the `strtolower` and the counter? Yes we can!

```
<?=preg_filter("/\pL/e",'lcfirst($0)^chr($u^=32)',$argv[1]);
```

60 chars long, the flag is ours! Can we make it even shorter though? I couldn't, but the "master" solution was very similar yet shorter by a few chars:

```
<?=preg_filter("/\pL/e",'($0|" ")^chr($u^=32)',$argv[1]);
```

Welcome to the world of dark PHP magic. You will never be the same again.
