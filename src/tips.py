import random
import sys

# linux/bash tips and tricks
tips = ['.. marks the directory above', 
        ' . marks your current directory', 
        'cd alone takes you home',
        '~ represents your home directory',
        'press ctl-C to stop processing a command', 
        'how to Vim: vim <filename>, i (insert mode), <type words>, esc, :wq', 
        'tab can auto-complete your commands', 
        'basic inventory: hostname, tty, uname -r, who, echo $PATH, cat /etc/*-release', 
        'files: ls, cp, cat/more/less, head/tail, vi', 
        'redirection: command > filename (write), command >> filename (append)', 
        'install: apt-get install <item>', 
        'remote login: ssh -p <port> <user>@<hostname/ip>',
        'Linux is not an OS, it is the kernel of GNU Linux which comes in many flavors',
        'only 2% of todays kernel contains code written by Linux Torvalds',
        'a standard Linux kernel today has 10 million + lines of code',
        'Debian v4.0 source code has 283 million lines of code',
        'the Unix Epoch is marked Thursday, 1 January 1970',
        'braces expansion: $echo {one, two, three, four}fish --> onefish twofish etc...',
        'steps of the shell: prompt, parse, search, execute, nap, repeat',
        'want to see lots of tips? try $watch tips' 
       ]

if __name__ == '__main__':
  print; print random.choice(tips); print
  

