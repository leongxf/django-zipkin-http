from django_zipkin_http import __version__
from setuptools import find_packages, setup

setup(
    name='django-zipkin-http',
    version=__version__,
    description='django-zipkin-http is a Django middleware and api refering to django-zipkin for recording and sending messages to Zipkin via HTTP protocol',
    author='Leon Guo',
    author_email='934214227@qq.com',
    url='https://github.com/leongxf/django-zipkin-http',
    packages=find_packages(),
    keywords='django zipkin middleware http',
    platforms=['any'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Freely Distributable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
