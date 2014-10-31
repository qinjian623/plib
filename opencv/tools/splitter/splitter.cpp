#include <string>
#include <fstream>

#include <stdlib.h>

#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <opencv2/objdetect/objdetect.hpp>

using namespace cv;
using namespace std;

double ratio = -1.0;

typedef std::string String;

void split(const std::string &s,
                char delim,
                vector<std::string> &elems) {
        stringstream ss(s);
        string item;
        while (std::getline(ss, item, delim)) {
            elems.push_back(item);
        }
}

Rect* parse_roi(String roi_str){
        vector<String> pos;
        split(roi_str, ',', pos);
        vector<int> pos_int;
        for(size_t i = 0; i < pos.size(); ++i){
                pos_int.push_back(atoi(pos[i].c_str()));
        }
        if(pos_int[2]<0 || pos_int[3]<0){
                return NULL;
        }
        if (ratio < 0){
                return (new Rect(pos_int[0], pos_int[1], pos_int[2], pos_int[3]));
        }else{
                return (new Rect(pos_int[0], pos_int[1], pos_int[2], pos_int[2] * ratio));
        }
}

int cut_pic(Mat img, String& roi_str, Mat& small){
        Rect* roi= parse_roi(roi_str);
        if (roi == NULL){
                return -1;
        }
        small= Mat(img, (*roi));
        delete roi;
        return 1;
}

inline Mat load_pic(const String& dir, const String & name){
        return imread(dir+name);
}


inline void write_pic(const Mat& img, const String& path){
        imwrite(path, img);
}

int main(int argc, char **argv) {
        assert(argc >= 4);
        char number_buffer[33];

        String meta_file_path = argv[1];
        String pics_dir = argv[2];
        String output_dir = argv[3];
        if (argc == 5){
                ratio = atof(argv[4]);
        }

        vector<String> file_names;
        ifstream meta_file(meta_file_path.c_str());
        String line;
        while(getline(meta_file, line)){
                vector<string> tokens;
                split(line, ' ', tokens);
                String pic_name = tokens[0];
                cout << "File:" << pic_name << endl;
                Mat img = load_pic(pics_dir, pic_name);
                for (size_t i = 1; i < tokens.size(); ++i) {
                        sprintf(number_buffer, "%d", i);
                        Mat small;
                        if (cut_pic(img, tokens[i], small) < 0){
                                continue;
                        }
                        write_pic(small, output_dir+'/'+pic_name+String(number_buffer)+".jpg");
                }
        }
        cout << "Mission Completed" << endl;
}



