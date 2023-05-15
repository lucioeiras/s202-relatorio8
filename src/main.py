from config.database import Database
from models.Player import Player
from models.Match import Match

db = Database("bolt://44.210.115.13:7687", "neo4j", "saturday-nozzles-collections")

match = Match(db)
player = Player(db)

print("1. Administrar jogador")
print("2. Listar jogadores")
print("3. Adicionar partida")
print("4. Visualizar partida")
print("5. Visualizar partidas por jogador")
print("6. Sair")

option = int(input("Qual opção você deseja? "))

while (option != 6):
  if (option == 1):
    print("")

    print("1. Adicionar jogador")
    print("2. Visualizar jogador")
    print("3. Alterar jogador")
    print("4. Deletar jogador")

    new_option = int(input("Qual opção você deseja? "))

    while (new_option != 6):
      if (new_option == 1):
        player_name = input("Qual o nome do jogador? ")
        player.create(name=player_name)

        print("Jogador adicionado com sucesso!")
      elif (new_option == 2):
        player_name = input("Qual o nome do jogador? ")
        player = player.read(name=player_name)

        print("ID: ", player.id)
        print("Nome: ", player.name)
      elif (new_option == 3):
        old_name = input("Qual o nome do jogador? ")
        new_name = input("Qual o novo nome do jogador? ")
        player.update(old_name=old_name, new_name=new_name)

        print("Jogador atualizado com sucesso!")
      elif (new_option == 3):
        player_name = input("Qual o nome do jogador? ")
        player.delete(name=player_name)

        print("Jogador deletado com sucesso!")
        
      print("")
      new_option = int(input("Qual opção você deseja? "))

  elif (option == 2):
    players = player.list_all()

    for player in players:
      print("ID: ", player.id)
      print("Nome: ", player.name)
      print("")

  elif (option == 3):
    id = input("Qual o ID da partida? ")
    house_goals = input("Quantos gols o time da casa fez? ")
    visitor_goals = input("Quantos gols o time visitante fez? ")

    print("Entre com os jogadores da casa:")
    house_players = []

    for i in range(0, 11):
      player_name = input("")
      house_players.append(player_name)

    print("Entre com os jogadores visitantes:")
    visitor_players = []

    for i in range(0, 11):
      player_name = input("")
      visitor_players.append(player_name)

    match.create(
      id=id, 
      home={ "goals": house_goals, "players": house_players },
      visitor={ "goals": visitor_goals, "players": visitor_players }
    )

  elif (option == 4):
    match_id = input("Qual o ID da partida? ")
    match = match.read(id=match_id)

    print("ID da partida: ", match.id)
    print("Gols do time da casa: ", match.house_goals)
    print("Gols do time visitante: ", match.visitor_goals)

    print("Jogadores do time da casa: ")
    for player in match.house_players:
      print("- ", player)

    print("Jogadores do time da casa: ")
    for player in match.visitor_players:
      print("- ", player)

  elif (option == 5):
    player_name = input("Qual o nome do jogador? ")
    matches = match.players_matches(name=player_name)

    for match in matches:
      print("ID da partida: ", match.match_id)
      print("Gols do time da casa: ", match.house_goals)
      print("Gols do time visitante: ", match.visitor_goals)

  print("")
  option = int(input("Qual opção você deseja? "))
