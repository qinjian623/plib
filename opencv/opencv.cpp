#include "stdio.h"
#include <opencv2/opencv.hpp>

using namespace cv;

Mat LUT_test(Mat &in){
	Mat out;
	uchar table[256];
	int divideWith = 2;
	for (int i = 0; i < 256; ++i)
		table[i] = divideWith* (i/divideWith);
	Mat lookUpTable(1, 256, CV_8U);
	uchar* p = lookUpTable.data;
	for( int i = 0; i < 256; ++i)
		p[i] = table[i];
	LUT(in, lookUpTable, out);
	return out;
}

Mat CannyThreshold(Mat &src_gray)
{
	Mat detected_edges;
	/// 使用 3x3内核降噪
	blur(src_gray, detected_edges, Size(3,3));
	/// 运行Canny算子
	Canny( detected_edges, detected_edges, 50, 50*3, 3);
	return detected_edges;
}


int main(int argc, char** argv)
{
	Mat image0;
	Mat image1;
	image0 = imread(argv[1], 1);
	namedWindow("Linear Blend", 1);
	uchar* d = image0.data;
	int size = image0.rows*image0.cols;

	Mat M(image0.rows,image0.cols, CV_8UC1, Scalar(0,0,255));

	// for (int j = 0; j < 3; j++) {
	// 	if (image0.isContinuous()){
	// 		for (int i = 0; i < size; i++) {
	// 			M.data[i] = d[i*3 + j];
	// 		}
	// 	}
	// 	imshow( "Linear Blend", M);
	// 	waitKey(0);
	// }

	Mat dst, src_gray;
	dst.create( image0.size(), image0.type() );

	/// 原图像转换为灰度图像
	cvtColor( image0, src_gray, CV_BGR2GRAY );
	imshow( "Linear Blend", image0);
	waitKey();

	M = CannyThreshold(src_gray);
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
	imshow( "Linear Blend", M);
	if (argc == 3){
		imwrite(argv[2], M);
	}
	waitKey(0);
	return 0;
}









