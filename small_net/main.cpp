#include <iostream>
#include <vector>
#include <assert.h>
#include <sstream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <cstdio>
using namespace std;

class Matrix2D;
class Net;

enum ActivationFunction{TANH, S, ReLU, NIL};


void sn_relu(double& d){
        if (d < 0){
                d = 0;
        }
}

void sn_nil(double& d){
        return;
}

void sn_tanh(double& d){
        d = std::tanh(d);
}

void sn_sigmoid(double& d){
        d = 1/(1+exp(-d));
}

void sn_random(double& d){
        d = (double)rand() / RAND_MAX * 2 - 1;
}

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
        void apply(void(*f)(double&));

private:
        void resize_data(size_t* s);
        void copy_data(vector < vector<double> >& temp);
        
        // Fields
        size_t size[2];
        vector< vector<double> > data;
        
        
};

void Matrix2D::apply(void (*f)(double&)){
        for(size_t i = 0; i < size[0]; ++i){
                for (size_t j = 0; j < size[1]; ++j) {
                        f(data[i][j]);
                }
        }
}


class Layer
{
public:
        Layer(size_t * size, ActivationFunction f);
        void forward(Matrix2D& input);
private:
        void apply_activation_function(Matrix2D& output);
        ActivationFunction af;
        Matrix2D m;
};

Layer::Layer(size_t *size, ActivationFunction f):m(Matrix2D(size)){
        af = f;
        m.random();
        //cout << m.to_string() << endl;
}

void Layer::apply_activation_function(Matrix2D &output){
        switch(af){
        case TANH:
                output.apply(sn_tanh);
                break;
        case S:
                output.apply(sn_sigmoid);
                break;
        case ReLU:
                output.apply(sn_relu);
                break;
        case NIL:
        default:
                break;
        }
}

void Layer::forward(Matrix2D &input){
        input.mul(m);
        apply_activation_function(input);
}

class Net{
public:
        Net(vector<int>& layers_neuron_counts, vector<ActivationFunction>& activation_functions);
        void forward(Matrix2D& input, Matrix2D& output);
private:
        vector<Layer> layers;
        //vector<Matrix2D> layers;
};

Net::Net(vector<int>& layers_neuron_counts, vector<ActivationFunction>& activation_functions){
        assert(layers_neuron_counts.size() > 1);
        assert(activation_functions.size() == layers_neuron_counts.size() - 1);
        layers.clear();
        size_t s[2];
        for(size_t i = 0; i < layers_neuron_counts.size() - 1; ++i){
                s[0] = layers_neuron_counts[i];
                s[1] = layers_neuron_counts[i+1];
                layers.push_back(Layer(s, activation_functions[i]));
        }
}

void Net::forward(Matrix2D& input, Matrix2D& output){
        assert(layers.size() > 0);
        output.clone(input);
        for(size_t i = 0; i < layers.size(); ++i){
                layers[i].forward(output);
                //cout << output.to_string() << endl;
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
        srand (time(NULL));
        apply(sn_random);
}

string Matrix2D::to_string(){
        stringstream ss;
        ss << "Matrix: size = " << size[0] << "," << size[1] << endl;
        for(size_t i = 0; i < size[0]; ++i){
                for(size_t j = 0; j < size[1]; ++j){
                        ss << data[i][j] << ", ";
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
        // FIXME This function can only work when the first dimension does NOT change.
        // If resize to a larger size, new created data[i] will need to be initialized.
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
        int ta[3] = {400, 400*2, 1};
        vector<int> arch(&ta[0], &ta[0]+3);
        ActivationFunction taf[9] = {TANH, TANH, ReLU, ReLU, ReLU, ReLU, ReLU, ReLU, TANH};
        vector<ActivationFunction> afs(&taf[0], &taf[0]+2);
        Net net(arch, afs);

        size_t in_size[2] = {1, ta[0]};
        size_t out_size[2] = {1, 1};
        Matrix2D in(&in_size[0]);
        in.random();
        in.fill(1);
        Matrix2D out(&out_size[0]);

        //cout << in.to_string() << endl;
        clock_t t = clock();
        net.forward(in, out);
        t = clock() - t;
        printf ("It took me %ld clicks (%f seconds).\n",t,((float)t)/CLOCKS_PER_SEC);
        cout << out.to_string() << endl;
        return 0;
}

