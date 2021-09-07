---
layout: post
title: "Solaris RAD With Python"
date: 2021-09-07
categories: [computing]
tags: [solaris, rad, python]
image: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Aktualne_logo_Oracle_Solaris_OS_OSos.png/250px-Aktualne_logo_Oracle_Solaris_OS_OSos.png"
excerpt_separator: <!--more-->
---

Continuing my experiments with [Solaris
RAD](https://docs.oracle.com/cd/E37838_01/html/E68270/gmfhf.html), I wanted to
validate some of the work in the [Solaris blog
post](https://blogs.oracle.com/solaris/managing-oracle-solaris-through-rest)
that uses the [python requests library](https://docs.python-requests.org/) to
authenticate to a Solaris zone and grab some SMF info.

<!--more-->

## Some Notes on the Orginal Script

Looking at the original script in the blog post, it is pretty slick. My
challenge is that I am behind the curve on REST programming in general! I
have a fairly basic grasp of python, but lack fundamentals on the requests
library. Here are some of my notes (a little random, but I think it is
illuminating as to how this stuff works):

- There is an `import requests` line at the top of the script, which I
  get (you need a package to make the http REST call). But why the `with
  requests.Session() as s` statment? Why bother with a _session_? (Line 17 in
  the script)  

  Answer: According to the
  [request docs](https://docs.python-requests.org/en/master/user/advanced/#session-objects)
  this allows cookies to persist between requests and re-uses the same TCP
  connection. The `with` keyword makes it a context manager and will make sure
  the session is closed as soon as the with block is exited, even if unhandled
  exceptions occurred.
  
- The zone is using a self-signed certificate for `https` connections. The
  client is a Mac. I could not get the blog post script to work initially.

  Answer: The blog post line of code:
  ```python
  r = s.post(login_url, json=config_json, verify='host.crt')
  ```

  Resulted in the following exception:

  ```python
  requests.exceptions.SSLError: 
  HTTPSConnectionPool(host='balder.norsestuff.com', port=6788): 
  Max retries exceeded with url: 
  /api/authentication/1.0/Session (Caused by
  SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED]
  certificate verify failed: unable to get local issuer certificate
  (_ssl.c:1108)')))
  ```

  After doing some research, I determined I needed to grab the zone's CA file:

  ```bash
  pwd
  /Users/jameshall/mysrc/python/solaris/rad/balder/CA
  scp backdoor@balder:/etc/certs/localhost/host-ca/hostca.crt .
  ```

  Then run the following `openssl` command in order to create the proper symlinks:

  ```bash
  ln -s hostca.pem `openssl x509 -hash -noout -in hostca.pem`.0
  ```

  Then I modified the script with a new post command using the path to the
  hostca file for the `verify` option:

  ```python
  r = s.post(login_url, json=config_json, verify='/Users/jameshall/mysrc/python/solaris/rad/balder/CA')
  ```

- How do you inspect the cookie that comes back? I was hoping that I could
  simply say `print(s.cookies.__dict__[blah])`, but not so much. Exploring the
  data structure got borked at the Cookie object.

  Answer: [https://docs.python-requests.org/en/master/api/#cookies](https://docs.python-requests.org/en/master/api/#cookies)

  ```python
  requests.utils.dict_from_cookiejar(s.cookies)
  ```
 
  and a little deeper into the structure:

  ```python
  requests.utils.dict_from_cookiejar(s.cookies)['_rad_instance']
  ```

  Sample API call and output:

  ```python
  requests.utils.dict_from_cookiejar(s.cookies)
  ```
  ```bash
  {'_rad_instance': '8960', '_rad_token': 'c2890180-7e70-42b0-a80f-b676161df99f'}
  ```

- How do you capture request status

  Answer: The [json](https://docs.python.org/3/library/json.html#module-json)
  package is needed. Add this line to the script:

  ```python
  >>> r.text
  '{\n        "status": "success",\n        "payload": "ONLINE"\n}'
  >>> bar = json.loads(r.text)
  >>> bar['status']
  'success'
  ```

- Tried to GET an SMF service that had a list of instances. Found
  `svc:/system/identity` had five instances:

  ```python
  query_url1 = "https://balder.norsestuff.com:6788/api/com.oracle.solaris.rad.smf/1.0/Service/system%2Fidentity/instances"
  ```
  This returns the following:

  ```bash
  The status code is: 200
  The return text is: {
          "status": "success",
          "payload": [
                  "cert",
                  "cert-expiry",
                  "domain",
                  "node",
                  "version"
          ]
  }
  ```

- An aside: Here is a code fragment  on exploring the session data structure
  which led to me determing that I needed to get further data about the
  session cookie via the `requests` API (see above).

  ```python
  >>> s.cookies.__dict__['_cookies']['balder.norsestuff.com']['/api']['_rad_instance']
  Cookie(version=0, name='_rad_instance', value='3840', port=None,
  port_specified=False, domain='balder.norsestuff.com',
  domain_specified=False, domain_initial_dot=False, path='/api',
  path_specified=True, secure=False, expires=1630617493, discard=False,
  comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
  ```

## Conclusion

It looks like I can run some slightly modified python code from a Mac client
and:

- Create a secure connection from the client by adding the hostca self-singed
  cert to the `verify` option.

- Manipulate the returned data structures to tell if the connection
  authenticated successfully.

- Inspect the cookies associated with the connection.

  Looks like there is a path to using this for Django authentication.

## Appendix: Modified blog post script

<script src="https://gist.github.com/jimhall/f8c08b94dbbe96cde0efc07ad712a69a.js"></script>
