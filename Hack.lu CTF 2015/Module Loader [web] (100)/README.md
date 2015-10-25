# Module Loader

## Problem

Since his students never know what date it is and how much time they have until the next homework's deadline, Mr P. H. Porter wrote a little webapp for that.
You can find it [here](https://school.fluxfingers.net:1522).

## Solution

Credit: [@emedvedev](https://github.com/emedvedev)

The app contains a simple module list:

![](loader.png?raw=true)

Clicking on "date" sends us to `https://school.fluxfingers.net:1522/?module=date` and outputs `Today: 2015-10-25` on the screen. There's also a comment in the app:

```
<!-- Modules are located in the 'modules' folder. Ask Mr Porter if you need more. -->
```

`https://school.fluxfingers.net:1522/modules/` reveal an Apache directory listing, indicating that module names in the URL are just links to files in the `modules` dir:

![](listing.png?raw=true)

Let's try directory traversal. It works: `https://school.fluxfingers.net:1522/?module=../index.php` includes `index.php` in place of a module.

![](index.png?raw=true)

After a few guesses, turns out `../.htaccess` has something interesting:

```
# needs to be hidden from direct access <!--
# seems to be not working, though
#<Directory "3cdcf3c63dc02f8e5c230943d9f1f4d75a4d88ae">
#    Options -Indexes
#</Directory>
# -->
```

Let's open the dir:

![](dir.png?raw=true)

Opening `flag.php` to get our flag:

```
not that easy, fella
```

Minor setback. Let's include the file through `?module`: `https://school.fluxfingers.net:1522/?module=../3cdcf3c63dc02f8e5c230943d9f1f4d75a4d88ae/flag.php` reveals the flag.

![](flag.png?raw=true)
