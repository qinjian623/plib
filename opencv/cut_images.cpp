#include <opencv2/opencv.hpp>
#include <ctime>
#include <cstdlib>

using namespace cv;


void gen_random(char *s, const int len) {
    static const char alphanum[] =
        "0123456789"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz";

    for (int i = 0; i < len; ++i) {
        s[i] = alphanum[rand() % (sizeof(alphanum) - 1)];
    }
    s[len] = '.';
    s[len+1] = 'j';
    s[len+2] = 'p';
    s[len+3] = 'g';
    s[len+4] = 0;
}

int main(int argc, char *argv[])
{
	Mat big_one;
	int big_height = 300;
	int big_width = 400;
	int small_size = 50;
	big_one = imread(argv[1], 1);
	int small_images_count = 10;
	std::srand(std::time(0));
	char name[100];

	for (int i = 0; i < small_images_count; i++) {
		int height = std::rand()%(big_height - small_size);
		int width = std::rand()%(big_width - small_size);
		Mat small_one = Mat(big_one, Rect(width, height, small_size, small_size));
		Mat down_sample;
		pyrDown(small_one, down_sample, Size( small_size /2, small_size/2 ) );
		gen_random(name, 20);
		imwrite(name, down_sample);
	}
	return 0;
}












