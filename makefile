#infinite chill / 2017
all: clean 555-coin 555-server

555-coin: 555-coin.py
	cp 555-coin.py 555-coin
	chmod u+x 555-coin


555-server: 555-server.py
	cp 555-server.py 555-server
	chmod u+x 555-server

run:
	./555-coin

runserver:
	./555-server MP00

test:
	./555-coin 20


clean:
	rm -f 555-server
