import datetime
from google.appengine.ext import db

from app import configs
from app.interfaces import DataSource
from app.models import Track


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
    __instance = None

    def __init__(self):
        self.entitiesToAdd = []
        self.entitiesToUpdate = []
        self.keysToDelete = []
        pass

    @staticmethod
    def get_instance():
        if Bulk.__instance is None:
            Bulk.__instance = Bulk()
        return Bulk.__instance

    def add(self, entity):
        entity.created = datetime.datetime.utcnow()
        entity.updated = datetime.datetime.utcnow()
        self.entitiesToAdd.append(entity)
        self.flush_if_needed()

    def update(self, entity):
        entity.updated = datetime.datetime.utcnow()
        self.entitiesToUpdate.append(entity)
        self.flush_if_needed()

    def delete(self, entity):
        self.keysToDelete.append(entity.key())
        self.flush_if_needed()

    def flush_if_needed(self):
        self.flush_all(configs.BULK_SIZE)

    def flush_all(self, size=0):
        if len(self.entitiesToAdd) > size:
            db.put(self.entitiesToAdd)
            self.entitiesToAdd = []
        if len(self.entitiesToUpdate) > size:
            db.put(self.entitiesToUpdate)
            self.entitiesToUpdate = []
        if len(self.keysToDelete) > size:
            db.delete(self.keysToDelete)
            self.keysToDelete = []


class TrackDataSource(DataSource):
    MAX_SIZE = 1000000

    def __init__(self):
        DataSource.__init__(self)

    def save(self, processor, limit = -1):
        if limit <= 0:
            limit = self.MAX_SIZE
        cursor = None
        for i in range(1, limit, configs.SCROLL_SIZE):
            tracks, cursor = self.scroll(cursor, min(limit - i + 1, configs.SCROLL_SIZE))
            if len(tracks) == 0:
                break
            for t in tracks:
                processor.process(t)

    def scroll(self, cursor, size):
        query = Track.all()
        query.with_cursor(start_cursor=cursor)
        tracks = query.fetch(limit=size)
        next_cursor = query.cursor()

        return tracks, next_cursor
