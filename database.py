# import psycopg2
#
# class Player:
#     def __init__(self, name, score):
#         self.name = name
#         self.score = score
#
# class Database:
#     def __init__(self):
#         self.conn = psycopg2.connect(
#             dbname="Game Database",
#             user="postgres",
#             password="root",
#             host="127.0.0.1"
#         )
#         self.cur = self.conn.cursor()
#
#     def insert_game_data(self, player, enemy):
#         try:
#             query = """INSERT INTO game_results (player1_name, player2_name, player1_score, player2_score)
#                        VALUES (%s, %s, %s, %s)"""
#             self.cur.execute(query, (player.name, enemy.name, player.score, enemy.score))
#             self.conn.commit()
#             print("Data inserted successfully!")
#         except psycopg2.Error as e:
#             print(f"Error inserting data: {e}")
#
#     def close_connection(self):
#         self.cur.close()
#         self.conn.close()
#
# if __name__ == "__main__":
#     # Assuming you have initialized 'player' and 'enemy' objects of the 'Player' class
#     # Initialize the Database object
#     db = Database()
#
#     # Example usage:
#     player = Player("Jawad", 8)
#     enemy = Player("Sajid", 10)
#
#     # Insert game data into the database
#     db.insert_game_data(player, enemy)
#
#     # Close the database connection
#     db.close_connection()


import csv


class Database:
    def __init__(self):
        self.file_name = 'game_data.csv'
        self.headers_written = False

    def write_to_csv(self, player1_name, player2_name, player1_score, player2_score):
        data = [
            [player1_name, player1_score, player2_name, player2_score]
        ]

        with open(self.file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not self.headers_written:  # Write headers if not already written
                writer.writerow(['Player 1 Name', 'Player 1 Score', 'Player 2 Name', 'Player 2 Score'])
                self.headers_written = True
            writer.writerows(data)

    def save_game_data(self, player1, player2):
        self.write_to_csv(player1.name, player2.name, player1.score, player2.score)
