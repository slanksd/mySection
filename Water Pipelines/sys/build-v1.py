import os, sys, winshell, shutil
from water_pipelines import waterPipelines
from wastewater_pump_stations import wastewaterPumpStations
from improvement_drawings import improvementDrawings
from reports import reports

sectionDirectory = r"Y:\EPM\CondAssess"
improvementDrawingDirectory = r"Y:\EPM\CondAssess\Improvement Drawings\By No"
WATER_PIPELINE_DRAWING_DIRECTORY_NAME = "Drawings"

def createShortcut( target="", shortcutPath="", icon_location="" ):
	if os.path.exists( target ) == False:
		print("WARNING: path: " + target + " does not exist.")
	with winshell.shortcut( shortcutPath ) as shortcut:
		shortcut.lnk_filepath = shortcutPath
		shortcut.path = target
		shortcut.icon_location = (icon_location,0)
		shortcut.write( shortcutPath )

def makeFacilityDirectories( facilities, buildDirectory ):
	print("Making facility folders...")
	for facility in facilities:
		path = buildDirectory + "\\" + facility
		if os.path.isdir( path ) == False:
			os.mkdir( path )

def getImprovementDrawings():
	print("Updating improvement drawing shortcuts...")
	drawingsByWaterPipeline = improvementDrawings["Water Pipelines"]
	for waterPipeline in waterPipelines:
		waterPipelineDirectory = os.path.join( buildDirectory, waterPipeline )
		if os.path.isdir( waterPipelineDirectory ):
			waterPipelineDrawingDirectory = os.path.join( waterPipelineDirectory, WATER_PIPELINE_DRAWING_DIRECTORY_NAME )
			drawingList = drawingsByWaterPipeline[waterPipeline]
			if os.path.isdir( waterPipelineDrawingDirectory ) == False and len( drawingList ) > 0:
				os.mkdir( waterPipelineDrawingDirectory )
			if len( drawingList ) > 0:
				print("...for  " + waterPipeline + "...")
				for drawing in drawingList:
					#print(drawing)
					target = os.path.join( improvementDrawingDirectory, drawing )
					shortcutPath = os.path.join( waterPipelineDrawingDirectory, drawing + ".lnk")
					icon_location = target
					#print("target: " + target)
					#print("shortcutPath: " + shortcutPath)
					createShortcut( 
						target=target, 
						shortcutPath=shortcutPath,
						icon_location=icon_location
					)
			# delete direcotry of it is empty
		else:
			print(waterPipelineDirectory + " is not a directory.")
		
		#print(drawingList)

def getReports( facilities ):
	print("Updating report shortcuts...")
	for keyName in reports:
		report = reports[ keyName ]
		print("...for " + keyName + "...")
		if "Water Pipelines" in report.keys():
			for facility in report["Water Pipelines"]:
				buildDirectory = sectionDirectory + "\\Water Pipelines"
				shortcutName = report["Publication Year"] + " " + report["BuildFileName"]
				target = report["Path"]
				shortcutPath = buildDirectory + "\\" + facility + "\\Reports\\" + shortcutName + ".lnk"
				icon_location = report["Path"]
				if os.path.isdir(buildDirectory + "\\" + facility) == False:
					print(facility + " is not a directory.")
					next
				if os.path.isdir(buildDirectory + "\\" + facility + "\\Reports") == False:
					os.mkdir( buildDirectory + "\\" + facility + "\\Reports" )
				createShortcut( 
					target=target, 
					shortcutPath=shortcutPath,
					icon_location=icon_location
				)
		if "Wastewater Pump Stations" in report.keys():		
			for facility in report["Wastewater Pump Stations"]:
				buildDirectory = sectionDirectory + "\\Wastewater Pump Stations"
				shortcutName = report["Publication Year"] + " " + report["BuildFileName"]
				target = report["Path"]
				shortcutPath = buildDirectory + "\\" + facility + "\\Reports\\" + shortcutName + ".lnk"
				icon_location = report["Path"]
				if os.path.isdir(buildDirectory + "\\" + facility) == False:
					print(facility + " is not a directory.")
					next
				if os.path.isdir(buildDirectory + "\\" + facility + "\\Reports") == False:
					os.mkdir( buildDirectory + "\\" + facility + "\\Reports" )
				createShortcut( 
					target=target, 
					shortcutPath=shortcutPath,
					icon_location=icon_location
				)

def deleteEmptyDirectories():
	print("Deleting empty subdirectories...")
	for waterPipeline in waterPipelines:
		waterPipelineDirectory = os.path.join( buildDirectory, waterPipeline )
		if os.path.isdir( waterPipelineDirectory ):
			for root, dirs, files in os.walk( waterPipelineDirectory ):
				for directory in dirs:
					if len( os.listdir( os.path.join( root, directory ) ) )== 0:
						try:
							#print( directory)
							os.rmdir( os.path.join( root, directory ) )
						except OSError as err:
							print("OS error: {0}".format(err))

	

makeFacilityDirectories( wastewaterPumpStations, sectionDirectory + "\\Wastewater Pump Stations" )
#getImprovementDrawings()
getReports( wastewaterPumpStations )
# delete empty subdirectories in pipeline directories
#deleteEmptyDirectories()