#include "stdio.h"
#include <opencv2/opencv.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <utility>
#include <cmath>


using namespace cv;
using namespace std;


SimpleBlobDetector::Params params;
Ptr<FeatureDetector> blob_detector;
void init()
{
	params.minDistBetweenBlobs = 1.0f;
	params.filterByInertia = false;
	params.filterByConvexity = false;
	params.filterByColor = true;
	params.filterByCircularity = false;
	params.filterByArea = true;
	params.blobColor = 255;
	params.minArea = 10.0f;
	params.maxArea = 10000.0f;
	params.minConvexity = 0.3f;
	params.maxConvexity = 100.0f;
	blob_detector= new SimpleBlobDetector(params);
	blob_detector->create("SimpleBlob");
}


void find_pairs(vector< pair<KeyPoint, KeyPoint> > & pairs, vector<KeyPoint> & keypoints){
	for (size_t i = 0; i < keypoints.size(); i++) {
		for (size_t j = i; j < keypoints.size(); j++) {
			if (i == j){
				continue;
			}
			float y0 = keypoints[i].pt.y;
			float y1 = keypoints[j].pt.y;
			if (abs(y0-y1)< 5){
				pairs.push_back(make_pair(keypoints[i],keypoints[j]));
			}
		}
	}
}

Mat CannyThreshold(Mat &gray)
{
	Mat detected_edges;
	/// 使用 3x3内核降噪
	blur(gray, detected_edges, Size(5,5));
	/// 运行Canny算子
	// detected_edges
	Canny(detected_edges, detected_edges, 50, 50*3, 3);
	return detected_edges;
}

void car_rear_dection_ROI(Mat &image0)
{
	uchar* d = image0.data;
	int size = image0.rows*image0.cols;
	Mat M(image0.rows,image0.cols, CV_8UC1, Scalar(0,0,255));
	Mat hsv, gray, mask1, mask0, mask;
	cvtColor(image0, hsv, CV_BGR2HSV);
	cvtColor(image0, gray, CV_BGR2GRAY);

	inRange(hsv, Scalar(165, 60, 0),Scalar(180, 255, 255), mask1);
	inRange(hsv, Scalar(0, 60, 0),Scalar(5, 255, 255), mask0);
	cv::bitwise_or(mask0, mask1, mask);

	imshow("Mask", mask);
	//waitKey();
	// vector<Mat> channels;
	// split(hsv,channels);
	// for (int j = 0; j < 3; j++) {
	// 	if (image0.isContinuous()){
	// 		for (int i = 0; i < size; i++) {
	// 			M.data[i] = d[i*3 + j];
	// 		}
	// 	}
	// 	( "Linear Blend", M);
	// 	waitKey(0);
	// }

	M = CannyThreshold(gray);
	imshow("gray channel",M);
	if (image0.isContinuous()){
		for (int i = 0; i < size; i++) {
			uchar b = d[i*3 + 0];
			uchar g = d[i*3 + 1];
			uchar r = d[i*3 + 2];
			if (M.data[i] == 255){
				M.data[i] = 120;
			}else if (r > b && r> g && b < 80 && g < 80 && r > 80){
				M.data[i] = 255;
			}
		}
	}


	vector<KeyPoint> keypoints;
	blob_detector->detect(mask, keypoints);


	vector< pair<KeyPoint, KeyPoint> > pairs;
	find_pairs(pairs, keypoints);
	for (size_t i = 0; i < pairs.size(); i++) {
		KeyPoint first = pairs[i].first;
		KeyPoint second = pairs[i].second;
		//cout << first.pt << "," << second.pt<< endl;
		float rect_height = abs(first.pt.x - second.pt.x)/3;
		float rect_min_x = min(first.pt.x, second.pt.x);
		float rect_min_y = min(first.pt.y, second.pt.y);
		// if (rect_min_y < image0.rows*0.4){
		// 	continue;
		// }

		//cout << pairs.size()<<','<<keypoints.size()<< endl;
		//cout <<
		//rect_min_x<<','<<rect_min_y<<','<<rect_max_x<<','<<rect_max_y
		//<< endl;
		if (abs(first.pt.x-second.pt.x)> 100){
			continue;
		}
		Rect ROI(rect_min_x,
			 rect_min_y,
			 abs(first.pt.x-second.pt.x),
			 rect_height);
		Mat smallImage = Mat(M, ROI);
		vector<Vec2f> lines;
		HoughLines(M, lines, 1, CV_PI/180, 50, 0, 0 );
		bool isRear = false;
		for( size_t i = 0; i < lines.size(); i++ ){
			float rho = lines[i][0], theta = lines[i][1];
			if (!(theta > 3.14/2-0.01 && theta < 3.14/2 + 0.01)){
				continue;
			}
			isRear = true;
			break;
		}
		if (isRear){
			rectangle(image0, ROI, Scalar(0, 255, 0));
		}else{
			//rectangle(image0, ROI, Scalar(0, 0, 255));
		}
	}
	drawKeypoints(image0, keypoints, image0);
//	imshow("Linear", image0);
	//imshow("Linear 2", M);
}


int main(int argc, char *argv[])
{
	Mat src,src_gray;
	string videoFile;
	videoFile=argv[1];
	VideoCapture video;
	namedWindow("output", 1);
	init();

	if(!video.open(videoFile))
		return 1;
	for(;;){
		video>>src;
		//cout << src.rows << ',' << src.cols<< endl;
		if(src.empty())
			break;
		pyrDown(src, src, Size(src.cols/2, src.rows/2));
		car_rear_dection_ROI(src);
		imshow("output",src);
		waitKey(1);
	}
	return 0;
}









