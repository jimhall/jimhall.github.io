---
layout: post
title: "SSH X Display Issue With OEL 7"
date: 2020-07-29
categories: [computing]
tags: [linux, oel, ssh, x11]
image: "https://news-cdn.softpedia.com/images/news2/oracle-enterprise-linux-7-5-debuts-with-unbreakable-enterprise-kernel-release-4-520750-2.jpg"
excerpt_separator: <!--more-->
---

I was trying out one of Oracle's VirtualBox images that allow you to try 
the database and key features and tools. The image I had laying around was a
couple of years old running OEL 7. I found I could not X display one of the
tools (SQL Developer) back to my Mac desktop. This is how I investigated the
issue and fixed it.

<!--more-->

I have Apple's [Xcode](https://developer.apple.com/xcode/) on my Macbook Pro,
which includes an X server, [XQuartz](https://www.xquartz.org). I have used it
successfully many times, but I was finding when I ssh'd into the OEL 7
virtualbox host, the ssh client on my Mac would complain with `X11 forwarding
request failed on channel 0`. 

I tried to run ssh in debug mode using `ssh -vvv <host>`, but all it reported
was the same error message without verbose debugging on and the Google
machine was not coming up with anything relevant. So then on the OEL host I
ran a separate sshd server using the command `/usr/sbin/sshd -d -p 2222`. On
the Mac I ran the client as `ssh -p 2222 <user@host>`. The debug ssh server on
the OEL host then printed the following error messages:

```bash
debug1: session_input_channel_req: session 0 req x11-req
Failed to allocate internet-domain X11 display socket.
debug1: x11_create_display_inet failed.
```

Plugging the string `Failed to allocate internet-domain X11 display socket` into
Google pointed me to the following [Red Hat
Bugzilla entry](https://bugzilla.redhat.com/show_bug.cgi?id=1027197). Per the
recommendation in the bug report I changed the `AddressFamily` default of
`any` to `inet` in `/etc/ssh/sshd_config`. I restarted the ssh service using the [proper systemctl
command](https://globedrill.com/how-to-start-stop-restart-ssh-service-on-centos-7-redhat-7-servers/)
using `systemctl restart sshd.service` and go figure X displaying applications
to my Mac work now. 

What seems strange to me is that this bug seems to have been filed and fixed
with OpenSSH 5.3 and identified as an issue in RH 6 back in 2014. I am running
an equivalent to RH 7 and OpenSSH 7.4, but the `AddressFamily any` is still
the default in `/usr/ssh/sshd_config` file and *still* breaks X displaying applications. 

My Linux-fu is too weak to sort out when `AddressFamily any` does not break X
displaying applications. Although I do not appear to be alone as to asking [why
this is still
broken](https://unix.stackexchange.com/questions/470905/why-addressfamily-needs-to-be-configured-for-x11-forwarding).
