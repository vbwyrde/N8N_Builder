from setuptools import setup, find_packages

with open("README_public.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements_public.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="n8n-builder-community",
    version="1.0.0",
    author="VBWyrde",
    author_email="31293466+vbwyrde@users.noreply.github.com",
    description="AI-powered workflow automation system that converts plain English to n8n workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vbwyrde/N8N_Builder",
    packages=find_packages(exclude=["Enterprise_Module*", "Enterprise Module*", "Enterprise_Database*", "advanced_systems*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-asyncio>=0.23.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "n8n-builder=n8n_builder.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "n8n_builder": ["templates/*.json", "static/*"],
    },
)
