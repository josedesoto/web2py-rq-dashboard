# web2py-rq-dashboard

`web2py-rq-dashboard` is a dashboard for monitoring RQ (Redis Queue) Python library for queueing jobs and processing them in the background. This app have been adapted to web2py from the original one `https://github.com/nvie/rq-dashboard` to make easier the integration with future web2py apps.

## It looks like this:

![](./static/images/rq1.png)

![](./static/images/rq2.png)


## Installing

### RQ library and redis:
```
pip install rq
apt-get install redis
```

### How to install the Dashboard in Linux, windows or Mac:

1- Download the last web2py version and unzip:
```
cd /opt
wget http://www.web2py.com/examples/static/web2py_src.zip
unzip web2py_src.zip
```

2- Download the app from github and move it into web2py framework:
```
cd /opt/web2py/applications
git clone https://github.com/josedesoto/monitor.git
```

3- Run web2py and ready to use it!!!
```
python /opt/web2py/web2py.py
```

4- Open the URL: http://localhost:8000/rq


For more info about rq library: `http://python-rq.org`
