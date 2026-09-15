from setuptools import find_packages, setup

package_name = 'turtlesim_catch_them_all'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Manit Singh Bhatia',
    maintainer_email='manitsingh57@gmail.com',
    description='Spawner and proportional controller nodes that hunt down randomly-spawned turtlesim turtles',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "controller = turtlesim_catch_them_all.turtle_controller:main",
            "spawner = turtlesim_catch_them_all.turtle_spawner:main"
        ],
    },
)
