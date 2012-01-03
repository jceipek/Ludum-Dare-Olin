from distutils.core import setup
import py2exe
import os

origIsSystemDLL = py2exe.build_exe.isSystemDLL # save the orginal before we edit it
def isSystemDLL(pathname):
    # checks if the freetype and ogg dll files are being included
    if os.path.basename(pathname).lower() in ("libfreetype-6.dll", "libogg-0.dll"):
            return 0
    return origIsSystemDLL(pathname) # return the orginal function
py2exe.build_exe.isSystemDLL = isSystemDLL # override the default function with this one


Mydata_files = [('', [
						'glowcrate.png',
						'door.png',
						'floorTurret.png',
						'laserBottom.png',
						'laserTop.png',
						'newcrate.png',
						'simplePlatform.png',
						'simpleWall.png',
						'turret.png',
						'roombg.png',
						'IntroPage.png',
						'GameOver.png',
						'YouWin.png',
						'alone2.mp3',
						'title.mp3'
					 ]
				),
				('astronaut', [
								'astronaut/walkingRight.png',
								'astronaut/walkingLeft.png',
								'astronaut/jumpingRight.png',
								'astronaut/jumpingLeft.png',
								'astronaut/standingRight.png',
								'astronaut/standingLeft.png',
							  ]
				)
				]
setup(
	console=['main.py'],
	data_files = Mydata_files,
	name = "Tarassis"
)