from setuptools import setup, find_packages



core_requirements = [
    "pyrep @ git+https://github.com/stepjam/PyRep.git",
    "numpy",
    "Pillow",
    "pyquaternion",
    "scipy",
    "natsort"
]

setup(name='harmful_rlbench',
      version="0.1.0",
      description='Harmful RLBench',
      install_requires=core_requirements,
      packages=find_packages(),
      include_package_data=True,
      extras_require={
        "gym": ["gymnasium==1.0.0a2"],
        "dev": ["pytest"]
      },
)