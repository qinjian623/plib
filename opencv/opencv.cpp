#include "stdio.h"
#include <opencv2/opencv.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <utility>
#include <cmath>


using namespace cv;
using namespace std;


SimpleBlobDetector::Params params;
Ptr<FeatureDetector> blob_detector;
int canny_thread;
int pair_thread = 5;
class SymmetryDetector
{
	public:
	SymmetryDetector(Mat mat){
		for(int i = 0; i < mat.cols; i++){
			int sum = 0;
			for(int j = 0; j < mat.rows; j++){
				sum += g(mat, j, i);
			}
			h[i] = sum;
		}
	}

	private :
	vector<int> h;
	uchar get(Mat mat, int x, int y){
		return mat.data[y*mat.cols+x];
	}
	float avg;
	uchar f(Mat mat, int x, int y){
		return get(mat, x, y);
	}

	int g(Mat mat, int x, int y){
		return abs((f(mat, x+1, y-1) + 2*f(mat, x+1 , y ) + f(mat, x+1, y+1))
			   - (f(mat, x-1, y-1) + 2*f(mat, x-1, y) + f(mat, x-1 , y+1)));
	}

	int G(vector<int> axis, int x){
		return axis[x];
	}

	float O(vector<int> axis, int u, int x_s){
		return (G(axis, x_s+u) - G(axis, x_s-u))/2;
	}

	float E(vector<int> axis, int u, int x_s){
		return (G(axis, x_s+u) + G(axis, x_s-u))/2;
	}

	float E_n(){
	}

	int u(int x, int x_s){
		return x - x_s;
	}
};

void init()
{
	params.minDistBetweenBlobs = 1.0f;
	params.filterByInertia = false;
	params.filterByConvexity = false;
	params.filterByColor = true;
	params.filterByCircularity = false;
	params.filterByArea = true;
	params.blobColor = 255;
	params.minArea = 2.0f;
	params.maxArea = 10000.0f;
	params.minConvexity = 0.3f;
	params.maxConvexity = 100.0f;
	blob_detector= new SimpleBlobDetector(params);
	blob_detector->create("SimpleBlob");

	canny_thread = 40;
	pair_thread = 5;
}

bool in_range(float value, float s, float e)
{
	if (value >= s && value < e){
		return true;
	}else{
		return false;
	}
}


void find_pairs(vector< pair<KeyPoint, KeyPoint> > & pairs, vector<KeyPoint> & keypoints){
	for (size_t i = 0; i < keypoints.size(); i++) {
		for (size_t j = i; j < keypoints.size(); j++) {
			if (i == j){
				continue;
			}
			float y0 = keypoints[i].pt.y;
			float y1 = keypoints[j].pt.y;
			if (abs(y0-y1)< pair_thread){
				pairs.push_back(make_pair(keypoints[i],keypoints[j]));
			}
		}
	}
}

Mat CannyThreshold(Mat &gray)
{
	Mat detected_edges;
	/// 使用 3x3内核降噪
	blur(gray, detected_edges, Size(3,3));
	/// 运行Canny算子
	Canny(detected_edges, detected_edges, canny_thread, canny_thread*3, 3);
	return detected_edges;
}

float calc_distance_thread(float x, float row, float col)
{
	return 3.0/7.0*col/row*x - 9.0/70.0*col;
	//return 10.0/7.0*col/row*x - (3.0/7.0*col);
	//return 10.0/30.0*x;
}






void print_his(Mat small)
{
	cout << "=================================" << endl;
	vector<int> h;
	cout << small.cols << endl;
	for(int i = 0; i < small.cols; i++){
		int sum = 0;
		for(int j = 0; j < small.rows; j++){
			//sum += g(small, j, i);
		}
		cout << sum << endl;
	}

}

void car_rear_dection_ROI(Mat &image0)
{
	int col = image0.cols;
	int row = image0.rows;
	uchar* d = image0.data;
	int size = image0.rows*image0.cols;
	Mat M(image0.rows,image0.cols, CV_8UC1, Scalar(0,0,255));
	Mat hsv, gray, mask1, mask0, mask, blured, sobel;

	// 去除左上和右上角
	if (image0.isContinuous()){
		for (int x = 0; x < image0.cols/3; x++){
			for (int y = 0; y< image0.rows/3;y++){
				int i = x+y*image0.cols;
				d[i*3] = 255;
				d[i*3+1] = 255;
				d[i*3+2] = 255;
			}
		}
		for (int x = image0.cols/3*2; x < image0.cols; x++){
			for (int y = 0; y< image0.rows/3;y++){
				int i = x+y*image0.cols;
				d[i*3] = 255;
				d[i*3+1] = 255;
				d[i*3+2] = 255;
			}
		}
	}
	//blur(hsv, hsv, Size(3, 3));
	// 灰度空间
	cvtColor(image0, gray, CV_BGR2GRAY);
	Sobel(gray, sobel, CV_8U, 1, 0);
	imshow("sobel", sobel);
	// 边界检测，以准备下一步的hough变换
	M = CannyThreshold(sobel);

	// 模糊以减少噪音
	// hsv空间，以更好的过滤红色
	blur(image0, blured, Size(5,5));
	cvtColor(blured, hsv, CV_BGR2HSV);
	// 获得过滤红色的mask
	inRange(hsv, Scalar(165, 60, 0),Scalar(180, 255, 255), mask1);
	inRange(hsv, Scalar(0, 60, 0),Scalar(5, 255, 255), mask0);
	cv::bitwise_or(mask0, mask1, mask);

	vector<Vec2f> all_lines;
	HoughLines(M, all_lines, 1, CV_PI/180, 75, 0, 0);

	// if (image0.isContinuous()){
	// 	for (int i = 0; i < size; i++) {
	// 		uchar b = d[i*3 + 0];
	// 		uchar g = d[i*3 + 1];
	// 		uchar r = d[i*3 + 2];
	// 		if (M.data[i] == 255){
	// 			//M.data[i] = 255;
	// 		}else if (r > b && r> g && b < 80 && g < 80 && r > 80){
	// 			//M.data[i] = 255;
	// 		}
	// 	}
	// }


	vector<KeyPoint> keypoints;
	blob_detector->detect(mask, keypoints);
	//blob_detector->detect(gray, keypoints);

	vector< pair<KeyPoint, KeyPoint> > pairs;
	find_pairs(pairs, keypoints);

	for (size_t i = 0; i < pairs.size(); i++) {
		KeyPoint first = pairs[i].first;
		KeyPoint second = pairs[i].second;
		//cout << first.pt << "," << second.pt<< endl;
		float rect_height = abs(first.pt.x - second.pt.x)/3;
		float rect_min_x = min(first.pt.x, second.pt.x);
		float rect_min_y = min(first.pt.y, second.pt.y);
		if (rect_min_y < image0.rows*0.33){
		 	continue;
		}
		//cout << pairs.size()<<','<<keypoints.size()<< endl;
		//cout <<
		//rect_min_x<<','<<rect_min_y<<','<<rect_max_x<<','<<rect_max_y
		//<< endl;
		float distance = abs(first.pt.x-second.pt.x);
		float distance_thredhold = calc_distance_thread(rect_min_y, row, col);// - (3.0/7.0*col);
		// 200? (rect_min_y/image0.rows * 200?
		//if (distance> 100 || distance < 20){
		if (distance> 800 || distance < 20){
			continue;
		}
		// TODO 调整参数的问题
		//if (distance > distance_thredhold*2 || distance < distance_thredhold){
//			continue;
//		}

		Rect ROI(max(0.0f, rect_min_x - 10),
			 rect_min_y,
			 min(abs(first.pt.x-second.pt.x)+20, image0.cols - rect_min_x),
			 min(rect_height, image0.rows - rect_min_y));
		Mat smallImage = Mat(gray, ROI);
		// TODO
		//print_his(smallImage);
		//imshow("small gray", smallImage);
		smallImage = Mat(M, ROI);
		vector<Vec2f> lines;
		HoughLines(M, lines, 1, CV_PI/180, 50, 0, 0 );
		bool isRear = false;
		for( size_t i = 0; i < lines.size(); i++ ){
			float theta = lines[i][1];
			//TODO 横线检测，0度的问题
			if (!(theta > 3.14/2-0.01 && theta < 3.14/2 + 0.01)){
				continue;
			}
			isRear = true;
			break;
		}
		if (isRear){
			rectangle(image0, ROI, Scalar(0, 0, 255),2);
		}else{
			//rectangle(image0, ROI, Scalar(0, 0, 255));
		}
	}
	for( size_t i = 0; i < all_lines.size(); i++ ){
		float theta = all_lines[i][1];
		if (in_range(theta, 1.3-0.2,1.3+0.2) || in_range(theta, 2.0-0.2, 2.0+0.2)){
			float rho = all_lines[i][0];
			Point pt1, pt2;
			double a = cos(theta), b = sin(theta);
			double x0 = a*rho, y0 = b*rho;
			pt1.x = cvRound(x0 + 1000*(-b));
			pt1.y = cvRound(y0 + 1000*(a));
			pt2.x = cvRound(x0 - 1000*(-b));
			pt2.y = cvRound(y0 - 1000*(a));
			//line( image0, pt1, pt2, Scalar(0,255,0), 1, CV_AA);
		}
	}
	for (int i =0; i < image0.cols;i++){
		float d = calc_distance_thread(i, row, col);
		Point pt1(0,i),pt2(d,i);
		//line( image0, pt1, pt2, Scalar(0,255,0), 1, CV_AA);
	}
	imshow("Mask", mask);
	imshow("Canny",M);
	drawKeypoints(image0, keypoints, image0);
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
		//exit(0);
	}
	return 0;
}

