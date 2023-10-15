We’re given a file: ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_1.png#%20big)  

And when we run it, it asks for magic password: ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_7.png#%20medium)  

Checking it with gdb: ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_2.png#%20big-p) The symbol table only contains plt entries. Before digging in GDB, let’s analyze the binary with Ghidra.  

After Ghidra was able to analyze the file, we’re able to find the main function: ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_3.png#%20medium-p)  

But upon looking at GDB, we can see that there are is one more address called: 0x8048440 but we can ignore since what it does is only get the next instruction address and store it at ebx. ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_4.png#%20small)  

However, what’s interesting is the result of ebx when added to 0x2ae6. Let’s run and set breakpoint at address 0x8048520: ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_5.png#%20medium) As we can see from above image, the value of EBX = 0x804b000. Let’s check the byte contents.  

Here is the byte contents from address0x804b000: ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_6.png#%20big)

Interesting! Some of the values lying around at different addresses looks like are printable bytes! It looks like for the VM this is where its _data segment_ starts. Let’s check the values:

```
Addresses:
0x804b060 -> "Welcome to SECURINETS CTF!\n"
0x804b0a0 -> "Give me the magic:"
0x804b0e0 -> "No...\n"
0x804b120 -> "Just get out ; No place for you here!\n"
0x804b1a0 -> "Good Job! You win!\n"
0x804b1e0 -> "Sz}hnrt|ldmcyLbc {=nx::gWu6fo6#|"
```

The string at 0x804b1e0 is the definitely the most interesting one. (In fact this is actually the encrypted flag. We just have to know how this is encrypted.)  

## How does the VM do its routine?

Upon checking the Ghidra, we can see that it calls 0x8048568 and when we check the disassembly in GDB.0x8048568:

```
   0x8048568:	push   ebp				
   0x8048569:	mov    ebp,esp
   0x804856b:	push   ebx
   0x804856c:	sub    esp,0x24
   0x804856f:	call   0x8048440
   0x8048574:	add    ebx,0x2a8c
   0x804857a:	mov    eax,gs:0x14
   0x8048580:	mov    DWORD PTR [ebp-0xc],eax
   0x8048583:	xor    eax,eax
   0x8048585:	mov    DWORD PTR [ebp-0x28],0x0
   0x804858c:	cmp    DWORD PTR [ebp+0x8],0x14 #This checks the canary
   0x8048590:	ja     0x8048cb9	
   0x8048596:	mov    eax,DWORD PTR [ebp+0x8] #ebp + 0x8 is 0 at first loop
   0x8048599:	shl    eax,0x2
   0x804859c:	mov    eax,DWORD PTR [eax+ebx*1-0x226c] 
   0x80485a3:	add    eax,ebx
   0x80485a5:	jmp    eax
```

Taking a look to the assembly above, what interests us is from address 0x8048596 - 0x80485a5 since this is how **addresses to different functions is calculated**. The most critical one for us is 0x80485a5 since this jumps to the subroutine the program is going to do. We can ignore everything else in it  

Let’s set a breakpoint to this address. When we run it, it will point to different address and it will do what it needs to be done (e.g. getting input, printing, encrypting etc.). However, we’re only concerned to addresses that **(a) gets input** and **(b) encrypts our input** because we will only have to check the transformation of our input once we get to the encryption function and how the encryption function works.

## Getting user input address

We will know the address that gets user input at registerEAX when it stops at our breakpoint and when we hit “continue” the program asks for a user input. ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_8.png#%20big-p) As we can see, the user input get function is at address 0x8048851. We’ll insert the following input above lol.  

Let’s check where does it store our user input. By following **any** jump instruction from that address, we will arrive at address 0x80488c9: ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_9.png#%20medium-p) Let’s set breakpoint to 0x80488ef. Let’s rerun the program again and check the stack since it will contain the destination address. Here is the stack value when it our breakpoints.: ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_10.png#%20big) Since scanf is used for getting the user input, the second value in the stack is actually the address where our input is stored! Address of our input is : 0x804b240. We can confirm this by stepping another instruction (Remark: Scanf doesn’t include strings after the first space!) ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_11.png#%20small).  

### Minor problem

However, our input seems not to be encrypted. We can know this by setting our breakpoint again to 0x80485a5 and by checking our string input `x/s 0x804b240` every time it hits our breakpoint. “No…” is printed but there are no changes to our input. ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_13.png#%20medium-p)  
When we rerun our program again with the same breakpoint and still checking our input, at some point the program jumps to address 0x804894e which has `strlen()` in it. It probably requires a certain length for our input. ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_12.png#%20medium-p)  
Let’s go check the most interesting string’s length.

```
>>> len("Sz}hnrt|ldmcyLbc {=nx::gWu6fo6#|")
32
```

Let’s try again with 32 “a”s. ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_14.png#%20medium) Let’s check if we still get “No…” response by breaking at 0x80485a5 and continuing. Let’s also check our input if there are changes made to it in case 32 “a”s as input works.  
After breaking and continuing, we arrived at the first instance where our first character in our input changed! ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_15.png#%20medium-p) And this changed happened when **after** we jumped to address 0x8048b16 so this must be the encryption function! ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_16.png#%20medium-p)  

## The Encryption function

The address of the encryption function is **0x8048b16**. Now, we have to know how it works so we can decrypt the encrypted flag we have. This is the assembly of the encryption function.

```
   0x8048b16:	mov    eax,DWORD PTR [ebx+0x40]
   0x8048b1c:	add    eax,0x1
   0x8048b1f:	mov    DWORD PTR [ebx+0x40],eax
   0x8048b25:	mov    eax,DWORD PTR [ebx+0x40]
   0x8048b2b:	mov    edx,DWORD PTR [ebx+eax*4-0x2c0]
   0x8048b32:	mov    eax,0x804b420
   0x8048b38:	mov    eax,DWORD PTR [eax+edx*4]
   0x8048b3b:	mov    DWORD PTR [ebp-0x24],eax
   0x8048b3e:	mov    eax,DWORD PTR [ebx+0x40]
   0x8048b44:	add    eax,0x1
   0x8048b47:	mov    DWORD PTR [ebx+0x40],eax
   0x8048b4d:	mov    eax,DWORD PTR [ebx+0x40]
   0x8048b53:	mov    edx,DWORD PTR [ebx+eax*4-0x2c0]
   0x8048b5a:	mov    eax,0x804b420
   0x8048b60:	mov    eax,DWORD PTR [eax+edx*4]
   0x8048b63:	mov    DWORD PTR [ebp-0x20],eax
   0x8048b66:	mov    eax,DWORD PTR [ebx+0x40]
   0x8048b6c:	add    eax,0x1
   0x8048b6f:	mov    DWORD PTR [ebx+0x40],eax
   0x8048b75:	mov    eax,DWORD PTR [ebx+0x40]
   0x8048b7b:	mov    eax,DWORD PTR [ebx+eax*4-0x2c0]
   0x8048b82:	mov    DWORD PTR [ebp-0x1c],eax
   0x8048b85:	mov    edx,DWORD PTR [ebp-0x20]
   0x8048b88:	mov    eax,DWORD PTR [ebp-0x1c]
   0x8048b8b:	add    eax,edx
   0x8048b8d:	movzx  ecx,BYTE PTR [eax]
   0x8048b90:	mov    eax,DWORD PTR [ebp-0x24]
   0x8048b93:	mov    ebx,eax
   0x8048b95:	mov    edx,DWORD PTR [ebp-0x20]
   0x8048b98:	mov    eax,DWORD PTR [ebp-0x1c]
   0x8048b9b:	add    eax,edx
   0x8048b9d:	xor    ecx,ebx
   0x8048b9f:	mov    edx,ecx
   0x8048ba1:	mov    BYTE PTR [eax],dl
   0x8048ba3:	jmp    0x8048cb9
```

However, what interests us is an instruction that saves 1 byte to to an address. This assumption was made since a transformed byte must be saved to our input address and the only instruction that does that is at address 0x8048ba1. Now, we have to find an instruction before it that does an arithmetic/bit operation (xor, sub, and, add etc.) and it s the instruction at 0x8048b9d. Let’s delete all of our breakpoints and set a new breakpoint to 0x8048b9d to see the value of ECX and EBX. Let’s now rerun the program.

```
#By checking the registers every time it hits the breakpoint here are the values
1 ----
EBX: 0x20 (' ')
ECX: 0x61 ('a')
XOR = 'A'
2 ----
EBX: 0x1f 
ECX: 0x61 ('a')
XOR = '~'
3 ----
EBX: 0x1e 
ECX: 0x61 ('a')
XOR = '\x7f'
4 ----
EBX: 0x1d 
ECX: 0x61 ('a')
XOR = '|'
---ommitted---
```

We can see a pattern in here! A countdown value from 0x20 XOR per character is the encryption operation! Let’s decrypt the encrypted flag earlier!

```
x = "Sz}hnrt|ldmcyLbc {=nx::gWu6fo6#|"

for i in range(len(x)):
	print(chr(ord(x[i]) ^ 0x20-i),end="")

print("")
```

  
And here is our result! ![file missing](https://altelus1.github.io/writeups/ctf/securinetspreq2020/images/kavm_17.png)

Flag: _securinets{vm_pr0t3ct10n_r0ck5!}_

  
Thank you for reading!