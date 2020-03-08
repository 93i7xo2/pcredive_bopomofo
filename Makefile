all: 

test:
	@! python3 main.py --input=./test_pic/invalid0.jpg --debug=True
	@! python3 main.py --input=./test_pic/invalid1.jpg --debug=True
	@! python3 main.py --input=./test_pic/invalid2.jpg --debug=True
	@! python3 main.py --input=./test_pic/invalid3.jpg --debug=True
	@! python3 main.py --input=./test_pic/invalid4.jpg --debug=True
	@! python3 main.py --input=./test_pic/invalid5.jpg --debug=True
	@! python3 main.py --input=./test_pic/invalid6.jpg --debug=True
	@ python3 main.py --input=./test_pic/valid0.jpg --debug=True
	@ python3 main.py --input=./test_pic/valid1.jpg --debug=True
	@ python3 main.py --input=./test_pic/valid2.jpg --debug=True

	@ python3 main.py --input=./test_pic/valid0.jpg --debug=True --output_x=x.txt --output_y=y.txt
	@ cat x.txt y.txt | grep "368236" >/dev/null
	@! python3 main.py --input=./test_pic/invalid0.jpg --debug=True --output_x=x.txt --output_y=y.txt
	@ cat x.txt y.txt | grep "\-1\-1" >/dev/null
	@ rm -rf x.txt y.txt
	@ echo "Pass"