# Mini Stats
A script which compiles answers from NYT mini puzzles. 
Full credit goes to Joel Fagliano for these amazing puzzles! 


## How it works
This was way simpler than I thought it would be. 
Using my subscription token and a given date, the bot can request a JSON file with the contents of each mini crossword. It iterates through each square and builds a list of words, then it adds those words to the word counter. 
I add a 5-second delay between each request to avoid getting rate-limited. 