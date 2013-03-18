BEGIN{
    FS=" ";
    filename=
    print filename
    while (getline < filename){
	dic1[$2] = 0+$1;
    }
    print "Reading finished ......"
}
{
    score = dic1[$0]-0.5
    if (score < 0.0 ) score = -score
    printf ("%f %f %s\n",score,dic1[$0],$0)
}