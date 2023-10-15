# [Misc] Chillt Out - 50 Pts.

  
We’re given with this wav file.  
![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/chill_out_1.png)  
A teammate of mine, EnGyn, managed to pull out an ELF file out of the WAV file using [deepsound](http://jpinsoft.net/deepsound/documentation.aspx)  
![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/chill_out_2.png)  
We ran `strings` command on the `hello` binary file and and found a `PyInstaller` keyword in there.  
![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/chill_out_3.png)  
Suspecting that it may have been compiled using PyInstaller, we extracted that contents using [pyinstxtractor.py](https://github.com/extremecoders-re/pyinstxtractor). However, there is a problem when we tried it in my Kali Linux. A warning has appeared.  
![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/chill_out_5.png)  
Since the python3 version I have is 3.11.2, there’s likely going to have a problem later when we try to reverse engineer the files further. I don’t want to brick my python3 also by installing another version. So we switched to my Remnux Box which has a compatible python3 version. In there, we ran the pyinstxtractor.py  
![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/chill_out_4.png)  
`hello_extracted` folder has been created.  
![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/chill_out_6.png)  
As instructed also, we tried reverting .pyc file to .py and hopefully retrieve the original python script. We used [uncompyle6](https://pypi.org/project/uncompyle6/)  
![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/chill_out_7.png)  
Turns out as well that it’s protected by [PyArmor](https://github.com/dashingsoft/pyarmor). Any debofuscation scripts we have used didn’t work. The plan now is to dump the memory of the script when the pyarmor has already deobfuscated the script for us. We used this [memory dumper](https://gist.githubusercontent.com/Dbof/b9244cfc607cf2d33438826bee6f5056/raw/aa4b75ddb55a58e2007bf12e17daadb0ebebecba/memdump.py).  
We will attempt the steps below:

1) Run a waiting one-liner command where if it sees the .pyc is running, it will retrieve its PID and use it to dump the memory immediately. 2) Run the .pyc file. 3) Analyze the dumped memory  
However, the above steps can only work if we can manage to run the script in the first place. Fortunately, we can. We just have to put `hello.pyc`, `\_pytransform.so`, and `pytransform.pyc` in the same directory.  
![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/chill_out_8.png)  
We also noticed that the script requires an argument.  
The following bash one-liner is used to wait and dump the memory of the target pyc script:  

```

while true;do x=$( ps -aux | grep hello.pyc | grep grep -v | awk '{ print $2 }'); if [ ${#x} -ge 1 ]; then ( sleep 0.05; python3 memdump.py $x); fi;done

```

  
Also notice that we put `sleep 0.05` in there. The waiting command is too fast and dumps the memory immediately while the pyarmor is yet to deobfuscate the script. The `sleep` serves as a waiting mechanism to give time pyarmor to deobfuscate the script.  
We executed the one-liner and once it sees the running pyc file, it will attempt to dump it.  
![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/chill_out_9.png)  
The dump is then output to 161043.dump

  
![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/chill_out_10.png)

  
Next is to analyze the dump. First, we just output the strings. We found a string that pertains to the CTF organizers with heart symbol on it.

  
![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/chill_out_11.png)

  
We tried this as the argument:

  
![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/chill_out_12.png)

  
We got the flag: `rc{jus7_r3m3mb3r_th4t_it_aint_0v3r_t1ll_its_over}`

  
Author’s note: This technique is a hit or miss. Many tries have been done before a remarkable result has been obtained since this is a race-condition based approach.