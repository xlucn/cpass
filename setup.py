from setuptools import setup

with open('Readme.md', 'r') as f:
    long_description = f.read()

for line in open('cpass.py', 'r'):
    if line.startswith('version'):
        version = line.split('=')[1].strip(' \"\'\n')
        break

setup(
    name='cpass',
    version=version,
    description='A TUI for pass, the standard Unix password manager',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author='Lu Xu',
    author_email='oliver_lew@outlook.com',
    url='https://github.com/OliverLew/cpass',
    # Single-file module and a console script
    py_modules=['cpass'],
    entry_points={
        'console_scripts': [
            'cpass = cpass:main',
        ],
    },
    python_requires='>=3',
    install_requires=['urwid'],
    data_files=[('share/doc/cpass', [
        'cpass.cfg',
        'CHANGELOG',
        'Readme.md',
    ])],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)
