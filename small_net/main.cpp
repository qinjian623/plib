#include "main.h"

int main()
{

        cout << "Program start." << endl;
        Net* n = load_model("/home/qin/model.txt");
        int training_size = 50000;
        int test_size = 5000;

        int ta[6] = {30*30, 30*30, 30*30/4, 30*30/8, 1, 1};
        vector<int> arch(&ta[0], &ta[0]+5);
        ActivationFunction taf[9] = {TANH, TANH, TANH, TANH, TANH, TANH, ReLU, ReLU, TANH};
        vector<ActivationFunction> afs(&taf[0], &taf[0]+4);
        //Net net(arch, afs);
        //net.prepare_training(0.001);


        cout << "Loading dataset..." << endl;
        vector< pair<Matrix2D*, Matrix2D*> > dataset;
        read_vector_file(string("/home/qin/workspace_c/qt_1/build-mat_dump-Desktop_Qt_Qt_Version_GCC_64bit-Debug/all_shuf.txt"), dataset, training_size + test_size + 3);
        cout << "OK" << endl;

        //std::random_shuffle(dataset.begin(), dataset.end());
        //train_model(net, dataset, training_size);


        //cout << "Close test:" << endl;
        //test_model(*n, dataset.begin(), dataset.begin()+training_size);
        cout << "Open test:" << endl;
        test_model(*n, dataset.begin()+training_size, dataset.begin()+training_size+100);
        cout << "----------------------------------------------------------------" << endl;


        //net.dump();
        // Open test

        /*size_t in_size[2] = {1, ta[0]};
        size_t out_size[2] = {1, 1};
        Matrix2D in(&in_size[0]);
        in.random();
        //in.fill(1);
        Matrix2D out(&out_size[0]);*/



        /*vector<Matrix2D*> xs;
        vector<Matrix2D*> ys;
        build_xor_training_set(xs, ys);

        std::srand(time(NULL));

        net.dump();
        net.forward(in, out);
        cout << in.to_string() << endl;
        cout << out.to_string() << endl;

        for (int var = 0; var < 700000; ++var) {
                int i= var%4;//std::rand()%4;
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
        return 0;*/
}

