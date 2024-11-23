from setuptools import setup, find_packages

setup(
    name='web_elements_handler',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'selenium',
    ],
    description='Модуль для продвинутого поиска элементов страницы через Selenium по множеству локаторов.'
                'А также для эмуляции движения и клика мыши по элементу с помощью ActionChains.',
    author='cherseroff',
    author_email='proffitm1nd@gmail.com',
    url='https://github.com/cherseroff27/web_elements_handler.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)