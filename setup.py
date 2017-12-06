from setuptools import setup
import platform, warnings

#Pypy dependency support
python_implementation = platform.python_implementation()

install_requires = ['sqlalchemy', 'pymysql', 'psycopg2',]
if python_implementation == "PyPy":
    install_requires = ['sqlalchemy', 'pymysql', 'psycopg2cffi',]
elif python_implementation != "CPython":
    warnings.warn("We don't know how to deal with the {} runtime. Treating it like CPython".format(python_implementation), RuntimeWarning)

setup(name='sqlcrush',
        version='0.1.5',
        description='console based database editor',
        url='http://github.com/coffeeandscripts/sqlcrush',
        author='coffeeandscripts',
        author_email='ersari94@gmail.com',
        license='GNU',
        scripts=['bin/sqlcrush',],
        packages=['sqlcrush',],
        install_requires=install_requires,
        include_package_data=True
)
