all: 

build:
	python3 genFindPairInRoundTable.py
	python3 genDB.py

run:
	python3 main.py

clean:
	rm -rf findPairInRoundTable.json DB.json
	
test:
	@ echo "Pass"