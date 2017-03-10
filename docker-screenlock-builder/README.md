Screenlock Builder Docker Image
===

This docker image uses wine and pyinstaller to build the screenlock application for windows.
It is based on the wine docker image that is built using the included Dockerfile.

The only changes made to the docker image after installing wine were manual
installations of python and python libraries for building the app.  Those are not
included here to save space.  

Download:
---
https://hub.docker.com/r/saltlakeryan/xvfb-wine-python/

Import:
---
```
docker pull saltlakeryan/xvfb-wine-python
```

Run:
---
Assuming the screenlock source directory is "~/dev/screenlock":

```
sudo docker run -u developer  -it -v ~/dev/screenlock:/screenlock saltlakeryan/xvfb-wine-python bash -c 'cd /screenlock && wine c:/Python27/python /screenlock/setup.py'

```
