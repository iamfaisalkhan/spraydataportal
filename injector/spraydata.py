
try:
	import h5py
except ImportError:
	sys.exit('H5py must be installed before using this class')

from config import Config

class SpryData:
	""" Injest an hdf5 file along with any data set """

	def __init__(self, file, config):
		self.args = {}
		self.filepath = file
		self.h5File = h5py.File(file, 'r')
		self.config = config
		self.datasetName = None
		self.zipFileName = None
		self.tarFileName = None
		self.attrs = {}

	def getAttributes(self):
		attrs = {}

		for key, value in self.h5File.attrs.iteritems():
			klower = key.lower().replace(",", " ")
			
			# Updated the key based on map (if given)
			if klower in self.config['keymap']:
				attrs[self.config['keymap'][klower]] = value
			else:
				attrs[klower] = value
				
		return attrs

	def getDataSetName(self):
		if self.datasetName:
			return self.datasetName

		import os
		# First lookup user provided option for the this injestion
		if 'datasetName' in self.config and self.config['datasetName']:
			return self.config['datasetName']

		# Since no dataset name was provided on the command line, we will construct one.
		if self.h5File and len(os.path.basename(self.filepath)) > 0:
			filename, file_ext = os.path.splitext(os.path.basename(self.filepath))
			if len(filename) > 0:
				self.datasetName = filename
			else:
				self.datasetName = 'Undefined'

		return self.datasetName


	def getArchiveName(self):
		if self.zipFileName:
			return self.zipFileName


		import time
		ts = int(time.time())

		self.zipFileName = "%s_%d"%(self.getDataSetName().replace(', ', '_'), ts)
		return self.zipFileName
