# [BinForCry] Mobster - 50 Pts.

  
We’re given with this file.  
![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/mobster_1.png)  
Checking out the file, it looks like a python code but something weird is being appended on the end. Also noticed that if we ever run this python script, there’s a chance that it will brick our system by executing something from `/usr/bin`.  

![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/mobster_2.png)  

From above, we can also see the first line `#coding: punycode`. Searching it, we found some other writeups on how they solve this kind of CTFs. We chose the [second one](https://medium.com/@0xMr_Robot/downunder-ctf-2023-reverse-engineering-challenges-205fc71e84ab).  
![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/mobster_3.png)  
Turns out, we can run the following code against the mobster.py file.  

```
f = open('<>', 'rb').read()
print(f.replace(b'#coding: punycode',b'').decode('punycode'))
```

  
Running it, below is the output: We can derive the flag from above:  
![lol it didn't load](https://altelus1.github.io/writeups/ctf/rootcon17quals/images/mobster_4.png)  
Flag is: `RC17{welcome_2_russian_roulette}`