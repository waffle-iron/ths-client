from setuptools import setup

setup(
    name='ths-client',
    packages=['ths-client'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-assets',
        'flask-login',
        'flask-sqlalchemy',
    ]
)
