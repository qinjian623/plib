love: opencv.cpp
	clang++ -O2 opencv.cpp -lm -o opencv -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_features2d

hog: hog.cpp
	clang++ -O2 hog.cpp -lm -o hog -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_features2d -lopencv_objdetect

label: label.cpp
	g++ -O2 label.cpp -lm -o label -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_features2d

label_debug: label.cpp
	g++ -g label.cpp -lm -o label -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_features2d

nn: nn_splitter.cpp
	g++ -g nn_splitter.cpp -lm -o nn -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_features2d
