Screenlock Builder Docker Image
===

This docker image uses wine and pyinstaller to build the screenlock application for windows.
It is based on the wine docker image that is built using the included Dockerfile.

The only changes made to the docker image after installing wine were manual
installations of python and python libraries for building the app.  Those are not
included here to save space.  

Download:
---
http://www.nanofab.utah.edu/sv/?dec=1&cat=Computer%20Passwords&t1=Prerequisites%20For%20Screenlock%20Build&t2=

Import:
---
```
docker import - screenlock-builder:2 < docker-screenlock-builder-2.tar
```

Run:
---
Assuming the screenlock source parent directory is "~/dev/screenlock-package":

```
docker run -u developer  -it -v ~/dev/screenlock-package/:/slock screenlock-builder:2 bash -c 'cd /slock/screenlock && wine python /slock/screenlock/setup.py'
```
