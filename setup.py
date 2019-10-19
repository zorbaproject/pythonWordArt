from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
myversion = '0.4'
setup(
  name = 'pythonWordArt',      
  packages = ['pythonWordArt'],   
  version = myversion,     
  license='gpl-3.0',     
  description = 'Make WordArt, like the ones in MS Office, using Python3', 
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Luca Tringali',                  
  author_email = 'TRINGALINVENT@libero.it',    
  url = 'https://github.com/zorbaproject/pythonWordArt',   
  download_url = 'https://github.com/zorbaproject/pythonWordArt/archive/v'+myversion+'.tar.gz',    
  keywords = ['wordart', 'html2png', 'office'],  
  include_package_data=True,
  install_requires=[            
          'PySide2',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Developers',   
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  
    'Programming Language :: Python :: 3',   
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
