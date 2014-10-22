#include "stdio.h"
#include <opencv2/opencv.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <utility>
#include <cmath>


using namespace cv;
using namespace std;



int main(int argc, char *argv[])
{
	Mat img0 = imread(argv[1]);
	int numKeyPoints = 1500;
	ORB orb(numKeyPoints);

	OrbFeatureDetector* detector = new OrbFeatureDetector(numKeyPoints);
	OrbDescriptorExtractor* extractor = new OrbDescriptorExtractor();
	BruteForceMatcher* matcher = new BruteForceMatcher<cv::HammingLUT>;
	return 0;


	
}
