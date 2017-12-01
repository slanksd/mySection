import os, sys, winshell, shutil
from water_pipelines import waterPipelines

buildDirectory = r"Y:\EPM\CondAssess\Water Pipelines"

pipelineDirs = waterPipelines




def createShortcut( target="", shortcutPath="", icon_location="" ):
	with winshell.shortcut( shortcutPath ) as shortcut:
		shortcut.lnk_filepath = shortcutPath
		shortcut.path = target
		shortcut.icon_location = (icon_location,0)
		shortcut.write( shortcutPath )
		print(shortcut.lnk_filepath)
	'''
	winshell.CreateShortcut(
		Path = shortcutPath,
		Target = target,
		Icon = ( icon_location, 0 )
	)
	'''

def makePipelineDirectories():
	print("Making water pipline directories")
	for waterPipeline in waterPipelines:
		path = buildDirectory + "\\" + waterPipeline
		if os.path.isdir( path ) == False:
			os.mkdir( path )

def getReports():
	print("Getting reports")
	from reports import reports
	for keyName in reports:
		report = reports[ keyName ]
		for waterPipelineDir in report["Water Pipeline Directory"]:
			shortcutName = report["BuildFileName"]
			target = report["Path"]
			shortcutPath = buildDirectory + "\\" + waterPipelineDir + "\\Reports\\" + shortcutName + ".lnk"
			icon_location = report["Path"]
			if os.path.isdir(buildDirectory + "\\" + waterPipelineDir) == False:
				print(waterPipelineDir + " directory does not exist.")
				next
			if os.path.isdir(buildDirectory + "\\" + waterPipelineDir + "\\Reports") == False:
				os.mkdir( buildDirectory + "\\" + waterPipelineDir + "\\Reports" )
			createShortcut( 
				target=target, 
				shortcutPath=shortcutPath,
				icon_location=icon_location
			)

makePipelineDirectories()
getReports()