#include <vector>
#include <map>

#include <iostream>

using namespace std;

int main(int argc, char *argv[])
{
	vector<int> v(1000);
	map<int, int> m;
	v[100] = 10;
	m[100] = 10;
	m[100] = 11;
	
	cout << v.size() << endl;
	cout << m[100] << endl;
	return 0;
}
