#include "reverse_geocoding.h"


KdTreeFLANN<PointXY>* build_index(char* index_file){
	vector<long> ids;
	vector<float> xs;
	vector<float> ys;

	string line;
	string cell;

	ifstream ll_file(index_file);

	while(getline(ll_file, line)){
		stringstream lineStream(line);
		getline(lineStream, cell, ',');
		ids.push_back(atol(cell.c_str()));
		getline(lineStream, cell, ',');
		xs.push_back(atof(cell.c_str()));
		getline(lineStream, cell, ',');
		ys.push_back(atof(cell.c_str()));
	}

	long data_size = ids.size();
	PointCloud<pcl::PointXY>::Ptr cloud (new PointCloud<pcl::PointXY>);
	cloud->width = data_size;
	cloud->height = 1;
	cloud->points.resize (cloud->width * cloud->height);

	for (int i = 0; i < data_size; i++) {
		cloud->points[i].x = xs[i];
		cloud->points[i].y = ys[i];
	}

	KdTreeFLANN<PointXY> *kdtree = new KdTreeFLANN<PointXY>;
	kdtree->setInputCloud (cloud);
	cout << "build_index" << endl;
	return kdtree;
}


int main_t(int argc, char *argv[])
{
	char* file = "/home/qin/data_base/reverse_gc_no_bom";
	vector<long> ids;
	vector<float> xs;
	vector<float> ys;

	string line;
	string cell;

	ifstream ll_file(file);

	while(getline(ll_file, line)){
		stringstream lineStream(line);
		getline(lineStream, cell, ',');
		ids.push_back(atol(cell.c_str()));
		getline(lineStream, cell, ',');
		xs.push_back(atof(cell.c_str()));
		getline(lineStream, cell, ',');
		ys.push_back(atof(cell.c_str()));
	}

	long data_size = ids.size();
	pcl::PointCloud<pcl::PointXY>::Ptr cloud (new pcl::PointCloud<pcl::PointXY>);
	cloud->width = data_size;
	cloud->height = 1;
	cloud->points.resize (cloud->width * cloud->height);

	for (int i = 0; i < data_size; i++) {
		cloud->points[i].x = xs[i];
		cloud->points[i].y = ys[i];
	}

	KdTreeFLANN<pcl::PointXY> *kdtree;
	kdtree = build_index(file);
	//kdtree.setInputCloud (cloud);


	vector<pcl::PointXY> searchPoints;
	for (size_t i = 0; i < data_size; i++) {
		pcl::PointXY point;
		point.x = xs[i] + 0.001;
		point.y = ys[i] + 0.00001;
		searchPoints.push_back(point);
	}

	cout << "Data size: "<<data_size << endl;
	// K nearest neighbor search
	int K = 1;
	vector<int> pointIdxNKNSearch(K);
	vector<float> pointNKNSquaredDistance(K);

	// std::cout << "K nearest neighbor search at (" << searchPoint.x
	// 	  << " " << searchPoint.y
	// 	  << ") with K=" << K << std::endl;
	clock_t start;
	double duration;
	start = clock();
	for (size_t i = 0; i < data_size; i++) {
		if ( kdtree->nearestKSearch (searchPoints[i], K, pointIdxNKNSearch, pointNKNSquaredDistance) <= 0 ){

			cout << "error" << endl;
			// for (size_t i = 0; i < pointIdxNKNSearch.size (); ++i)
			// 	std::cout << "    "  <<   cloud->points[ pointIdxNKNSearch[i] ].x
			// 		  << " " << cloud->points[ pointIdxNKNSearch[i] ].y
			// 		  << " (squared distance: " << pointNKNSquaredDistance[i] << ")"
			// 		  << std::endl;
		}
// cout << pointNKNSquaredDistance.at(0) << endl;
	}
	duration = ( std::clock() - start ) / (double) CLOCKS_PER_SEC;
	std::cout<<"Takes time: "<< duration <<"s\n";
	return 0;
}


