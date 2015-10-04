# Entry language - (Reverse 100)

## Problem

You might be able to talk like them once you find who they are.

## Analysis

Below is the password hashing and comparison function. Examining the comparison we see that it compares our input byte by byte, with a calculated hash value. It expects the result of the comparison to equal 1, so our input byte values will need to be 1 smaller than the actual key.

```
signed __int64 __fastcall sub_4006FD(__int64 input)
{
  signed int i; // [sp+14h] [bp-24h]@1
  char v3[8]; // [sp+18h] [bp-20h]@1
  char v4[8]; // [sp+20h] [bp-18h]@1
  char v5[8]; // [sp+28h] [bp-10h]@1
  *(_QWORD *)v3 = "Dufhbmf";
  *(_QWORD *)v4 = "pG`imos";
  *(_QWORD *)v5 = "ewUglpt";
  for ( i = 0; i <= 11; ++i )
  {
    if ( *(_BYTE *)(*(_QWORD *)&v3[8 * (i % 3)] + 2 * (i / 3)) - *(_BYTE *)(i + input) != 1 )
      return 1LL;
  }
  return 0LL;
}
```
```
//the meat
*(_BYTE *)(*(_QWORD *)&v3[8 * (i % 3)] + 2 * (i / 3)) - *(_BYTE *)(i + input) != 1
```
Time to open gdb and see if we can breakpoint the comparison and see what it does.

```
xpl0@kali:~/Desktop# gdb ./r101 
(gdb) start
Function "main" not defined.
Make breakpoint pending on future shared library load? (y or [n]) y

Temporary breakpoint 1 (main) pending.
Starting program: /home/xpl0/Desktop/r101 
asd
hello!
<<STUCK IN SOME LOOP??
^Z
Program received signal SIGTSTP, Stopped (user).
0x00000000004007e4 in ?? ()
```

Right there I got stuck or something so I went to the address 0x00000000004007e4 in IDA and it shows the following C code.

```
//0x00000000004007e4:jmp     short loc_4007E4

int sub_4007A8()
{
  __int64 v0; // rax@3

  if ( (unsigned int)getenv("LD_PRELOAD") )
  {
    while ( 1 )
      ;
  }
  LODWORD(v0) = ptrace(0, 0LL, 0LL, 0LL);
  if ( v0 < 0 )
  {
    while ( 1 )// I'M STUCK HERE SEND HELP!
      ;
  }
  return v0;
}
```

It is a two byte JMP SHORT operation so lets just try to take it out and keep going.

## Solution
Credit: [@gellin](https://github.com/gellin)


```
(gdb) set *(byte*)0x4007e4=0x90
(gdb) set *(byte*)0x4007e5=0x90
(gdb) b* 0x400784
Breakpoint 2 at 0x400784
(gdb) c
Continuing.

Program received signal SIGTSTP, Stopped (user).
0x00000000004007e4 in ?? ()
(gdb) c
Continuing.
Enter the password: AAAAAAAAAAAAAA

Breakpoint 4, 0x0000000000400784 in ?? ()
(gdb) print $edx
$1 = 68
(gdb) print $eax
$2 = 65
(gdb) set $eax=67
(gdb) c
Continuing.

Breakpoint 4, 0x0000000000400784 in ?? ()
(gdb) print $edx
$3 = 112
(gdb) set $eax=111
(gdb) c
Continuing.

Breakpoint 4, 0x0000000000400784 in ?? ()
(gdb) print $edx
$4 = 101
(gdb) set $eax=100
(gdb) c
Continuing.

Breakpoint 4, 0x0000000000400784 in ?? ()
(gdb) print $edx
$5 = 102
(gdb) set $eax=101
(gdb) c
Continuing.

Breakpoint 4, 0x0000000000400784 in ?? ()
(gdb) print $edx
$6 = 96
(gdb) set $eax=95
(gdb) print $edx
$7 = 96
(gdb) set $eax=95
(gdb) c
Continuing.

Breakpoint 4, 0x0000000000400784 in ?? ()
(gdb) print $edx
$8 = 85
(gdb) set $eax=84
(gdb) c
Continuing.

Breakpoint 4, 0x0000000000400784 in ?? ()
(gdb) print $edx
$9 = 98
(gdb) set $eax=97
(gdb) c
Continuing.

Breakpoint 4, 0x0000000000400784 in ?? ()
(gdb) print $edx
$10 = 109
(gdb) set eax=108
No symbol "eax" in current context.
(gdb) set $eax=108
(gdb) c
Continuing.

Breakpoint 4, 0x0000000000400784 in ?? ()
(gdb) print $edx
$11 = 108
(gdb) set $eax=107
(gdb) c
Continuing.

Breakpoint 4, 0x0000000000400784 in ?? ()
(gdb) print $edx
$12 = 102
(gdb) set $eax=101
(gdb) c
Continuing.

Breakpoint 4, 0x0000000000400784 in ?? ()
(gdb) print $edx
$13 = 115
(gdb) set $eax=114
(gdb) c
Continuing.

Breakpoint 4, 0x0000000000400784 in ?? ()
(gdb) print $edx
$14 = 116
(gdb) set $eax=115
(gdb) c
Continuing.
Nice!
[Inferior 1 (process 3590) exited normally]
(gdb) 
```
Converting all of the edx registers from decimal to ascii, and concatenating them together it ends up being.

```
Code_Talkers

68 - C 
112 - o 
101 - d 
102 - e 
96 - _
85 - T 
98 - a 
109 - l 
108 - k 
102 - e 
115 - r 
116 - s

```

We try it as a flag and it works!