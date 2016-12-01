# django-zipkin-http
This is a django zipkin middleware, send information to zipkin
via HTTP protocol. Referring to [django-zipkin](https://github.com/prezi/django-zipkin)

**django-zipkin-http** is a middleware for django to send report
to [Zipkin](http://twitter.github.io/zipkin/). It can be used as
some kind of HTTP client*(or reporter)* for Zipkin.

You can eithor report issues on github, or contact me at
934214227@qq.com. Suggestions and issues are most welcomed! 

## How to install 
---

* Pip

    ``` Pip install django-zipkin-http```
    
* setup.py

    1. Clone the project or download from [Pypi](https://pypi.python.org/pypi/django-zipkin-http)
    2. Unzip the package then ``` python setup.py install ```
    
## Settings
---
1. Add middleware in middleware classes

    ```
    MIDDLEWARE_CLASSES = (
        ...
        'django_zipkin_http.middleware.ZipkinMiddleware',
        ...
    )
    ```

2. Add zipkin host

    settings.py
    
    ```
    ZIPKIN_HTTP_HOST = "http://host:port"
    ```
    
3. Optional configuration

    ```
    ZIPKIN_HTTP_API = "/api/v1/"
    ZIPKIN_HTTP_SPAN = "/span/" # span uploading uri
    ZIPKIN_SERVICE_NAME = "HTTP-service" # service name shows in zipkin
    ```
    
# Demo
---
**To be done :P**     
