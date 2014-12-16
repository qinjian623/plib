/*
  TODO training
  TODO bias
  */


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
        Matrix2D(size_t rows, size_t cols);
        Matrix2D(size_t*s);
        void clone(Matrix2D& m);
        void mul(Matrix2D& m);
        void mul(double& d);
        void sub(Matrix2D& m);
        void add(Matrix2D& m);
        void mul_transpose(Matrix2D& m);
        // void mul(double f);
        // void mul(int d);
        
        void zero();
        void fill(double d);
        void random();
        string to_string();
        void apply(void(*f)(double&));
        void set(size_t row, size_t col, double val);
        double get(size_t row, size_t col);
        void resize(size_t row, size_t col);
        size_t rows();
        size_t cols();
private:
        void init(size_t rows, size_t cols);
        void resize_data(size_t* s);
        void resize_data(size_t rows, size_t cols);
        void copy_data(vector < vector<double> >& temp);
        
        // Fields
        size_t size[2];
        vector< vector<double> > data;

};


void Matrix2D::mul(double &d){
        for(size_t i = 0; i < data.size(); ++i){
                for(size_t j = 0; j < data[i].size(); ++j){
                        data[i][j] *= d;
                }
        }
}

void Matrix2D::resize(size_t rows, size_t cols){
        resize_data(rows, cols);
        this->size[0] = rows;
        this->size[1] = cols;
}

size_t Matrix2D::rows(){
        return size[0];
}
size_t Matrix2D::cols(){
        return size[1];
}

double Matrix2D::get(size_t row, size_t col){
        return data[row][col];
}

void Matrix2D::sub(Matrix2D &m){
        assert(m.size[0] == size[0] && m.size[1] == size[1]);
        for(size_t i = 0; i < size[0]; ++i){
                for(size_t j = 0; j < size[1]; ++j){
                        data[i][j] -= m.get(i, j);//m.size[i][j];
                }
        }
}

void Matrix2D::add(Matrix2D &m){
        assert(m.size[0] == size[0] && m.size[1] == size[1]);
        for(size_t i = 0; i < size[0]; ++i){
                for(size_t j = 0; j < size[1]; ++j){
                        data[i][j] += m.get(i, j);//m.size[i][j];
                }
        }
}

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
        friend class Net;
        void prepare_training();
        Layer(size_t * size, ActivationFunction f);
        void forward(Matrix2D& input);
        void training_forward(Matrix2D& input);

        void reset();

        string to_string();
private:

        void add_bias(Matrix2D& input);
        void apply_activation_function(Matrix2D& output);
        ActivationFunction af;
        Matrix2D m;
        // For training.
        Matrix2D* D;
        Matrix2D* O;
        // TODO 未来可以考虑使用vector节约内存使用
        //vector<double> *D;
};

string Layer::to_string(){
        stringstream ss;
        ss << m.to_string();
        ss << af;
        return ss.str();
}
void Layer::reset(){
        O->resize(m.rows(), 1);
        D->resize(m.cols(), m.cols());
}

void Layer::prepare_training(){
        O = new Matrix2D(m.rows(), 1);
        // bias
        D = new Matrix2D(m.cols(), m.cols());
}

/**
 * TODO bias bug
 * @brief Layer::training_forward
 * @param input
 */
void Layer::training_forward(Matrix2D &input){
        assert(D!=NULL);
        assert(D->rows() == D->cols() && D->cols() == m.cols());

        add_bias(input);
        for(size_t i = 0; i < input.cols(); ++i){
                O->set(i, 0, input.get(0, i));
        }
        // same as forward(input);
        input.mul(m);
        apply_activation_function(input);


        assert(input.rows() == 1);
        D->zero();
        for(size_t i = 0; i < input.cols() ; ++i){
                double o = input.get(0, i);
                // double o = input.data[0][i];
                D->set(i, i, 1-o*o); // Sigmoid ::o*(1-o)
        }
}

Layer::Layer(size_t *size, ActivationFunction f):m(Matrix2D(size)){
        af = f;
        m.random();
        D = NULL;
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

void Layer::add_bias(Matrix2D& input){
        // bias
        input.resize(input.rows(), input.cols()+1);
        for(size_t i = 0; i < input.rows(); ++i){
                input.set(i, input.cols()-1 ,1);
        }
}
void Layer::forward(Matrix2D &input){
        add_bias(input);
        input.mul(m);
        apply_activation_function(input);
}

class Net{
public:
        Net(vector<int>& layers_neuron_counts, vector<ActivationFunction>& activation_functions);
        void forward(Matrix2D& input, Matrix2D& output);
        void train(Matrix2D& input, Matrix2D& label);
        void prepare_training(const double& step);

        void dump();

private:
        void reset();
        void backward(Matrix2D& error);
        void training_forward(Matrix2D& input, Matrix2D& output);
        void update();
        double step;
        vector<Layer> layers;
        //vector<Matrix2D> layers;
};

void Net::dump(){
        for(vector<Layer>::iterator it = layers.begin(); it!= layers.end(); ++it){
                cout << (*it).to_string()<< endl;
        }
}
void Net::reset(){
        for(vector<Layer>::iterator it = layers.begin(); it!= layers.end(); ++it){
                        (*it).reset();
        }
}

void Net::prepare_training(const double& s){
        for(vector<Layer>::iterator it = layers.begin(); it != layers.end(); ++it){
                (*it).prepare_training();
        }
        this->step = s;
}

void Net::backward(Matrix2D &error){
        assert(layers.size() > 1);
        // Output layer.
        error.mul(*layers.back().D);
        //layers.back().D->clone(error);
        layers.back().O->mul(error);
        for(size_t i = layers.size() - 2;; --i){
                error.mul_transpose(layers[i + 1].m);
                error.mul_transpose(*layers[i].D);
                layers[i].O->mul(error);
                //layers[i].D->clone(error);
                if (i == 0) break;
        }
}

void Net::training_forward(Matrix2D &input, Matrix2D &output){
        assert(layers.size() > 0);
        output.clone(input);
        for(size_t i = 0; i < layers.size(); ++i){
                layers[i].training_forward(output);
                //layers[i].forward(output);
        }
}


void Net::update(){
        for(size_t i = 0; i < layers.size(); ++i){
                assert(layers[i].m.rows() == layers[i].O->rows() &&
                       layers[i].m.cols() == layers[i].O->cols());
                layers[i].O->mul(step);
                //cout << "Weights update..." << endl;
                //cout << layers[i].O->to_string() << endl;
                layers[i].m.sub(*layers[i].O);
        }
}
void Net::train(Matrix2D &input, Matrix2D &label){

        // Feed forward
        Matrix2D output(label.rows(), label.cols());
        training_forward(input, output);
        cout << "Output ============" << endl;
        cout << output.to_string() << endl;
        // Derivatives of Loss
        output.sub(label);

        double sum = 0.0;
        for(size_t i = 0; i < output.rows(); ++i){
               for(size_t j = 0; j < output.cols(); ++j){
                       sum += output.get(i, j)*output.get(i, j);
               }
        }
        cout << "Loss ========>"<< sum << endl;
        // Backward
        backward(output);
        // Update weights
        update();
        reset();
}

Net::Net(vector<int>& layers_neuron_counts, vector<ActivationFunction>& activation_functions){
        assert(layers_neuron_counts.size() > 1);
        assert(activation_functions.size() == layers_neuron_counts.size() - 1);
        layers.clear();
        size_t s[2];
        for(size_t i = 0; i < layers_neuron_counts.size() - 1; ++i){
                // features + bias
                s[0] = layers_neuron_counts[i] + 1;
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
        ss << "[";
        for(size_t i = 0; i < size[0]; ++i){
                for(size_t j = 0; j < size[1]; ++j){
                        ss << data[i][j] << ", ";
                }
                ss << ";"<< endl;
        }
        ss << "]";
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


Matrix2D::Matrix2D(size_t rows, size_t cols){
        init(rows, cols);
}

void Matrix2D::init(size_t rows, size_t cols){
        data.resize(rows);
        for(size_t i = 0; i < rows; ++i){
                data[i] = vector<double>(cols);
        }
        size[0] = rows;
        size[1] = cols;
}

Matrix2D::Matrix2D(size_t *s){
        init(s[0], s[1]);
}

void Matrix2D::resize_data(size_t* s){
        resize_data(s[0], s[1]);
}

void Matrix2D::resize_data(size_t rows, size_t cols){
        // FIXME This function can only work when the first dimension does NOT change.
        // If resize to a larger size, new created data[i] will need to be initialized.
        data.resize(rows);
        for(size_t i = 0; i < size[0]; ++i){
                data[i].resize(cols);
        }
}


void Matrix2D::set(size_t row, size_t col, double val){
        assert(row >= 0 && row < this->size[0] && col >= 0 && col < this->size[1]);
        data[row][col] = val;
}


void Matrix2D::mul_transpose(Matrix2D &m){
        //cout << size[1] << ",," << m.size[1] << endl;
        assert(size[1] == m.size[1]);
        if (size[1] != m.size[1]){
                cout << "Error" << endl;
                return;
        }
        vector< vector<double> > temp(size[0], vector<double>(size[1]));
        copy_data(temp);
        size_t new_size[2] = {size[0], m.size[0]};
        resize_data(new_size);

        for(size_t i = 0; i < new_size[0]; ++i){
                for(size_t j = 0; j < new_size[1]; ++j){
                        // i-th row of this * j-th cols of m
                        double sum = 0.0;
                        for(size_t k = 0; k < size[1]; ++k){
                                sum += temp[i][k] * m.data[j][k];
                        }
                        data[i][j] = sum;
                }
        }

        size[0] = new_size[0];
        size[1] = new_size[1];

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


void build_xor_training_set(vector<Matrix2D*>& xs, vector<Matrix2D*>& ys){
        Matrix2D* x, *y;
        xs.resize(4);
        ys.resize(4);

        x = new Matrix2D(1, 2);
        x->set(0, 0, 0.0001);
        x->set(0, 1, 0.0001);
        y = new Matrix2D(1, 1);
        y->set(0, 0, -1);
        xs[0] = x;
        ys[0] = y;


        x = new Matrix2D(1, 2);
        x->set(0, 0, 1);
        x->set(0, 1, 1);
        y = new Matrix2D(1, 1);
        y->set(0, 0, 1);
        xs[1] = x;
        ys[1] = y;

        x = new Matrix2D(1, 2);
        x->set(0, 0, 0.0001);
        x->set(0, 1, 1);
        y = new Matrix2D(1, 1);
        y->set(0, 0, -1);
        xs[2] = x;
        ys[2] = y;

        x = new Matrix2D(1, 2);
        x->set(0, 0, 1);
        x->set(0, 1, 0.0001);
        y = new Matrix2D(1, 1);
        y->set(0, 0, -1);
        xs[3] = x;
        ys[3] = y;
}

int main()
{
        int ta[4] = {2, 4, 1, 1};
        vector<int> arch(&ta[0], &ta[0]+3);
        ActivationFunction taf[9] = {TANH, TANH, TANH, TANH, ReLU, ReLU, ReLU, ReLU, TANH};
        vector<ActivationFunction> afs(&taf[0], &taf[0]+2);
        Net net(arch, afs);

        size_t in_size[2] = {1, ta[0]};
        size_t out_size[2] = {1, 1};
        Matrix2D in(&in_size[0]);
        in.random();
        //in.fill(1);
        Matrix2D out(&out_size[0]);

        net.prepare_training(0.000001);

        vector<Matrix2D*> xs;
        vector<Matrix2D*> ys;
        build_xor_training_set(xs, ys);

        std::srand(time(NULL));

        net.dump();
        net.forward(in, out);
        cout << in.to_string() << endl;
        cout << out.to_string() << endl;

        for (int var = 0; var < 10000; ++var) {
                int i= std::rand()%4;
                //cout << "Input & Label ====================" << endl;
                //
                //net.forward(*xs[i], out);
                //cout << out.to_string() << endl;
                net.train(*xs[i], *ys[i]);
        }
        //cout << "Network dumping ...." << endl;
        //net.dump();
        //exit(0);
        //cout << in.to_string() << endl;
        clock_t t = clock();
        for(int i = 0; i < 4; ++i){
                net.forward(*xs[i], out);
                cout << "--------------------------------"<<endl;
                cout << "X = ";
                cout << xs[i]->to_string() << endl;
                cout << "Y = ";
                cout << ys[i]->to_string() << endl;
                cout << "H(x) = ";
                cout << out.to_string() << endl;
        }
        //net.forward(in, out);
        t = clock() - t;
        printf ("It took me %ld clicks (%f seconds).\n",t,((float)t)/CLOCKS_PER_SEC);
        return 0;
}

