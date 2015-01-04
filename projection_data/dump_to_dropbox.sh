#!/bin/bash 
set -e

DROPDUMP='dump'
INDBF='out.dbf'
OUTDBF='projection_data_20150103.dbf'
FIG='figs.*'

if [ ! -d ~/Dropbox/$DROPDUMP ]
then
    mkdir ~/Dropbox/$DROPDUMP
fi

cp shps/$INDBF ~/Dropbox/$DROPDUMP/$OUTDBF
cp shps/$FIG ~/Dropbox/$DROPDUMP/
