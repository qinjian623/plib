
w1 = [0.550412, -0.0728101, 0.0115137, 0.816991, ;
-0.282518, 0.198864, -0.149404, -0.344874, ;
];

w2 = [0.550412, ;
-0.0728101, ;
0.0115137, ;
0.816991, ;
];

in = [1, 0]
label = [1]
o1 = tanh(in*w1)
o2 = tanh(tanh(in*w1)*w2)
out = tanh(tanh(in*w1)*w2)

loss = (out - label)^2
error = (out - label)
D2 = [1- o2^2]

step = 0.000001
del2 = error*D2

size(del2)

delw2= o1*step*del2



D1 = [0.74917, 0, 0, 0;
     0, 0.99472, 0, 0;
     0, 0, 0.99987, 0;
     0, 0, 0, 0.54649]
del1 = D1*w2*del2
delw1 = step*del1*in

w1 - delw1'
w2 - delw2'
