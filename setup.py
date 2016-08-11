from setuptools import setup

setup(name='sqlcrush',
        version='0.1.2',
        description='console based database editor',
        url='http://github.com/coffeeandscripts/sqlcrush',
        author='coffeeandscripts',
        author_email='ersari94@gmail.com',
        license='GNU',
        scripts=['bin/sqlcrush',],
        packages=['sqlcrush',],
        install_requires=['sqlalchemy',],
        include_package_data=True
)
