from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='tildejsongen',
    version='0.1.2',
    description='A sample Python project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dimension-sh/tildejsongen',
    author='Andrew Williams',
    author_email='andy@tensixtyone.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    py_modules=["tildejsongen"],
    python_requires='>=3.5, <4',
    install_requires=[],
    extras_require={
        'yaml': ['pyyaml'],
        'text': ['jinja2'],
    },
    entry_points={
        'console_scripts': [
            'tildejsongen=tildejsongen:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/dimension-sh/tildejsongen/issues',
        'Source': 'https://github.com/dimension-sh/tildejsongen/',
    },
)
