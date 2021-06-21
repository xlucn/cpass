from setuptools import setup

with open('Readme.md', 'r') as f:
    long_description = f.read()

with open('cpass', 'r') as f:
    for line in f.readlines():
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
    scripts=['cpass'],
    python_requires='>=3',
    install_requires=['urwid'],
    package_dir={"": "."},
    package_data={
        'cpass': ['LICENSE'],
    },
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
