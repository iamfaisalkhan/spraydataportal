import argparse

from config import Config
from spraydata import SpryData
from injector import Injector
from util import zip, fileInfo

def main():

	parser = argparse.ArgumentParser(description='Data injestor for fule injection experiment at 7-id')

	parser.add_argument("h5file", help="*path to the h5file with attributes")
	parser.add_argument("-c", "--config", action="store", dest="configPath", help="Path to the config file. (default: spraydata_config in current dir)")
	parser.add_argument("-d", "--dataset_name", action="store", dest="datasetName", help="Name of the current datset (default: name of the h5 file)")
	parser.add_argument("-f", "--files", action="store", dest="files", nargs='*', help="list of files contained in this dataset")
	parser.add_argument("-k", "--key", action="store", dest="newkeymap", nargs='*', help="Overide default key-value mapping")
	parser.add_argument("-a", "--attributes", action="store", dest="attrs", nargs="*", help="Pass extra attributes to store with the dataset")
	
	args = parser.parse_args()

	listoffiles = set()
	if (args.files):
		for file in args.files:
			listoffiles.add(file)

	listoffiles.add(args.h5file)

    # configuraiton object used by this application. 
	config = Config(args)
	
	config['spraydata'] = SpryData(args.h5file, config)
	config['files'] = fileInfo(listoffiles)

	injector = Injector(config)
	injector.inject()
	

if __name__ == "__main__":
	main()