class Match:
  def create(self, id, house, visitor):
    query = "CREATE(:Match {id: $id, house_goals: $house_goals, visitor_goals: $visitor_goals})"
    parameters = { 
      "house_goals": house.goals, 
      "visitor_goals": visitor.goals 
    }

    self.db.execute_query(query, parameters)

    for player in house.players:
      query = "MATCH (p:Player {name: $player_name}) MATCH (m:Match {name: $match_id}) CREATE (p)-[:JOGOU_EM, {team: $team}]->(m)"
      parameters = { "player_name": player, "match_id": id, "team": "house" }

      self.db.execute_query(query, parameters)

    for player in visitor.players:
      query = "MATCH (p:Player {name: $player_name}) MATCH (m:Match {name: $match_id}) CREATE (p)-[:JOGOU_EM, {team: $team}]->(m)"
      parameters = { "player_name": player, "match_id": id, "team": "visitor" }

      self.db.execute_query(query, parameters)

  def read(self, id):
    parameters = { "id", id }

    query = "MATCH (p:Player)<-[:JOGOU_EM, {team: 'house'}]-(m:MATCH, {id: $id}) RETURN p.name AS player_name"
    house_players = self.db.execute_query(query, parameters)

    query = "MATCH (p:Player)<-[:JOGOU_EM, {team: 'visitor'}]-(m:MATCH, {id: $id}) RETURN p.name AS player_name"
    visitor_players = self.db.execute_query(query, parameters)

    query = "MATCH (m:match, {id: $id}) RETURN m.id AS id, m.house_goals AS house_goals, m.visitor_goals AS visitor_goals"
    match = self.db.execute_query(query, parameters)[0]

    return { 
      "match_id": match["id"], 
      "house_goals": match["house_goals"], 
      "visitor_goals":  match["visitor_goals"],
      "house_players": house_players,
      "visitor_players": visitor_players
    }
  
  def players_matches(self, name):
    query = "MATCH (p:Player, {name: $name})<-[:JOGOU_EM]-(m:MATCH) RETURN m.id AS match_id, m.house_goals AS house_goals, m.visitor_goals AS visitor_goals"
    parameters = { "name": name }
    results = self.db.execute_query(query, parameters)

    return [(result["match_id"], result["house_goals"], result["visitor_goals"]) for result in results]
