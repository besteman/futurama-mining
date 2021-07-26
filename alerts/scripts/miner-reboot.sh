#!/usr/bin/expect -f
set miner [lindex $argv 0]
set timeout 60
spawn sshpass -f switch_password.txt ssh switch.home.schrauger.com:10022
expect "Switched CDU: "
send "reboot $miner\r"
expect "Switched CDU: "
send "exit\r"
expect eof
