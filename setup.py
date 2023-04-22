from setuptools import setup, find_packages

with open("requirements.txt") as reqs:
    requirements = [line.strip() for line in reqs.readlines()]

setup(
    name='flowmapviz',
    version='0.1',
    packages=find_packages(),
    author='Pavlina Smolkova',
    author_email='smo0117@vsb.cz',
    description='Package for plotting routes',
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "flowmapviz-example = flowmapviz_example.slider:main"
        ]
    }
)
