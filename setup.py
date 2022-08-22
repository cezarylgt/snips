from setuptools import setup, find_packages

setup(
    name='snips',
    packages=find_packages(),
    version='0.0.1',
    install_requires=[
        'typer',
        'pyperclip',
        'rich',
        'tinydb',
        'pydantic',
        'python-dotenv',
        'pyyaml'
    ],
    package_data={'': ['../.env', '../snp.sh']},
    include_package_data=True,
    entry_points='''
        [console_scripts]
        snp=snips.app:app
    '''
)

# todo:
#   use injector
#   ls with search option
#   console logger - loging info (messages to user)
#   themes:
#       theme as domain object
#       theme cli
