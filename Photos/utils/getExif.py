import io
import os
import sys
import datetime
import pprint
import PIL.Image

strLog = "Generated on " + str( datetime.datetime.now() ) + "\n"

#for root, dirs, files in os.walk( "..\\Files\\2017.05.04-SLa" ):
directories = []

directory = os.getcwd()

print("Getting exif data...")
for root, dirs, files in os.walk( directory ):
	for name in files:
		if name.endswith( ".db" ) \
		or name.endswith( ".mp4" ) \
		or name.endswith( ".MP4" ) \
		or name.endswith( ".png" ) \
		or name.endswith( ".PNG" ):

			strLog += "Ignored: " + root + "\\" +  name + "\n"

		else:
			try:
				img = PIL.Image.open( root + "\\" +  name )
				exif_data = img._getexif()
				strLog += "exif of: " + root + "\\" +  name + "\n" \
					+ pprint.PrettyPrinter( indent=4 ).pformat( exif_data ) + "\n\n"
				#pprint.PrettyPrinter( indent=4 ).pprint(exif_data)

				continue
			except OSError as err:
			    strLog += "OS error: {0}\n".format(err)
			except ValueError:
			    strLog += "Could not convert data to an integer.\n"
			except:
			    strLog += "Unexpected error; file: " + root + "\\" +  name + "; " + str( sys.exc_info()[0] ) + "\n"

print("Writing log to file.")
with io.open( "getExif.log.txt", "w", encoding="utf-8" ) as file:
	file.write( strLog )