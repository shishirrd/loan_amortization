from setuptools import setup

setup(
	name='emi_table_streamlit_app',
	author = 'Shishir Deshpande',
	packages = ['emi_table',],
	package_dir = {'emi_table':'emi_table',},
	package_data = {'emi_table':['mappings/*.csv','sql/*.txt']},
	version='1.0.0',
	description = 'library to help create a loan amortization table',
	install_requires=[
        'pandas',
    ],
)
