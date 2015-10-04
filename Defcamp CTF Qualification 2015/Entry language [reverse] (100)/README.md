# Entry language - (Reverse 100)

## Problem

You might be able to talk like them once you find who they are.

## Analysis & Solution
Credit: [@gellin](https://github.com/gellin)

```
xpl0@kali:~/Desktop# file r100
r100: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=0f464824cc8ee321ef9a80a799c70b1b6aec8168, stripped
```
Next we dropped it into IDA64 and found the two useful functions.
Below is the password hashing and comparison function that takes in our input "password". Examining the comparison we see that it compares our input byte by byte, with a calculated hash value. 
It expects the result of the comparison to equal 1, so our input byte values will need to be 1 smaller than the actual key.

```
signed __int64 sub_4007E8()
{
  signed __int64 result; // rax@3
  __int64 v1; // rcx@6
  char input; // [sp+0h] [bp-110h]@1
  __int64 v3; // [sp+108h] [bp-8h]@1

  v3 = *MK_FP(__FS__, 40LL);
  printf("Enter the password: ");
  if ( fgets(&input, 255, stdin) )
  {
    if ( sub_4006FD(&input) )                   // right here it passes our input to the pass hash & compare function.
    {
      puts("Incorrect password!");
      result = 1LL;
    }
    else
    {
      puts("Nice!");
      result = 0LL;
    }
  }
  else
  {
    result = 0LL;
  }
  v1 = *MK_FP(__FS__, 40LL) ^ v3;
  return result;
}

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

.text:000000000040076E                 movzx   eax, byte ptr [rax]
.text:0000000000400771                 movsx   edx, al
.text:0000000000400774                 mov     eax, [rbp+var_24]
.text:0000000000400777                 movsxd  rcx, eax
.text:000000000040077A                 mov     rax, [rbp+var_38]
.text:000000000040077E                 add     rax, rcx
.text:0000000000400781                 movzx   eax, byte ptr [rax]
.text:0000000000400784                 movsx   eax, al
.text:0000000000400787                 sub     edx, eax
.text:0000000000400789                 mov     eax, edx
.text:000000000040078B                 cmp     eax, 1
.text:000000000040078E                 jz      short loc_400797
```

Time to open gdb to see if we can breakpoint at 0x400784 and see if we can steal the values we need out of the registers.

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

Right there I got stuck in what I thought was an infinite loop, so I went to the address 0x00000000004007e4 in IDA and it shows the following C code.

```
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

We are stuck in a two byte JMP SHORT operation 

```
//0x00000000004007e4:jmp     short loc_4007E4
```

So lets just try to take it out(NOP) and keep going.


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