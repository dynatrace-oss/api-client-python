from setuptools import setup, find_packages

setup(
    name="dt",
    version="1.1.37",
    packages=find_packages(),
    install_requires=["requests>=2.22"],
    tests_require=["pytest", "mock", "tox"],
    python_requires=">=3.6",
    author="David Lopes",
    author_email="davidribeirolopes@gmail.com",
    description="Dynatrace API Python client",
    long_description="Dynatrace API Python client",
    url="https://github.com/dlopes7/dynatrace-rest-python",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: Apache Software License",  # 2.0
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development",
    ],
    project_urls={"Issue Tracker": "https://github.com/dlopes7/dynatrace-rest-python/issues"},
)
