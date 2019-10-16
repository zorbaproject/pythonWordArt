from distutils.core import setup
setup(
  name = 'pythonWordArt',      
  packages = ['pythonWordArt'],   
  version = '0.1',     
  license='gpl-3.0',     
  description = 'Make WordArt, like the ones in MS Office, using Python3',  
  author = 'Luca Tringali',                  
  author_email = 'TRINGALINVENT@libero.it',    
  url = 'https://github.com/zorbaproject/pythonWordArt',   
  download_url = 'https://github.com/zorbaproject/pythonWordArt/archive/v0.1.tar.gz',    
  keywords = ['wordart', 'html2png', 'office'],   
  install_requires=[            
          'PySide2',
          'python-poppler-qt5',
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
