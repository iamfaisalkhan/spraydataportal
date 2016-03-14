
from util import zip, tar
from pymongo import MongoClient
import time
import os

class Injector:
    """ Injest an hdf5 file along with any data set """

    def __init__(self, config):
        self.sprayData = config['spraydata']
        self.files = config['files']
        self.dbname = config['mongodb']['dbname']
        self.uploadDir = config['upload']
        self.keysfile = config['search_keys_file']
        
        self.mongoClient = MongoClient()
        self.db = self.mongoClient[self.dbname]

    def inject(self):
        #insert attributes for the file
        attrs = self.sprayData.getAttributes()
        dsname = self.sprayData.getDataSetName()
        injector = attrs['injector']

        fileTozip = [x for x in self.files.keys()]
        zipDest = "%s/%s"%(self.uploadDir, self.sprayData.getArchiveName())

        zip(fileTozip, zipDest)
        tar(fileTozip, zipDest)

        # Description of the dataset.
        desc = dsname
        if 'description' in attrs:
            desc = attrs['description']

        doc = {
            'name' : dsname,
            'injector': injector,
            'description': desc,
            'files' : self.files.values(),
            'date_added' : int(time.time()),
            'zip_file' : ("%s.zip")%self.sprayData.getArchiveName(),
            'tar_file' : ("%s.tar.gz")%self.sprayData.getArchiveName(),
        }

        doc.update(attrs)

        res = self.db.dataset.insert(doc)

        self.refreshKeyData(doc);

    def refreshKeyData(self, doc):
        import json
        exclude = ['description', 'files', '_id', 'name', 'zip_file', 'date_added'];


        keys = set()
        if (os.path.isfile(self.keysfile)):
            with open(self.keysfile) as data_file:
                r = json.load(data_file)
                for item in r:
                    keys.add(item['label'])


        for k,v in doc.iteritems():
            if not k in exclude:
                str = "%s = %s"%(k,v)
                keys.add(str)


        data = []
        for key in keys:
            data.append({'label' : key, 'value' : key})
        
        with open(self.keysfile, 'w') as outfile:
            json.dump(data, outfile)



