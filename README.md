RunRes
======
A small utility to run an application using the specified resolution. After the application ends, the resolution
will automatically revert to the default.

This was developed to make it easier for my children to play old games that require specific resolutions and has
currently been tested on the 32 bits version of Windows 7.

Usage:
runres.exe <width> <height> path

Example:
To run notepad in 800x600 use:
    runres.exe 800 600 %windir%\notepad.exe
