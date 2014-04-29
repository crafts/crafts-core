from setuptools import setup, find_packages

setup(
    name='CRAFTS',
    version='0.1',
    description='A predictive scaling framework',

    author='Andrew Guenther',
    author_email='guenther.andrew.j@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Systems Administration'
    ],

    keywords='scaling operations devops aws',

    install_requires=['requests', 'python-daemon'],

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'craftsd = crafts.craftsd:run'
        ]
    }
)
