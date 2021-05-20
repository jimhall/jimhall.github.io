---
layout: post
title: "Using Kerberos Authentication With RAD"
date: 2021-05-20
categories: [computing]
tags: [solaris, rad, kerberos, ldap]
image: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Aktualne_logo_Oracle_Solaris_OS_OSos.png/250px-Aktualne_logo_Oracle_Solaris_OS_OSos.png"
excerpt_separator: <!--more-->
---

I am considering doing some experiments with [Solaris
RAD](https://docs.oracle.com/cd/E37838_01/html/E68270/gmfhf.html) with [LDAP
naming services](https://docs.oracle.com/cd/E37838_01/html/E61012/index.html)
and use it as a foundation for application authentication using using
[Kerberos](https://docs.oracle.com/cd/E37838_01/html/E61026/index.html).

<!--more-->

This post is a quick proof of concept and allowing me to kind of kick off my
documentation process. Given that I have successfully configured Kerberos and
LDAP on Solaris 11.4 I wanted to validate the following:

## High Level Steps

- Create a user in LDAP called `jhall` and using [per-user PAM](https://docs.oracle.com/cd/E37838_01/html/E61023/rbacref-6.html#OSSUPrbacref-10) and setting pam_policy in `user_attr` to [krb5_only](https://docs.oracle.com/cd/E88353_01/html/E37853/pam-user-policy-7.html#REFMAN7pam-user-policy-7)

- Create a Kerbros principal of the same name (jhall@norsestuff.com) with a
homedir on a kerberos protected NFS share

- On my Mac, follow the steps in [this Solaris blog post](https://blogs.oracle.com/solaris/managing-oracle-solaris-through-rest) and use the curl commands in the blog post to login and use the SMF RAD API command.

- Monitor Solaris Audit in the global zone and observe the RAD login is
recorded in the audit record (and note the format).

## Detailed Steps

### Record of RAD authentication (curl commands run on my Mac)

- Curl command in the blog post:

```bash
curl -c cookie.txt -X POST --cacert host.crt --header 'Content-Type:application/json' --data '@login.json' https://balder.norsestuff.com:6788/api/authentication/1.0/Session/
```

- JSON fragment `login.json` that has the authentication information for the
jhall LDAP user // kerberos principal:

```json
{
  "username": "jhall",
  "password": "<kerberos password>",
  "scheme": "pam",
  "preserve": true,
  "timeout": -1
}
```

- Running the curl command results in the following expected result, matching
the blog post:

```json
{
        "status": "success",
        "payload": {
                "href": "/api/com.oracle.solaris.rad.authentication/1.0/Session/_rad_reference/3328"
        }
}
```

- Below is the audit record for the authentication. Note it shows the service
used to connect (RAD), the user (jhall), group (staff), session id
(2004100041), and terminal id / IP address connecting from (54270 6788
::ffff:10.0.0.69):

```csv
header,101,2,connect to RAD,,balder,2021-05-13 21:32:53.841-04:00
subject,jhall,jhall,staff,jhall,staff,0,2004100041,54270 6788 ::ffff:10.0.0.69
return,success,0
```

### Use generated cookie to run the SMF command in the blog post

(modified for my environment):

```bash
curl -b cookie.txt --cacert host.crt -H 'Content-Type:application/json' -X GET https://balder.norsestuff.com:6788/api/com.oracle.solaris.rad.smf/1.0/Service/system%2Frad/instances
```

- Output returned similar to the blog post:

```json
{
        "status": "success",
        "payload": [
                "local",
                "remote"
        ]
}
```

- Generated audit log (2 records this time; connection then logout):

```csv
header,101,2,connect to RAD,,balder,2021-05-13 21:32:59.520-04:00
subject,jhall,jhall,staff,jhall,staff,0,1530906022,54271 6788 ::ffff:10.0.0.69
return,success,0
header,101,2,logout,,balder,2021-05-13 21:32:59.598-04:00
subject,jhall,jhall,staff,jhall,staff,0,1530906022,54271 6788 ::ffff:10.0.0.69
return,success,0
```

### Use generated cookie again for second SMF RAD command in blog post:

```bash
curl -b cookie.txt --cacert host.crt -H 'Content-Type:application/json' -X GET https://balder.norsestuff.com:6788/api/com.oracle.solaris.rad.smf/1.0/Instance/system%2Frad,remote/state
```

- Again, good output is similar to the blog post:

```json
{
        "status": "success",
        "payload": "ONLINE"
}
```

- Generated audit log (Again, 2 records this time; connection then logout):

```csv
header,101,2,connect to RAD,,balder,2021-05-13 21:36:06.090-04:00
subject,jhall,jhall,staff,jhall,staff,0,1482710200,54314 6788 ::ffff:10.0.0.69
return,success,0
header,101,2,logout,,balder,2021-05-13 21:36:06.098-04:00
subject,jhall,jhall,staff,jhall,staff,0,1482710200,54314 6788 ::ffff:10.0.0.69
return,success,0
```

## Conclusion

This worked out well. I was able to use RAD to authenticate to a non-root user. The fact that I was using kerberos in the PAM stack was "no big deal". This will allow me to proceed with further validation that I can use this mechanism as a web based authentication method for applications.

### Reference // Appendix

- Here is an audit record of SSH Login:

```csv
header,85,2,login - ssh,,balder,2021-05-13 21:44:25.705-04:00
subject,jhall,jhall,staff,jhall,staff,6423,1118693340,54412 22 10.0.0.69
return,success,0
```

- Here is how to modify per zone audit policy. Necessary since I am doing
RAD auth in local zone and wanted to disambiguate what zone is being connected
to (without this, the audit records are written to the global zone audit log
stating the connection is from the global zone host):

```bash
# auditconfig -getpolicy -t
active audit policies = argv,cnt
# auditconfig -setpolicy +perzone
# auditconfig -getpolicy -t
active audit policies = argv,cnt,perzone
# svcadm enable auditd
```

- Here is a command to tail the latest audit log file to monitor activity in
real time:

```bash
# tail -0f $(find /var/share/audit -name $(ls -rt /var/audit | tail -1)) | praudit -x
```

