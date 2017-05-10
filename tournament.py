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
    cur.execute("UPDATE players SET wins = 0, matches = 0;")
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
    cur.execute("INSERT INTO players (name, wins, matches) VALUES (%s, %s, %s);", (str(name), 0, 0))
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
    cur.execute("SELECT player_id, name, wins, matches FROM players ORDER BY wins;")
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
    cur.execute("UPDATE players SET wins = wins+1, matches = matches+1 WHERE player_id = (%s);", (winner,))
    cur.execute("UPDATE players SET matches = matches+1 WHERE player_id = (%s);", (loser,))
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
    cur.execute("SELECT player_id, name, wins FROM players")
    cur.execute("CREATE OR REPLACE VIEW updated_match AS \
                SELECT  player_id, \
                        name, \
                        COUNT(CASE WHEN players.player_id = match.winner_id THEN 1 ELSE 0 END) AS number_of_wins, \
                        COUNT(matches) AS match_count \
                FROM players LEFT JOIN match \
                ON players.player_id = match.winner_id \
                GROUP BY player_id \
                ORDER BY wins;")
    cur.execute("SELECT player_id, name FROM updated_match;")
    records = cur.fetchall()
    # Make list of tuples
    c = 0
    pairs = []
    while c < len(records):
        pairs.append(records[c]+records[c+1])
        c += 2

    db.commit()
    db.close()
    print "pairs: ", pairs
    return pairs
