#include "stdio.h"
#include <opencv2/opencv.hpp>
#include <opencv2/features2d/features2d.hpp>

#include <utility>
#include <cmath>

using namespace cv;
using namespace std;


int main(int argc, char *argv[])
{
	Mat empty(720, 1280, CV_8UC1);
	cv::rectangle(empty, Point(30, 30), Point(200, 200), Scalar(255));
	imshow("asdf", empty);
	waitKey();
	return 0;
}

