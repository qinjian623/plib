#include "stdio.h"
#include <string>
#include <opencv2/opencv.hpp>

using namespace cv;

int main(int argc, char *argv[])
{
	Mat src;
	src = imread(argv[1]);
	string name = string(argv[1])+ ".jpg";
	imwrite(name, src);
	return 0;
}
