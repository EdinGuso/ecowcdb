from setuptools import setup

setup(
    name="ecowcdb",
    version="1.0.0",
    author="Edin Guso",
    author_email="edin.guso@epfl.ch",
    license="MIT",
    description="Efficient Computation of Worst-Case Delay-Bounds for Time-Sensitive Networks",
    packages=[
        "ecowcdb",
        "ecowcdb.util",
        "ecowcdb.panco",
        "ecowcdb.panco.fifo",
        "ecowcdb.panco.descriptor",
    ],
    install_requires=["numpy", "tabulate", "tqdm", "scipy"],
    python_requires=">=3.10",
    package_data={'': ['lp_solve']},
    include_package_data=True,
    url="https://github.com/EdinGuso/ecowcdb"
)