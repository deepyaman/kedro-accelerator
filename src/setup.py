# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

from inspect import getdoc
from pathlib import Path

from setuptools import find_packages, setup

import kedro_accelerator

setup(
    name="kedro-accelerator",
    version=kedro_accelerator.__version__,
    description=getdoc(kedro_accelerator).partition("\n")[0],
    long_description=(Path(__file__) / "../../README.md").resolve().read_text("utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/deepyaman/kedro-accelerator",
    author="Deepyaman Datta",
    author_email="deepyaman.datta@utexas.edu",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Kedro",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="kedro",
    packages=find_packages(include=["kedro_accelerator.plugins"]),
    entry_points={
        "kedro.hooks": ["kedro-accelerator = kedro_accelerator.plugins:hooks"]
    },
    python_requires=">=3.6, <3.9",
    install_requires=["kedro>=0.16, <0.18"],
    extras_require={
        "docs": [
            "sphinx>=1.6.3, <2.0",
            "sphinx_rtd_theme==0.4.1",
            "nbsphinx==0.3.4",
            "nbstripout==0.3.3",
            "recommonmark==0.5.0",
            "sphinx-autodoc-typehints==1.6.0",
            "sphinx_copybutton==0.2.5",
            "jupyter_client>=5.1.0, <6.0",
            "tornado>=4.2, <6.0",
            "ipykernel>=4.8.1, <5.0",
        ]
    },
)
