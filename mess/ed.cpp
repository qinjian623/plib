#include <string>
#include <iostream>
#include <iomanip>

using namespace std;

void printMatrix(int ** matrix, int x, int y){
	for (int i = 0; i < x; ++i){
		for (int j = 0; j < y; ++j){
			cout << setw(3) << matrix[i][j];
		}
		cout << endl;
	}
}

int substituteCost(char t , char s){
	if (t == s){
		return 0;
	}
	return 2;
}

int min(int a, int b, int c){
	if (a > b){
		return b < c? b:c;
	}else {
		return a < c? a:c;
	}
}


int edit_distance(string a, string b)
{
	int length_a = a.length();
	int length_b = b.length();
	
	int ** matrix = new int*[length_a+1];
	for (int i = 0; i < length_a + 1; ++i){
		matrix[i] = new int[length_b + 1];
	}
	for (int i = 0; i < length_a + 1; ++i){
		for (int j = 0; j < length_b + 1; ++j){
			matrix[i][j] = 0;
		}
	}
	for (int i = 0; i < length_a + 1; ++i){
		matrix[i][0] = i;
	}
	for (int i = 0; i < length_b + 1; ++i){
		matrix[0][i] = i;
	}
	for (int i = 1; i <= length_a; ++i){
		for (int j = 1; j <= length_b; ++j){
			matrix[i][j] = min(matrix[i - 1][j] + 1,
					   matrix[i - 1][j - 1] + substituteCost(a[i - 1], b[j - 1]),
					   matrix[i][j - 1] + 1);
		}
	}

	int ret = matrix[length_a][length_b];
	
	for (int i = 0; i < length_a + 1; ++i){
		delete[] matrix[i];
	}
	delete[] matrix;
	
 	return ret;
}



int main(int argc, char *argv[])
{
	string a, b;
	cin >> a;
	cout << a << endl;
	cin >> b;
	cout << b << endl;
	cout << edit_distance(a, b)<< endl;
	return 0;
}










