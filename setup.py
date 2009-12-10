long_description = """sanctions - checking against EU senction lists.
"""

from setuptools import setup, find_packages

setup(name='sanctions',
      maintainer='Maximillian Dornseif',
      maintainer_email='md@hudora.de',
      version='1.0',
      description='checking against EU senction lists',
      long_description=long_description,
      classifiers=['License :: OSI Approved :: BSD License',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python'],
      download_url='https://cybernetics.hudora.biz/nonpublic/eggs/',
      zip_safe=False,
      packages=find_packages(),
      include_package_data=True,
      install_requires=['Django', 'hudoratools>=0.26']
)
