libld06.so: src/*
	g++ -shared -g -Og -o $@ src/lipkg.cpp src/tofbf.cpp src/capi.cpp
