# Perl Golf

## Problem

Johnny B. Krad from your local schoolyard gang thinks that you are a poser! The stuff you solved until now was just luck. He bets that you are not able to beat him in Perl golf.

[Link](https://school.fluxfingers.net:1521/golf/perl/)

## Solution

Credit: [@emedvedev](https://github.com/emedvedev)

The link contains our golf challenge:

> Write a Perl program that takes a parameter as input and outputs a filtered version with alternating upper/lower case letters of the (english) alphabet. Non-letter characters have to be printed but otherwise ignored.
>
> - You have 1 second.
> - You have 45 (ASCII) chars.
> - Do not flood the server.
>
> ```
> Input   Hello World! Hallo Welt!
> Output  HeLlO wOrLd! HaLlO wElT!
> ```

Let's start by looking at the parts we can't get rid of. The obvious way to solve it in Perl is a regular expression substitution:

- `@ARGV[0]` (8 chars): for reading input
- `print` (5 chars): to writing output
- `=~s/*/*/r*` (7 chars): shortest regex replacement syntax I can think of

Now our code looks like this (and apparently can be reduced even further, but I'm not a codegolf pro:

```
print@ARGV[0]=~s/<expr>/<replace>/r<modifiers>
```

We have 25 chars left for the expression, replacement code and modifiers. Perl can evaluate the replacement side as an expression with a modifier `e`, so let's use that: we'll match every letter with `\pL` (which is an alias for `\p{Letter}`), increment a switcher variable and alternate uppercase/lowercase with `%2` to get a working solution:

```
print@ARGV[0]=~s/(\pL)/++$c%2?uc$1:lc$1/ger
```

43 chars! Here's an explanation:

```
print@ARGV[0]=~s/(\pL)/++$c%2?uc$1:lc$1/ger

print@ARGV[0]=~s/     /                /    # print the input pattern-replaced by an expression
                 (\pL)                      # match every letter
                       ++$c                 # increment a counter
                           %2?              # if the counter is even
                              uc$1          # convert our match to upper case
                                  :         # else
                                   lc$1     # convert the match to lower case
                                        g   # match globally
                                         e  # evaluate right part as an expression
                                          r # return the value instead of storing it
```

That's already enough to get the flag, but some teams took it even further, with the shortest solution I've seen being 34 chars long. Let's try to shorten our solution further by using some Perl trickery I wasn't aware of when originally solving the challenge:

- use ` pop` instead of `@ARGV[0]` (saving 4 chars)
- use `$&` to get the whole regex match and getting rid of parentheses (saving 2 chars)

We get 37 chars:

```
print pop=~s/\pL/++$c%2?uc$&:lc$&/ger
```

We can also make use of the fact that XOR 32 changes case in ASCII. Now, instead of incrementing the counter, we'll XOR it by 32 (`$"` is a Perl alias for space which is, in turn, ASCII 32), and then XOR it with the match converted to lowercase. 35 chars:

```
print pop=~s/\pL/$c^=$";lc$&^$c/ger
```

We just pulled a Tiger Woods right there. Now let's get it down to 34 chars: we'll define and use our counter in the same expression:

```
print pop=~s/\pL/($c^=$")^lc$&/ger
```

Congratulations!
