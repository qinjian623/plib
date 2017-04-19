plot '~/sgd_0.01_momentum_0.9_epoch_50.log' using (100-$2) with lines title 'SGD[0.01,0.9]',\
     '~/sgd_0.01_momentum_0.5_epoch_50.log' using (100-$2) with lines title 'SGD[0.01,0.5]', \
     '~/sgd_0.001_momentum_0.9_epoch_50.log' using (100-$2) with lines title 'SGD[0.001,0.9]',\
     '~/sgd_0.001_momentum_0.99_epoch_50.log' using (100-$2) with lines title 'SGD[0.001,0.99]',\
     '~/adam_0.0001_epoch_50.log' using (100-$2) with lines title 'Adam[0.0001]',\
     '~/adam_0.001_epoch_50.log' using (100-$2) with lines title 'Adam[0.001]',\
     '~/adam_0.01_epoch_50.log' using (100-$2) with lines title 'Adam[0.01]',

