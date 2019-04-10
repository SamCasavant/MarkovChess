import chess
import chess.pgn
import random
import sys
import re
import shelve

#In the process of:
# shelving

def chain(moves, models):
	index = 0
	for move in moves:
		n = 1
		key = ' '.join(moves[index-n:index])
		while True:
			try: # If the context+key have been seen before
				if move in models[str(n)][key]: # If the move has been seen before
					models[str(n)][key][move] = str(int(models[str(n)][key][move])+1) # Increase frequency
					if int(models[str(n)][key][move]) > 2:
						models[str(n)][key]['advance'] = True
				else:
					models[str(n)][key][move] = '1'
					
				if models[str(n)][key]['advance']==False:
					break
				n=int(n)
				n+=1
				if n>len(moves): #if there is too much context to generate the upcoming key
					break
				key = ' '.join(moves[index-n:index])
			except KeyError:
				try: # attempt to generate at key level
					models[str(n)][key] = {move:'1', 'advance':False}
					break
				except KeyError: # generate new context level
					models[str(n)] = {key: {move:'1', 'advance':False}}
					break
		index += 1

def makestring(length):	
	with shelve.open('models') as models:
		print(models['games'])
		moves = ['_']
		for index in range(0, length): #iterate over space to fill with moves
			if index % 2 == 0: # If white playing
				n=1 
				cur_move = ''
				while True:
					key = ' '.join(moves[index+1-n:])
					print("Key:", key)
					print("index:", index)
					print(moves[index-n:])
					print("n:", n)
					try:
						if models[str(n)][key]['advance']:
							print("Advance")
							print(models[str(n)][key])
							cur_move = random.choice([move for move in models[str(n)][key] if move != 'advance'])
							print(cur_move)
							n+=1
						else:
							try: 
								"BBBBBB"
								print("Play at current level")
								key = ' '.join(moves[index-n+1:])
								population = [move for move in models[str(n)][key] if move != 'advance']
								weights = [int(models[str(n)][key][move]) for move in population]
								print("weights for", population, ":", weights)
								newmove = random.choices(population=population, 
									weights=weights, k=1)[0]
								moves.append(newmove)
								break
							except KeyError:
								newmove = cur_move
								print("Playing cur_move (", cur_move, ")")
								moves.append(newmove)
								break	

					except KeyError:
						for m in range(1, n):
							try:
								key = ' '.join(moves[index-(n-m-1):])
								print(key, n-m)
								population = [move for move in models[str(n-m)][key] if move != 'advance']
								weights = [int(models[str(n-m)][key][move]) for move in population]
								print("(should be different)weights for", population, ":", weights)
								newmove = random.choices(population=population, 
									weights=weights, k=1)[0]
								moves.append(newmove)
								break
							except KeyError:
								pass
						break
						#except KeyError:
						#	newmove = cur_move
						#	print("Playing cur_move (", cur_move, ")")
						#	moves.append(newmove)
						#	break
						
			else: #if black playing
				movestr = ' '.join(moves)
				newmove = input(movestr + " ") 
				moves.append(newmove)
			
			if newmove == "0-1":
				print("Black wins")
				return movestr
			if newmove == "1-0":
				print("White wins")
				return movestr
			if newmove == "1/2-1/2":
				print("Stalemate")
				return movestr

			
		return moves

if __name__ == '__main__':
	#ChessAI.py [pgn file] [number of games] [output length]
	#Models = Dictionary of context levels, each a dictionary of input moves at that context, 
	#  each a dictionary of output moves and frequencies + whether context should be increased
	models =  shelve.open('models', writeback = True)
	if '1' not in models:
		models['1'] = {'_':{'e4': '1', 'advance':False}}
		models['games'] = 1

	pgn = open(sys.argv[1])
	first_game = 0
	#for each in range(0, int(sys.argv[2])):
	#	try:
	#		while(first_game < models['games']):
	#			game = chess.pgn.read_game(pgn)
	#			first_game += 1
	#	except:
	#		pass
	#	exporter = chess.pgn.StringExporter(headers=False, variations=False, comments=False)
	#	game_str = game.accept(exporter)
	#	game_str = re.sub(r"[1234567890]*\.|\*", "", game_str)
	#	game_str = re.sub(r"\n", " ", game_str)
	#	moves = game_str.split(' ')
	#	moves = list(filter(('').__ne__, moves))
	#	moves.insert(0, "_")
	#	if each % 1000 == 0:
	#		models.sync()
	#	chain(moves, models)
	#	print(first_game)
	#	models['games'] += 1
	models.close()
	#while(True):
		#try:
	string = makestring(int(sys.argv[3]))
		#print(str(string))
		#except KeyError as e:
		#	print("Cannot improvise moves at present time", e)