from setuptools import setup, find_packages

setup(
    name='module-web_element_handler',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'selenium',
    ],
    description='Модуль для продвинутого поиска жлемента через Selenium по множеству локаторов.'
                'А также для эмуляции движения и клика мыши по элементу с помощью ActionChains.',
    author='cherseroff',
    author_email='proffitm1nd@gmail.com',
    url='https://github.com/cherseroff27/module-web_element_handler.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)