from setuptools import setup, find_packages

setup(
    name='sabo',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # add settings
    ],
    entry_points={
        'console_scripts': [
            'sabo = sabo.cli:main'
        ]
    },
    python_requires='>=3.10',
    description='Sabo - minimal Python site builder framework',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/emizhaa/sabo',
    author='emizhaa',
    author_email='emizhaa@gmail.com',
    license='MIT',
)