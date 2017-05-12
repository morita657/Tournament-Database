#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("DELETE FROM match;")
    # Delete the history of players table
    # cur.execute("UPDATE players SET wins = 0, matches = 0;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("DELETE FROM players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT count(name) as num FROM players;")
    result = cur.fetchone()[0]
    db.close()
    return int(result)


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cur = db.cursor()
    cur.execute("INSERT INTO players (name) VALUES (%s);", (str(name),))
    # print "Come on: ", cur
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT players.player_id, players.name FROM players;")
    cur.execute("SELECT players.player_id, count(match.match_id) AS wins FROM players JOIN match \
                 ON players.player_id = match.winner_id \
                 GROUP BY players.player_id;")

    cur.execute("SELECT players.player_id, count(match.match_id) AS wins \
                 from players LEFT OUTER JOIN match \
                 ON players.player_id != match.loser_id \
                 GROUP BY players.player_id;")

    cur.execute("SELECT players.player_id, count(match.match_id) AS played \
                 from players LEFT OUTER JOIN match \
                 ON players.player_id != match.winner_id OR players.player_id != match.loser_id \
                 GROUP BY players.player_id;")

    cur.execute("CREATE VIEW view_wins AS \
                 SELECT players.player_id, count(match.match_id) AS wins \
                 FROM players LEFT OUTER JOIN match \
                 ON players.player_id = match.winner_id \
                 GROUP BY players.player_id;")

    cur.execute("CREATE VIEW view_played AS \
                 SELECT players.player_id, count(match.match_id) AS played \
                 FROM players LEFT OUTER JOIN match \
                 ON players.player_id = match.winner_id OR players.player_id = match.loser_id \
                 GROUP BY players.player_id;")

    cur.execute("SELECT p.player_id, p.name, vw.wins, vp.played \
                 FROM players AS p \
                 INNER JOIN view_wins AS vw ON p.player_id = vw.player_id \
                 INNER JOIN view_played AS vp ON p.player_id = vp.player_id \
                 ORDER BY vw.wins;")
    result = cur.fetchall()
    db.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cur = db.cursor()
    cur.execute("INSERT INTO match (winner_id, loser_id) VALUES (%s, %s);", (winner, loser,))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    cur = db.cursor()
    records = playerStandings()
    # Make list of tuples
    c = 0
    # I used the following code which was written by PhilipCoach in Discussion Forum.
    # https://discussions.udacity.com/t/idiomatic-code-for-swisspairings-function/17210
    pairs = []
    for player1, player2 in zip(records[0::2], records[1::2]):
        pairs.append((player1[0], player1[1], player2[0], player2[1]))
    db.commit()
    db.close()
    return pairs
