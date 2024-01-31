from setuptools import setup, find_packages

setup(
    name='cow_shed',
    version='1.0.0',
    author='Sagarnil',
    description='FastAPI project deployed on Azure clude with Azure function',
    packages=find_packages(),
    install_requires=[
        'fastapi[all]',
        'fastapi-sqlalchemy',
        'pydantic',
        'python-dotenv',
        'psycopg2-binary'
    ],
    package_data={
        # Include any additional files needed by your package
        '': ['*.json', '*.env', '*.md'],
    },
)
