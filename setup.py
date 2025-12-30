from setuptools import setup
from setuptools.command.build_py import build_py
import subprocess
from pathlib import Path

class BuildWithResources(build_py):
    def run(self):
        resources_dir = Path("data/resources")
        xml = resources_dir / "resources.gresource.xml"

        subprocess.check_call([
            "glib-compile-resources",
            str(xml),
            "--target",
            str(resources_dir / "resources.gresource"),
            "--sourcedir",
            str(resources_dir),
        ])

        super().run()

setup(
    cmdclass={"build_py": BuildWithResources},
)
