from setuptools import find_packages, setup
from typing import List

Hyphen='-e .'
def requirements_needed(file_path:str)->List[str]:
    '''
       this will return list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]
    
        if Hyphen in requirements:
            requirements.remove(Hyphen)
    return requirements

setup(
    name='mlproject',
    version='0.0.1',
    author="b3yotch",
    author_email='vaibhavpandey4022003@gmail.com',
    packages=find_packages(),
    install_requires=requirements_needed('requirements.txt')
)