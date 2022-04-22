# Copyright 2022 British Broadcasting Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="carbon-intensity-exporter",
    version="0.0.1",
    author="Iain McClenaghan",
    author_email="iain.mcclenaghan@bbc.co.uk",
    description="An API to find optimal times to do tasks based on when the grid is greenest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bbc/rd-carbon-minimiser",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=['pytest'],
    python_requires=">=3.6"
)