#!/bin/sh
export LANG="en_EN.UTF-8"
export LC_COLLATE="en_EN.UTF-8"
export LC_CTYPE="en_EN.UTF-8"
export LC_MESSAGES="en_EN.UTF-8"
export LC_MONETARY="en_EN.UTF-8"
export LC_NUMERIC="en_EN.UTF-8"
export LC_TIME="en_EN.UTF-8"
export LC_ALL=

python -c 'import locale; print(locale.getdefaultlocale());'
echo ales gut.

