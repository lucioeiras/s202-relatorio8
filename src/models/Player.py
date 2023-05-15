from uuid import uuid5

class Player:
  def __init__(self, database):
    self.db = database

  def create(self, name):
    id = uuid5()

    query = "CREATE (:Player {id: $id, name: $name})"
    parameters = { "id": id, "name": name }

    self.db.execute_query(query, parameters)

  def list_all(self):
    query = "MATCH (p:Player) RETURN p.name AS name, p.id AS id"
    results = self.db.execute_query(query)

    return [(result["name"], result["id"]) for result in results]

  def read(self, name):
    query = "MATCH (p:Player {name: $name}) RETURN p.name AS name, p.id AS id"
    parameters = { "name": name }

    results = self.db.execute_query(query, parameters)

    return [(result["name"], result["id"]) for result in results]
  
  def update(self, old_name, new_name):
    query = "MATCH (p:Player {name: $old_name}) SET p.name = $new_name"
    parameters = {"old_name": old_name, "new_name": new_name}

    self.db.execute_query(query, parameters)

  def delete(self, name):
    query = "MATCH (p:Player {name: $name}) DETACH DELETE p"
    parameters = { "name": name }

    self.db.execute_query(query, parameters)