import setuptools
import sensor_client

setuptools.setup(
    name='rpi-gpio-sensor-monitor',
    version=sensor_client.version,
    packages=setuptools.find_packages(),
    url='',
    license='',
    maintainer='Jorge Lopes',
    maintainer_email='jorgedclopes@gmail.com',
    author='Jorge Lopes',
    author_email='jorgedclopes@gmail.com',
    description='Monitoring tool for RPi + circuit to display using a Grafana Dashboard.',
    include_package_data=True
)
