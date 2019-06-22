from setuptools import setup


setup(
    name='cec_backend_python',
    version='0.0.2',
    packages=['cec_backend_python'],
    description='CEC Backend Python API client',
    author='Kyriakos Toumbas',
    author_email='kyriakos@pixelactions.com',
    url='https://github.com/PixelActions/cec_backend_python',
    install_requires=['requests >= 2.2.1'],
    license='http://opensource.org/licenses/MIT',
    #test_suite='tests',
    classifiers=(
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
    keywords='cec_backend api'
)
