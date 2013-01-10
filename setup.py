#!/usr/bin/python
import sys

from cx_Freeze import setup, Executable
from cx_Freeze import bdist_msi

base = None
if sys.platform == "win32":
	base = "Win32GUI"

setup(
	name = "runres",
	version = "0.1",
	description = "Runs application using specified resolution",
	options = { 
		"build_exe": {"includes": ["re"]},
		"cx_Freeze.windist.bdist_msi": {"upgrade-code":"{E22C543D-B08B-42d5-9F22-88E89AA0E226}", "add-to-path": True}
	},
	executables = [Executable("runres.py", base = base)]
	)
