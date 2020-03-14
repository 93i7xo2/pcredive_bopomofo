all: 

build:
	python3 genFindPairInRoundTable.py
	python3 genDB.py

run:
	@echo nothing

clean:
	rm -rf findPairInRoundTable.json DB.json
test:
	@ echo "Pass"