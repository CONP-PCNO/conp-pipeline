import sys
from setuptools import setup
import sys

VERSION = "0.1"
DEPS = [ "clowdr", "datalad" ]

setup(name="conp-pipeline",
      version=VERSION,
      description="Pipeline management tool for CONP",
      url="http://github.com/CONP-PCNO/conp-pipeline",
      author="CONP developers",
      classifiers=[
                "Programming Language :: Python",
                "Programming Language :: Python :: 2",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 2.6",
                "Programming Language :: Python :: 2.7",
                "Programming Language :: Python :: 3.4",
                "Programming Language :: Python :: 3.5",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "Programming Language :: Python :: Implementation :: PyPy",
                "License :: OSI Approved :: MIT License",
                "Topic :: Software Development :: Libraries :: Python Modules",
                "Operating System :: OS Independent",
                "Natural Language :: English"
                  ],
      license="MIT",
      packages=["conp-pipeline"],
      include_package_data=True,
      test_suite="pytest",
      tests_require=["pytest"],
      setup_requires=DEPS,
      install_requires=DEPS,
      entry_points={
        "console_scripts": [
            "conp-pipeline=main:main",
        ]
      },
      zip_safe=False)
