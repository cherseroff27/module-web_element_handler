from setuptools import setup, find_packages

setup(
    name='module-web_element_handler',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'pyperclip',
        'browser_manager @ git+https://github.com/cherseroff27/module-browser_manager.git',
        'browser_manager @ git+https://github.com/cherseroff27/module-web_element_handler.git',
        'browser_manager @ git+https://github.com/cherseroff27/module-manual_script_control.git',
    ],
    description='Генерация комментариев через ChatGPT.'
                '(Предполагается автоматизация с помощью модуля browser_manager,'
                'использующего selenium, undetected_chromedriver).',
    author='cherseroff',
    author_email='proffitm1nd@gmail.com',
    url='https://github.com/cherseroff27/module-web_element_handler.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)