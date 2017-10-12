# Author: Spencer Lank

import io
import os
import datetime

with io.open( "checkPhotos.txt", "w", encoding="utf-8"  ) as outputFile:
	outputFile.write( "Generated on " + str( datetime.datetime.now() ) + "\n" )
	for root, dirs, files in os.walk( "..\Files" ):
		for name in files:
			if name.endswith( ".db" ):
				pass
			else:
				outputFile.write( root + name + "\n" )