import setuptools

setuptools.setup(
    name="kt_tv_ch",
    version="0.5",
    url="https://github.com/jinniahn/kt_tv_ch",

    author="jinsub ahn",
    author_email="jinniahn@gmail.com",

    description="extracting tv channel information for web",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    entry_points = {
        'console_scripts': ['kt_tv_export=kt_tv_ch.db_export:main']
    }

    install_requires=[
        'requests','pyquery'
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
