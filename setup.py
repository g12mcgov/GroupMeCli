#!/usr/local/bin/python

## 
## Created by: Grant McGovern 
## Date: 18 July 2014 
## Purpose: Setup environment for GroupMeCli.
## 

from setuptools import setup, find_packages

setup(name = 'GroupMeCli',
	version = '0.1a',
	description = 'A command line client for GroupMe!',
	author = 'Grant McGovern',
	author_email = 'grantmcgovern.mcgovern@gmail.com',
	install_requires = [
		'requests',
		'termcolor',
		'prettytable',
	]
)
