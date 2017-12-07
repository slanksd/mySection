import io
import os
import sys
import datetime
import pprint
import PIL.Image

PHOTOS_DIRECTORY = r"\\aladdin2\epm\CondAssess\Photos\Files"

strKml = ""
strLog = "Generated on " + str( datetime.datetime.now() ) + "\n"

with io.open( r"\\aladdin2\epm\CondAssess\Photos\utils\kmlTemplateHead.kml", "r", encoding="utf-8"  ) as file:
	strKml = file.read()

#for root, dirs, files in os.walk( "..\\Files\\2017.05.04-SLa" ):
directories = []

print("Scanning directories...")
for root, dirs, files in os.walk( PHOTOS_DIRECTORY ):
	for dirName in dirs:
		directories.append( [ root + "\\" + dirName , dirName ] )

print("Generating kml code...")
for directory in directories:
	print("Processing directory: " + directory[0] )
	for root, dirs, files in os.walk( directory[0] ):
		strKml += "<Folder><name>" + directory[1].replace("&","&amp;") + "</name>"
		strKml += "<visibility>0</visibility>"
		strKml += "<open>0</open>"
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
					if 34853 in exif_data:
						
						northingDeg = exif_data[34853][2][0][0]
						northingMin = exif_data[34853][2][1][0]
						northingSec = exif_data[34853][2][2][0] / exif_data[34853][2][2][1]
						northing = northingDeg + northingMin / 60 + northingSec / 60 / 60
						if exif_data[34853][1] == "S":
							northing *= -1
						eastingDeg = exif_data[34853][4][0][0]
						eastingMin = exif_data[34853][4][1][0]
						eastingSec = exif_data[34853][4][2][0] / exif_data[34853][4][2][1]
						easting = eastingDeg + eastingMin / 60 + eastingSec / 60 / 60
						if exif_data[34853][3] == "W":
							easting *= -1
						strNorthing = str(northing)
						strEasting = str(easting)
						strKml += \
							"<Placemark>" + \
								"<name>" + name + "</name>" + \
								"<visibility>0</visibility>" + \
								"<description><![CDATA[<img style=\"max-width:500px;\" src=\"" + PHOTOS_DIRECTORY + "\\" +  name + "\">]]></description>" + \
								"<LookAt>" + \
									"<longitude>" + strEasting + "</longitude>" + \
									"<latitude>" + strNorthing + "</latitude>" + \
									"<altitude>0</altitude>" + \
									"<heading>0.3093354852598443</heading>" + \
									"<tilt>0</tilt>" + \
									"<range>21872.10725297808</range>" + \
									"<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>" + \
								"</LookAt>" + \
								"<styleUrl>#m_ylw-pushpin</styleUrl>" + \
								"<Point>" + \
									"<gx:drawOrder>1</gx:drawOrder>" + \
									"<coordinates>" + strEasting + "," + strNorthing + ",0</coordinates>" + \
								"</Point>" + \
							"</Placemark>"
					else:
						strLog += "Dictionary key 34853 not found for: " + root + "\\" +  name + "\n"
					continue
				except OSError as err:
				    strLog += "OS error: {0}\n".format(err)
				except ValueError:
				    strLog += "Could not convert data to an integer.\n"
				except:
				    strLog += "Unexpected error; file: " + root + "\\" +  name + "; " + str( sys.exc_info()[0] ) + "\n"
		strKml += "</Folder>"

print("Getting kml file footer code...")
with io.open( r"\\aladdin2\epm\CondAssess\Photos\utils\kmlTemplateFooter.kml", "r", encoding="utf-8" ) as file:
	strKml += file.read()

print("Writing to kml file...")
with io.open( r"\\aladdin2\epm\CondAssess\Photos\utils\photos.kml", "w", encoding="utf-8" ) as file:
	file.write( strKml )

print("Writing log file...")
with io.open( r"\\aladdin2\epm\CondAssess\Photos\utils\makePhotoKml.log.txt", "w", encoding="utf-8" ) as file:
	file.write( strLog )