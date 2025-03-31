import sqlite3
import os
from utils.coro import use_sync


__all__ = ['Database']


DEFAULT_DIRECTORY = os.getcwd()


class Database:
  def __init__(self, name, directory=DEFAULT_DIRECTORY):
    self.name = name
    self.directory = directory
    self.path = os.path.join(directory, name)
    self.connection = None
  
  async def connect(self):
    if self.connection is None:
      self.connection = await use_sync(lambda: sqlite3.connect(self.path, check_same_thread=False))
    return self.connection
  
  async def close(self):
    if self.connection:
      await use_sync(self.connection.close)
      self.connection = None

  async def execute(self, query, params=None, commit=True, fetch="all"):
    if self.connection is None:
      await self.connect()

    cursor = await use_sync(self.connection.cursor)

    if params:
      await use_sync(lambda: cursor.execute(query, params))
    else:
      await use_sync(lambda: cursor.execute(query))

    if commit:
      await use_sync(self.connection.commit)
    
    if fetch == "all":
      return await use_sync(cursor.fetchall)
    elif fetch == "one":
      return await use_sync(cursor.fetchone)
