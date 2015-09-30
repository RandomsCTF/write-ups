# Analysis - Offensive 100

## Problem

[vonn.zip](puzzle/vonn.zip)

Analyze this! (pass: wx5tOCvU3g2FmueLEvj5np9xJX0cND3K)

## Solution

Credit: [@gellin](https://github.com/gellin)

It doesn't come with any hints or direction, so lets take a stab at it with the `file` command.

```
root@kali:/media/sf_vm_share# file vonn
vonn: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=7f89c2bb36cc9d0882a4980a99d44a7674fb09e2, not stripped
```

Now lets see what `IDA 64` says about it.

![](./1.png?raw=true)

The main function looks pretty simple, it loads a few variables, and then does a few checks on them only resulting in two main case `branches`. In one case, it prints `You are not on VMM` and then simply returns, in the other case it prints `You are on VMM!` and then calls a function named `ldex`. So we should already be assuming we need to make this program call `ldex` so lets take a look at it!

![](./2.png?raw=true)

After reading the function it appears to do the following. Open a handle to `/tmp/...,,,...,,` on the HDD. Read a buffer into memory, decrypt the buffer and write it to the open handle and finally execute the file `/tmp/...,,,...,,`.

So its time to open `gdb` in our VM and try to break it, lets atleast see what this file `/tmp/...,,,...,,` is all about.

```
root@kali:/media/sf_vm_share# gdb ./vonn
(gdb) start
Temporary breakpoint 1 at 0x400b91
Starting program: /media/sf_vm_share/vonn
Temporary breakpoint 1, 0x0000000000400b91 in main ()
(gdb) disas main
Dump of assembler code for function main:
   0x0000000000400b8d <+0>:	push   %rbp
   0x0000000000400b8e <+1>:	mov    %rsp,%rbp
   0x0000000000400b91 <+4>:	sub    $0xd0,%rsp
   0x0000000000400b98 <+11>:	mov    %edi,-0xc4(%rbp)
   0x0000000000400b9e <+17>:	mov    %rsi,-0xd0(%rbp)
   0x0000000000400ba5 <+24>:	cpuid
   0x0000000000400ba7 <+26>:	rdtsc
   0x0000000000400ba9 <+28>:	mov    %rax,-0xb8(%rbp)
   0x0000000000400bb0 <+35>:	mov    %rdx,-0xb0(%rbp)
   0x0000000000400bb7 <+42>:	rdtsc
   0x0000000000400bb9 <+44>:	mov    %rax,-0xa8(%rbp)
   0x0000000000400bc0 <+51>:	mov    %rdx,-0xa0(%rbp)
   0x0000000000400bc7 <+58>:	rdtsc
   0x0000000000400bc9 <+60>:	mov    %rax,-0x98(%rbp)
   0x0000000000400bd0 <+67>:	mov    %rdx,-0x90(%rbp)
   0x0000000000400bd7 <+74>:	rdtsc
   0x0000000000400bd9 <+76>:	mov    %rax,-0x88(%rbp)
   0x0000000000400be0 <+83>:	mov    %rdx,-0x80(%rbp)
   0x0000000000400be4 <+87>:	mov    -0xb8(%rbp),%rax
   0x0000000000400beb <+94>:	mov    %rax,-0x78(%rbp)
   0x0000000000400bef <+98>:	mov    -0xb0(%rbp),%rax
   0x0000000000400bf6 <+105>:	mov    %rax,-0x70(%rbp)
---Type <return> to continue, or q <return> to quit---
   0x0000000000400bfa <+109>:	mov    -0xa8(%rbp),%rax
   0x0000000000400c01 <+116>:	mov    %rax,-0x68(%rbp)
   0x0000000000400c05 <+120>:	mov    -0xa0(%rbp),%rax
   0x0000000000400c0c <+127>:	mov    %rax,-0x60(%rbp)
   0x0000000000400c10 <+131>:	mov    -0x98(%rbp),%rax
   0x0000000000400c17 <+138>:	mov    %rax,-0x58(%rbp)
   0x0000000000400c1b <+142>:	mov    -0x90(%rbp),%rax
   0x0000000000400c22 <+149>:	mov    %rax,-0x50(%rbp)
   0x0000000000400c26 <+153>:	mov    -0x88(%rbp),%rax
   0x0000000000400c2d <+160>:	mov    %rax,-0x48(%rbp)
   0x0000000000400c31 <+164>:	mov    -0x80(%rbp),%rax
   0x0000000000400c35 <+168>:	mov    %rax,-0x40(%rbp)
   0x0000000000400c39 <+172>:	mov    -0x70(%rbp),%rax
   0x0000000000400c3d <+176>:	shl    $0x20,%rax
   0x0000000000400c41 <+180>:	or     -0xb8(%rbp),%rax
   0x0000000000400c48 <+187>:	mov    %rax,-0x38(%rbp)
   0x0000000000400c4c <+191>:	mov    -0x60(%rbp),%rax
   0x0000000000400c50 <+195>:	shl    $0x20,%rax
   0x0000000000400c54 <+199>:	or     -0xa8(%rbp),%rax
   0x0000000000400c5b <+206>:	mov    %rax,-0x30(%rbp)
   0x0000000000400c5f <+210>:	mov    -0x50(%rbp),%rax
   0x0000000000400c63 <+214>:	shl    $0x20,%rax
   0x0000000000400c67 <+218>:	or     -0x98(%rbp),%rax
---Type <return> to continue, or q <return> to quit---
   0x0000000000400c6e <+225>:	mov    %rax,-0x28(%rbp)
   0x0000000000400c72 <+229>:	mov    -0x40(%rbp),%rax
   0x0000000000400c76 <+233>:	shl    $0x20,%rax
   0x0000000000400c7a <+237>:	or     -0x88(%rbp),%rax
   0x0000000000400c81 <+244>:	mov    %rax,-0x20(%rbp)
   0x0000000000400c85 <+248>:	mov    -0x38(%rbp),%rax
   0x0000000000400c89 <+252>:	mov    -0x30(%rbp),%rdx
   0x0000000000400c8d <+256>:	sub    %rax,%rdx
   0x0000000000400c90 <+259>:	mov    %rdx,%rax
   0x0000000000400c93 <+262>:	mov    %rax,-0x18(%rbp)
   0x0000000000400c97 <+266>:	mov    -0x30(%rbp),%rax
   0x0000000000400c9b <+270>:	mov    -0x28(%rbp),%rdx
   0x0000000000400c9f <+274>:	sub    %rax,%rdx
   0x0000000000400ca2 <+277>:	mov    %rdx,%rax
   0x0000000000400ca5 <+280>:	mov    %rax,-0x10(%rbp)
   0x0000000000400ca9 <+284>:	mov    -0x28(%rbp),%rax
   0x0000000000400cad <+288>:	mov    -0x20(%rbp),%rdx
   0x0000000000400cb1 <+292>:	sub    %rax,%rdx
   0x0000000000400cb4 <+295>:	mov    %rdx,%rax
   0x0000000000400cb7 <+298>:	mov    %rax,-0x8(%rbp)
   0x0000000000400cbb <+302>:	mov    -0x18(%rbp),%rax
   0x0000000000400cbf <+306>:	cmp    -0x10(%rbp),%rax
   0x0000000000400cc3 <+310>:	je     0x400cfc <main+367>
---Type <return> to continue, or q <return> to quit---
   0x0000000000400cc5 <+312>:	mov    -0x10(%rbp),%rax
   0x0000000000400cc9 <+316>:	cmp    -0x8(%rbp),%rax
   0x0000000000400ccd <+320>:	je     0x400cfc <main+367>
   0x0000000000400ccf <+322>:	mov    -0x18(%rbp),%rax
   0x0000000000400cd3 <+326>:	cmp    -0x8(%rbp),%rax
   0x0000000000400cd7 <+330>:	je     0x400cfc <main+367>
   0x0000000000400cd9 <+332>:	mov    $0x401100,%edi
   0x0000000000400cde <+337>:	callq  0x400990 <puts@plt>
   0x0000000000400ce3 <+342>:	mov    -0xd0(%rbp),%rax
   0x0000000000400cea <+349>:	mov    (%rax),%rax
   0x0000000000400ced <+352>:	mov    %rax,%rdi
   0x0000000000400cf0 <+355>:	mov    $0x0,%eax
   0x0000000000400cf5 <+360>:	callq  0x400d08 <ldex>
   0x0000000000400cfa <+365>:	jmp    0x400d06 <main+377>
   0x0000000000400cfc <+367>:	mov    $0x401110,%edi
   0x0000000000400d01 <+372>:	callq  0x400990 <puts@plt>
   0x0000000000400d06 <+377>:	leaveq
   0x0000000000400d07 <+378>:	retq
End of assembler dump.
```

So we can see the jumps at - `0x400cc3`,  `0x400ccd`, and `0x400cd7`. So lets try the `lazy` way of breaking the JE (jump if equal), instructions first.  You could also change them to JNE (jump if not equal), or just make a JMP or call to `ldex`.

```
(gdb) set *(unsigned char*)0x400cc3 = 0x90
(gdb) set *(unsigned char*)0x400cc4 = 0x90
(gdb) set *(unsigned char*)0x400ccd = 0x90
(gdb) set *(unsigned char*)0x400cce = 0x90
(gdb) set *(unsigned char*)0x400cd7 = 0x90
(gdb) set *(unsigned char*)0x400cd8 = 0x90
(gdb) disas main
Dump of assembler code for function main:
   0x0000000000400b8d <+0>: push   %rbp
   0x0000000000400b8e <+1>: mov    %rsp,%rbp
   0x0000000000400b91 <+4>: sub    $0xd0,%rsp
   0x0000000000400b98 <+11>:    mov    %edi,-0xc4(%rbp)
   0x0000000000400b9e <+17>:    mov    %rsi,-0xd0(%rbp)
   0x0000000000400ba5 <+24>:    cpuid
   0x0000000000400ba7 <+26>:    rdtsc
   0x0000000000400ba9 <+28>:    mov    %rax,-0xb8(%rbp)
   0x0000000000400bb0 <+35>:    mov    %rdx,-0xb0(%rbp)
   0x0000000000400bb7 <+42>:    rdtsc
   0x0000000000400bb9 <+44>:    mov    %rax,-0xa8(%rbp)
   0x0000000000400bc0 <+51>:    mov    %rdx,-0xa0(%rbp)
   0x0000000000400bc7 <+58>:    rdtsc
   0x0000000000400bc9 <+60>:    mov    %rax,-0x98(%rbp)
   0x0000000000400bd0 <+67>:    mov    %rdx,-0x90(%rbp)
   0x0000000000400bd7 <+74>:    rdtsc
   0x0000000000400bd9 <+76>:    mov    %rax,-0x88(%rbp)
   0x0000000000400be0 <+83>:    mov    %rdx,-0x80(%rbp)
   0x0000000000400be4 <+87>:    mov    -0xb8(%rbp),%rax
   0x0000000000400beb <+94>:    mov    %rax,-0x78(%rbp)
   0x0000000000400bef <+98>:    mov    -0xb0(%rbp),%rax
   0x0000000000400bf6 <+105>:   mov    %rax,-0x70(%rbp)
   0x0000000000400bfa <+109>:   mov    -0xa8(%rbp),%rax
   0x0000000000400c01 <+116>:   mov    %rax,-0x68(%rbp)
   0x0000000000400c05 <+120>:   mov    -0xa0(%rbp),%rax
   0x0000000000400c0c <+127>:   mov    %rax,-0x60(%rbp)
   0x0000000000400c10 <+131>:   mov    -0x98(%rbp),%rax
   0x0000000000400c17 <+138>:   mov    %rax,-0x58(%rbp)
   0x0000000000400c1b <+142>:   mov    -0x90(%rbp),%rax
   0x0000000000400c22 <+149>:   mov    %rax,-0x50(%rbp)
   0x0000000000400c26 <+153>:   mov    -0x88(%rbp),%rax
   0x0000000000400c2d <+160>:   mov    %rax,-0x48(%rbp)
   0x0000000000400c31 <+164>:   mov    -0x80(%rbp),%rax
   0x0000000000400c35 <+168>:   mov    %rax,-0x40(%rbp)
   0x0000000000400c39 <+172>:   mov    -0x70(%rbp),%rax
   0x0000000000400c3d <+176>:   shl    $0x20,%rax
   0x0000000000400c41 <+180>:   or     -0xb8(%rbp),%rax
   0x0000000000400c48 <+187>:   mov    %rax,-0x38(%rbp)
   0x0000000000400c4c <+191>:   mov    -0x60(%rbp),%rax
   0x0000000000400c50 <+195>:   shl    $0x20,%rax
   0x0000000000400c54 <+199>:   or     -0xa8(%rbp),%rax
   0x0000000000400c5b <+206>:   mov    %rax,-0x30(%rbp)
   0x0000000000400c5f <+210>:   mov    -0x50(%rbp),%rax
   0x0000000000400c63 <+214>:   shl    $0x20,%rax
   0x0000000000400c67 <+218>:   or     -0x98(%rbp),%rax
   0x0000000000400c6e <+225>:   mov    %rax,-0x28(%rbp)
   0x0000000000400c72 <+229>:   mov    -0x40(%rbp),%rax
---Type <return> to continue, or q <return> to quit---
   0x0000000000400c76 <+233>:   shl    $0x20,%rax
   0x0000000000400c7a <+237>:   or     -0x88(%rbp),%rax
   0x0000000000400c81 <+244>:   mov    %rax,-0x20(%rbp)
   0x0000000000400c85 <+248>:   mov    -0x38(%rbp),%rax
   0x0000000000400c89 <+252>:   mov    -0x30(%rbp),%rdx
   0x0000000000400c8d <+256>:   sub    %rax,%rdx
   0x0000000000400c90 <+259>:   mov    %rdx,%rax
   0x0000000000400c93 <+262>:   mov    %rax,-0x18(%rbp)
   0x0000000000400c97 <+266>:   mov    -0x30(%rbp),%rax
   0x0000000000400c9b <+270>:   mov    -0x28(%rbp),%rdx
   0x0000000000400c9f <+274>:   sub    %rax,%rdx
   0x0000000000400ca2 <+277>:   mov    %rdx,%rax
   0x0000000000400ca5 <+280>:   mov    %rax,-0x10(%rbp)
   0x0000000000400ca9 <+284>:   mov    -0x28(%rbp),%rax
   0x0000000000400cad <+288>:   mov    -0x20(%rbp),%rdx
   0x0000000000400cb1 <+292>:   sub    %rax,%rdx
   0x0000000000400cb4 <+295>:   mov    %rdx,%rax
   0x0000000000400cb7 <+298>:   mov    %rax,-0x8(%rbp)
   0x0000000000400cbb <+302>:   mov    -0x18(%rbp),%rax
   0x0000000000400cbf <+306>:   cmp    -0x10(%rbp),%rax
=> 0x0000000000400cc3 <+310>:   nop
   0x0000000000400cc4 <+311>:   nop
   0x0000000000400cc5 <+312>:   mov    -0x10(%rbp),%rax
   0x0000000000400cc9 <+316>:   cmp    -0x8(%rbp),%rax
   0x0000000000400ccd <+320>:   nop
   0x0000000000400cce <+321>:   nop
   0x0000000000400ccf <+322>:   mov    -0x18(%rbp),%rax
   0x0000000000400cd3 <+326>:   cmp    -0x8(%rbp),%rax
   0x0000000000400cd7 <+330>:   nop
   0x0000000000400cd8 <+331>:   nop
   0x0000000000400cd9 <+332>:   mov    $0x401100,%edi
   0x0000000000400cde <+337>:   callq  0x400990 <puts@plt>
   0x0000000000400ce3 <+342>:   mov    -0xd0(%rbp),%rax
   0x0000000000400cea <+349>:   mov    (%rax),%rax
   0x0000000000400ced <+352>:   mov    %rax,%rdi
   0x0000000000400cf0 <+355>:   mov    $0x0,%eax
   0x0000000000400cf5 <+360>:   callq  0x400d08 <ldex>
   0x0000000000400cfa <+365>:   jmp    0x400d06 <main+377>
   0x0000000000400cfc <+367>:   mov    $0x401110,%edi
   0x0000000000400d01 <+372>:   callq  0x400990 <puts@plt>
   0x0000000000400d06 <+377>:   leaveq
   0x0000000000400d07 <+378>:   retq
End of assembler dump.
```
Now that we verified the jump's are `DEAD`, we are going to let it ride!

```
(gdb) continue
Continuing.
You are on VMM!
process 1463 is executing new program: /tmp/...,,,...,,
TMCTF{ce5d8bb4d5efe86d25098bec300d6954}[Inferior 1 (process 1463) exited with code 0377]
/tmp/...,,,...,,: No such file or directory.
(gdb)
```

Boom there's the flag!

If you need take the time to analyze `/tmp/...,,,...,,`, you will find that it is just another trojan dropper like application, with the same but opposite `VMM` check if I recall correctly. It can be broken the same way.

Note - This challenge may differ if you are on a VM or running it native.
