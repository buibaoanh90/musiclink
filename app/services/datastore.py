import datetime
from google.appengine.ext import db


class DataStore:
    __instance = None

    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        if DataStore.__instance is None:
            DataStore.__instance = DataStore()
        return DataStore.__instance

    def add(self, entity):
        entity.created = datetime.datetime.utcnow()
        entity.put()

    def update(self, entity):
        entity.put()

    def delete(self, entity):
        entity.delete()


class Bulk:
    SIZE = 100
    __instance = None

    def __init__(self):
        self.entitiesToAdd = []
        self.keysToDelete = []
        pass

    @staticmethod
    def get_instance():
        if Bulk.__instance is None:
            Bulk.__instance = Bulk()
        return Bulk.__instance

    def add(self, entity):
        entity.created = datetime.datetime.utcnow()
        self.entitiesToAdd.append(entity)
        self.flush_if_needed()

    def delete(self, entity):
        self.keysToDelete.append(entity)
        self.flush_if_needed()

    def flush_if_needed(self):
        self.flush_all(Bulk.SIZE)

    def flush_all(self, size=0):
        if len(self.entitiesToAdd) > size:
            db.put(self.entitiesToAdd)
            self.entitiesToAdd = []
        if len(self.keysToDelete) > size:
            db.delete(self.keysToDelete)
            self.keysToDelete = []
