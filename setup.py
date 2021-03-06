import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="emotions-comparison-dyaroshevych",  # Replace with your own username
    version="0.0.1",
    author="Dmytro Yaroshevych",
    author_email="dyaroshevych@gmail.com",
    description="A package for comparing emotions in books and films",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dyaroshevych/emotions-comparison",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    packages=["emotions_comparison"],
    package_dir={"emotions_comparison": "emotions_comparison"},
    include_package_data=True
)
