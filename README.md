# trebuchet.py

Trebuchet.py lets you send files to other computers on your LAN.  It requires Python 2.

Usage:

```
$ ./trebuchet.py send file.txt
$ ./trebuchet.py recv file.txt
```

## Caveats
Trebuchet.py may or may not work due to UDP broadcast issues.

(If you know of a better way to send broadcast packets in Python, please send a pull request.)
