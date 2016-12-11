from distutils.core import setup
import py2exe

options = {"py2exe":{
					'includes': ['lxml.etree', 'lxml._elementpath', 'gzip'],
					"compressed": 1, # compress
                     "optimize": 2,  
                     "bundle_files": 1 # all to one exe
                     }}  

setup(
	console=[{"script": "NCUTSpider.py", "icon_resources": [(1, "ncutCourse.ico")]}
	],
	options=options,  
    zipfile=None,
    data_files=[(".", ["_config.ini", "readme.txt"])], 
)
