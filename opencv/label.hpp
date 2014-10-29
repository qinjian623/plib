#include <string>
#include <vector>

#ifdef _WIN32
#include <io.h>
#else
#include <dirent.h>
#endif


#include <errno.h>

#include <opencv2/features2d/features2d.hpp>
#include <opencv2/objdetect/objdetect.hpp>


using namespace std;
using namespace cv;

const char path_separator =
#ifdef _WIN32
                            '\\';
#else
                            '/';
#endif

#ifdef _WIN32
struct _finddata_t myfile;

#else
#endif


class Label;
void save_label(String &dir, String &file_name, vector<Label*> &labels);
