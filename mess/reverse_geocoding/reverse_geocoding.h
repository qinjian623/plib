#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <vector>
#include <pcl/kdtree/kdtree_flann.h>


using namespace std;
using namespace pcl;

KdTreeFLANN<PointXY>* build_index(char* index_file);
