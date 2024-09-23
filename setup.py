from setuptools import setup, find_packages

setup(
    name="cluster_tool",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=7.0",
        "Jinja2>=2.11",
    ],
    entry_points={
        "console_scripts": [
            "provisioner=provisioner.provisioner:create_cluster",
        ],
    },
    author="Harsha Vardhan",
    author_email="harshavardhan.workspace@gmail.com",
    description="A platform automation tool for Data Engineering dev environment. Provision and scale local development clusters using VMs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/harshavardhaSDE/oneData",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
