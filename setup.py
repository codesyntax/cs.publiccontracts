from setuptools import find_packages
from setuptools import setup

import os

long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


version = "2.0dev"

setup(
    name="cs.publiccontracts",
    version=version,
    description="Public Contracs Product",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="",
    author="Lur Ibargutxi",
    author_email="libargutxi@codesyntax.com",
    url="https://github.com/codesyntax/cs.publiccontracts",
    license="GPL",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["cs"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "plone.app.dexterity",
        "plone.namedfile",
        "collective.z3cform.datagridfield",
        "z3c.unconfigure",
        "collective.dexteritytextindexer",
        "Plone > 4.99"
        # -*- Extra requirements: -*-
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
