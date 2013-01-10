#!/usr/bin/python
# Simple script to set screen resolution
# Based on code from http://www.news2news.com/vfp/?example=374&ver=vcpp

import argparse
import ctypes
import ctypes.wintypes
import io
import subprocess
import sys

user32 = ctypes.windll.user32

CCHFORMNAME = 32
CCHDEVICENAME = 32
DM_BITSPERPEL = 0x00040000
DM_PELSWIDTH = 0x00080000
DM_PELSHEIGHT = 0x00100000
DM_DISPLAYFLAGS = 0x00200000
DM_DISPLAYFREQUENCY = 0x00400000
DM_POSITION = 0x00000020
DISPLAY_DEVICE_PRIMARY_DEVICE = 0x00000004
ENUM_CURRENT_SETTINGS = -1
CDS_UPDATEREGISTRY = 1
CDS_TEST = 2
CDS_FULLSCREEN = 4
CDS_GLOBAL = 8
CDS_SET_PRIMARY = 16
CDS_RESET = 0x40000000
CDS_SETRECT = 0x20000000
CDS_NORESET = 0x10000000
DISP_CHANGE_SUCCESSFUL = 0
DISP_CHANGE_RESTART = 1
DISP_CHANGE_FAILED = (-1)
DISP_CHANGE_BADMODE = (-2)
DISP_CHANGE_NOTUPDATED = (-3)
DISP_CHANGE_BADFLAGS = (-4)
DISP_CHANGE_BADPARAM = (-5)
DISP_CHANGE_BADDUALVIEW = (-6)



class DUMMYSTRUCT(ctypes.Structure):
	_fields_  = [
		("dmOrientation", ctypes.c_short),
		("dmPaperSize", ctypes.c_short),
		("dmPaperLength", ctypes.c_short),
		("dmPaperWidth", ctypes.c_short),
		("dmScale;", ctypes.c_short),
		("dmCopies;", ctypes.c_short),
		("dmDefaultSource;", ctypes.c_short),
		("dmPrintQuality;", ctypes.c_short)
	]


class DUMMYSTRUCT2(ctypes.Structure):
	_fields_ = [
		("dmPosition", ctypes.wintypes.POINTL),
		("dmDisplayOrientation", ctypes.wintypes.DWORD),
		("dmDisplayFixedOutput", ctypes.wintypes.DWORD)
	]

class DUMMYUNION(ctypes.Union):
	_anonymous_ = ["s1", "s2"]
	_fields_ = [
		("s1", DUMMYSTRUCT),
		("s2", DUMMYSTRUCT2)
	]

class DUMMYUNION2(ctypes.Union):
	_fields_ = [
		("dmDisplayFlags", ctypes.wintypes.DWORD),
		("dmNup", ctypes.wintypes.DWORD)
	]

class DEVMODE(ctypes.Structure):
	_anonymous_ = ["dummyunion", "dummyunion2"]
	_fields_ = [
		("dmDeviceName", ctypes.wintypes.BYTE*CCHDEVICENAME),
		("dmSpecVersion", ctypes.wintypes.WORD),
		("dmDriverVersion", ctypes.wintypes.WORD),
		("dmSize", ctypes.wintypes.WORD),
		("dmDriverExtra", ctypes.wintypes.WORD),
		("dmFields", ctypes.wintypes.DWORD),
		("dummyunion", DUMMYUNION),
		("dmColor", ctypes.c_short),
		("dmDuplex", ctypes.c_short),
		("dmYResolution", ctypes.c_short),
		("dmTTOption", ctypes.c_short),
		("dmCollate", ctypes.c_short),
		("dmFormName", ctypes.wintypes.BYTE*CCHFORMNAME),
		("dmLogPixels", ctypes.wintypes.WORD),
		("dmBitsPerPel", ctypes.wintypes.DWORD),
		("dmPelsWidth", ctypes.wintypes.DWORD),
		("dmPelsHeight", ctypes.wintypes.DWORD),
		("dummyunion2", DUMMYUNION2),
		("dmDisplayFrequency", ctypes.wintypes.DWORD),
#if(WINVER >= 0x0400) 
		("dmICMMethod", ctypes.wintypes.DWORD),
		("dmICMIntent", ctypes.wintypes.DWORD),
		("dmMediaType", ctypes.wintypes.DWORD),
		("dmDitherType", ctypes.wintypes.DWORD),
		("dmReserved1", ctypes.wintypes.DWORD),
		("dmReserved2", ctypes.wintypes.DWORD),
#if (WINVER >= 0x0500) || (_WIN32_WINNT >= 0x0400)
		("dmPanningWidth", ctypes.wintypes.DWORD),
		("dmPanningHeight", ctypes.wintypes.DWORD)
#endif
#endif /* WINVER >= 0x0400 */
	]


class DISPLAY_DEVICE(ctypes.Structure):
	_fields_ = [
		("cb", ctypes.wintypes.DWORD),
		("DeviceName", ctypes.wintypes.CHAR*32),
		("DeviceString", ctypes.wintypes.CHAR*128),
		("StateFlags", ctypes.wintypes.DWORD),
		("DeviceID", ctypes.wintypes.CHAR*128),
		("DeviceKey", ctypes.wintypes.CHAR*128)
	]


def get_resolution():
	"""Get current screen resolution
	:return: (width, height)
	"""
	return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def get_primary_device():
	"Gets the primary display device; ie screen"
	dd = DISPLAY_DEVICE()
	dd.cb = ctypes.sizeof(dd)
	index = 0
	while user32.EnumDisplayDevicesA(None, index, ctypes.pointer(dd),0):
		index = index+1
		if(dd.StateFlags & DISPLAY_DEVICE_PRIMARY_DEVICE):
			return dd

	return dd

def set_display_defaults():
	"Reset to default settings."
	user32.ChangeDisplaySettingsA(None, 0)

def set_resolution(width, height):
	"""Set the resolution of the screen
	:param width: width of screen
	:param height: height of screen
	"""
	dd = get_primary_device()
	dm = DEVMODE()
	dm.dmSize = ctypes.sizeof(dm)
	if not user32.EnumDisplaySettingsA(dd.DeviceName, ENUM_CURRENT_SETTINGS, ctypes.pointer(dm)):
		raise Exception("Failed to get display settings.")

	dm.dmPelsWidth = width
	dm.dmPelsHeight = height
	dm.dmFields = (DM_PELSWIDTH | DM_PELSHEIGHT)
	if user32.ChangeDisplaySettingsA(ctypes.byref(dm), CDS_TEST)!=DISP_CHANGE_SUCCESSFUL:
		raise Exception("Graphics mode not supported.")

	return user32.ChangeDisplaySettingsA(ctypes.byref(dm), 0)==DISP_CHANGE_SUCCESSFUL


MB_ABORTRETRYIGNORE = 0x00000002
MB_CANCELTRYCONTINUE = 0x00000006
MB_HELP = 0x00004000
MB_OK = 0x00000000
MB_OKCANCEL = 0x00000001
MB_RETRYCANCEL = 0x00000005
MB_YESNO = 0x00000004
MB_YESNOCANCEL = 0x00000003

MB_ICONEXCLAMATION = 0x00000030
MB_ICONWARNING = 0x00000030
MB_ICONINFORMATION = 0x00000040
MB_ICONASTERISK = 0x00000040
MB_ICONQUESTION = 0x00000020
MB_ICONSTOP = 0x00000010
MB_ICONERROR = 0x00000010
MB_ICONHAND = 0x00000010

MB_DEFBUTTON1 = 0x00000000
MB_DEFBUTTON2 = 0x00000100
MB_DEFBUTTON3 = 0x00000200
MB_DEFBUTTON4 = 0x00000300

MB_APPLMODAL = 0x00000000
MB_SYSTEMMODAL = 0x00001000
MB_TASKMODAL = 0x00002000

MB_DEFAULT_DESKTOP_ONLY = 0x00020000
MB_RIGHT = 0x00080000
MB_RTLREADING = 0x00100000
MB_SETFOREGROUND = 0x00010000
MB_TOPMOST = 0x00040000
MB_SERVICE_NOTIFICATION = 0x00200000

# Return values
IDABORT = 3
IDCANCEL = 2
IDCONTINUE = 11
IDIGNORE = 5
IDNO = 7
IDOK = 1
IDRETRY = 4
IDTRYAGAIN = 10
IDYES = 6

MessageBox = user32.MessageBoxW


if __name__=="__main__":
	output = None
	if sys.stdout==None:
		output = io.StringIO()
		sys.stdout = output
		sys.stderr = output

	try:
		parser = argparse.ArgumentParser(
			description="Run program using specified resolution.",
			epilog="When program exits, the resolution is reset.")
		parser.add_argument("width", type=int, help="Screen width")
		parser.add_argument("height", type=int, help="Screen height")
		parser.add_argument("cmd", type=str, help="Command to execute")
		args = parser.parse_args()
		try:
			set_resolution(args.width, args.height)
			subprocess.call(args.cmd)
		finally:
			set_display_defaults()
	finally:
		if output is not None:
			msg = output.getvalue()
			if len(msg)>0:
				title = sys.argv[0]
				MessageBox(None, msg, title, 0)

			output.close()