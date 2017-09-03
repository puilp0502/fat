# Fake AP Toolkit
Fake AP Toolkit is a collection of script/program(s) to automate creating fake AP and proxy server.  

*tested under kali linux 2.0*  
# Dependencies
FAT Requires these programs to run properly:  
- hostapd  
- dnsmasq  

Optionally, If you want to run a proxy server, you need:  
- virtualenv  
- beef framework  

# Configuration
## Dnsmasq
Typically, you won't need to make any change(s) to dnsmasq.conf unless you want to change hosting interface.   
You can add hosts that you want to intercept requests to. You can do this by adding the host to fakehosts.conf.  

## Hostapd
Hostapd configuration file(hostapd.conf) is self-explanatory, so you can view and edit the configuration file.  
Also, you can see more configuration options at [here](https://w1.fi/cgit/hostap/plain/hostapd/hostapd.conf).  

## Proxy server
If you want to configure proxy server, you need two things: virtualenv and beef-framework.   
### virtualenv
if you have any experience in python, you'll know how to configure virtualenv. Just make a virtualenv at fakesite/venv.   
You'll also need two python libraries to be installed: requests and flask.

### BeEF Framework
We won't cover beef installation at this document; there are plentiful of documents out there.  
After you install beef, tell run.sh where beef script is located. Example location is /usr/share/beef-xss/beef.  

# Usage
If you don't want to run proxy server, run:  
>./run.sh  

If you do want to run proxy server, run:
>./run.sh runserver  
