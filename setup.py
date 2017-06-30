
from setuptools import setup

setup(
    name='backplate-auth',
    version='0.0.1',
    description='RESTful API Auth Helpers',
    author='Peter Boyer',
    author_email='petertboyer@gmail.com',
    url='https://github.com/studioarmix/backplate-auth',
    packages=['backplate_auth'],
    license='MIT',
    install_requires=[
        'flask',
        'flask-restful',
        'flask-cors'
    ]
)