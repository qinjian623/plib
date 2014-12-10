#include <iostream>
#include <vector>
#include <assert.h>
#include <sstream>
#include <random>

using namespace std;

class Matrix2D;
class Net;

enum ActiveFunction{tanh, sigmoid, LeRU};

class Matrix2D
{
public:
        Matrix2D(size_t*s);
        void clone(Matrix2D& m);
        void mul(Matrix2D& m);
        // void mul(double f);
        // void mul(int d);
        
        void zero();
        void fill(double d);
        void random();
        string to_string();
        
        
private:
        void resize_data(size_t* s);
        void copy_data(vector < vector<double> >& temp);
        
        // Fields
        size_t size[2];
        vector< vector<double> > data;
        
        
};

class Net{
public:
        Net(vector<int> layers_neuron_counts);
        void forward(Matrix2D& input, Matrix2D& output);
private:
        vector<Matrix2D> layers;
};


void Net::forward(Matrix2D& input, Matrix2D& output){
        assert(layers.size() > 0);
        output.clone(input);
        for(size_t i = 0; i < layers.size(); ++i){
                output.mul(layers[i]);
        }
}


void Matrix2D::clone(Matrix2D& m){
        size[0] = m.size[0];
        size[1] = m.size[1];
        data.resize(size[0]);
        for(size_t i = 0; i < size[0]; ++i){
                data[i] = m.data[i];
        }
}

void Matrix2D::random(){
        std::srand(std::time(0));
        
}

string Matrix2D::to_string(){
        stringstream ss;
        ss << "Matrix: size = " << size[0] << "," << size[1] << endl;
        for(size_t i = 0; i < size[0]; ++i){
                for(size_t j = 0; j < size[1]; ++j){
                        ss << data[i][j] << ",";
                }
                ss << endl;
        }
        return ss.str();
}

void Matrix2D::fill(double d){
        for(size_t i = 0; i < size[0]; ++i){
                for (size_t j = 0; j < size[1]; ++j) {
                        data[i][j] = d;
                }
        }
}

void Matrix2D::zero(){
        fill(0.00000);
}

Matrix2D::Matrix2D(size_t *s){
        data.resize(s[0]);
        for(size_t i = 0; i < s[0];++i){
                data[i] = vector<double>(s[1]);
        }
        size[0] = s[0];
        size[1] = s[1];
}

void Matrix2D::resize_data(size_t* s){
        data.resize(s[0]);
        for(size_t i = 0; i < size[0]; ++i){
                data[i].resize(s[1]);
        }
}

void Matrix2D::mul(Matrix2D &m){
        assert(size[1] == m.size[0]);
        if (size[1] != m.size[0]){
                cout << "Error" << endl;
                return;
        }
        vector< vector<double> > temp(size[0], vector<double>(size[1]));
        copy_data(temp);
        size_t new_size[2] = {size[0], m.size[1]};

        resize_data(new_size);

        for(size_t i = 0; i < new_size[0]; ++i){
                for(size_t j = 0; j < new_size[1]; ++j){
                        // i-th row of this * j-th cols of m
                        double sum = 0.0;
                        for(size_t k = 0; k < size[1]; ++k){
                                sum += temp[i][k] * m.data[k][j];
                        }
                        data[i][j] = sum;
                }
        }

        size[0] = new_size[0];
        size[1] = new_size[1];
}

void Matrix2D::copy_data(vector < vector<double> >& temp){
        for(size_t i = 0; i < size[0]; ++i){
                for(size_t j = 0; j < size[1]; ++j){
                        temp[i][j] = data[i][j];
                }
        }
}


void test_function( vector< vector <int> > &vv){
        vv.resize(3);
        vv[0] = vector<int>(3);
        vv[1] = vector<int>(3);
        vv[2] = vector<int>(3);
}

int main()
{
        size_t size[2] = {2, 2};
        Matrix2D m(size);
        m.fill(1.33);

        size[1] = 10;
        Matrix2D m1(size);
        m1.fill(3.21);
        m.mul(m1);
        cout << m.to_string() << endl;
        return 0;
}

