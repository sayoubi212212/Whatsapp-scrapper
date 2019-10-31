import os
import json
import pickle
import time

class Env:
    # this class is responsible for creating and retrieving resources (folders,files) for crawled websites.
    # each time we crawl over a new website, we will create separate, dedicated resources for it.

    def createFolder(directory):
        #create a new folder
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except:
                raise Exception("directory creation failed: {}".format(directory))

    def writeToJSON(file_name, data):
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name, 'w') as fp:
            json.dump(data, fp)

    def appendToJSON(file_name, data):
        with open(file_name, 'a+') as fp:
            json.dump(data, fp)

    def appendToPickle(file_name, data):
        with open(file_name, 'ab+') as fp:
            pickle.dump(data, fp, pickle.HIGHEST_PROTOCOL)

    def pickleIterator(file_name):
        # iterates over a pickle file, each yield returns the next object saved on the file
        try:
            with open(file_name, 'rb') as fp:
                try:
                    while True:
                        data = pickle.load(fp)
                        yield pickle.load(fp)
                except EOFError:  # no more objects in the pickle
                    pass
        except:
            raise RuntimeError("cannot open pickle file: {}".format(file_name))
