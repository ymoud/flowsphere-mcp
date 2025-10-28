"""
Setup script for FlowSphere MCP Server
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="flowsphere-mcp-server",
    version="1.0.0",
    author="Yannis Moudilos",
    author_email="jmoudilos@gmail.com",
    description="Generate production-ready test code from FlowSphere configurations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ymoud/flowsphere-mcp",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "flowsphere_mcp": [
            "templates/**/*.py",
            "templates/**/*.jinja2",
        ],
    },
    python_requires=">=3.10",
    install_requires=[
        "mcp>=0.1.0",
        "jinja2>=3.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "flowsphere-mcp=flowsphere_mcp.server:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="mcp flowsphere testing code-generation pytest jest behave bdd api-testing",
    project_urls={
        "Bug Reports": "https://github.com/ymoud/flowsphere-mcp/issues",
        "Source": "https://github.com/ymoud/flowsphere-mcp",
        "Documentation": "https://github.com/ymoud/flowsphere-mcp/blob/main/README.md",
    },
)
