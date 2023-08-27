from setuptools import find_packages, setup

# Load the README file.
with open(file='README.md', mode='r') as readme_handle:
    long_description = readme_handle.read()

# Load the __version__ script.
with open('./src/version.py', mode='r') as f:
    __version__ = exec(f.read())

setup(
    # Define the library name, this is what is used along with `pip install`.
    name = 'synt',

    # Define the author of the repository.
    author = 'Nelson A. Salazar Peña',

    # Define the Author's email, so people know who to reach out to.
    author_email = 'na.salazar10@uniandes.edu.co',

    # Define the version of this library.
    # Read this as
    #   - MAJOR VERSION 0
    #   - MINOR VERSION 1
    #   - MAINTENANCE VERSION 0
    version = __version__,

    # Here is a small description of the library. This appears
    # when someone searches for the library on https://pypi.org/search.
    description='',

    # I have a long description but that will just be my README
    # file, note the variable up above where I read the file.
    long_description=long_description,

    # This will specify that the long description is MARKDOWN.
    long_description_content_type='text/markdown',

    # Here is the URL where you can find the code, in this case on GitHub.
    url='https://github.com/salazarna/synthetic_irradiance',

    # These are the dependencies the library needs in order to run.
    install_requires=['folium==0.13.0',
                      'matplotlib==3.7.1',
                      'numpy==1.24.1',
                      'pandas==1.5.3',
                      'pvlib==0.9.4',
                      'scikit_learn==1.2.1',
                      'scipy==1.10.1',
                      'seaborn==0.12.2',
                      'statsmodels==0.13.5'],

    # Here are the keywords of my library.
    keywords=['synthetic data', 'solar radiation models', 'irradiance generation', 'stochastic modeling', 'clear-sky index', 'sky condition'],

    # here are the packages I want "build."
    packages=find_packages(include=['src', 'src.*']),

    # I also have some package data, like photos and JSON files, so
    # I want to include those as well.
    include_package_data=True,

    # Here I can specify the python version necessary to run this library.
    python_requires='>=3.10',

    # Additional classifiers that give some characteristics about the package.
    # For a complete list go to https://pypi.org/classifiers/.
    classifiers=[
        # I can say what phase of development my library is in.
        'Development Status :: 3 - Alpha',

        # Here I'll add the audience this library is intended for.
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',

        # Here I'll define the license that guides my library.
        'License :: OSI Approved :: MIT License',

        # Here I'll note that package was written in English.
        'Natural Language :: English',

        # Here I'll note that any operating system can use it.
        'Operating System :: OS Independent',

        # Here I'll specify the version of Python it uses.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',

        # Here are the topics that my library covers.
        'Topic :: Education',
        'Topic :: Office/Business',
        'Topic :: Scientific/Engineering']
)