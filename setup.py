from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mtn_ngs/__init__.py
from mtn_ngs import __version__ as version

setup(
	name="mtn_ngs",
	version=version,
	description="Mtn Ngs ",
	author="Ahmed Osama",
	author_email="ahmedosama.dev@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
