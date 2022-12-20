a.exe: a.cpp
	c++ -O2 --std=c++17 -I ../../ac-library -D USE_PYTHON_LIKE_PRINT a.cpp

nodebug: a.cpp
	c++ -O2 --std=c++17 -I ../../ac-library a.cpp

expand: a.cpp
	python3 ../../ac-library/expander.py a.cpp

%: a.exe %.in
	time ./a.exe < $@.in

