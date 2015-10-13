#include <iostream>
using namespace std;
int main(){
	int t, n, k, startIndex;
	cin >> t;

	for (int i =0 ; i< t; i++){
		cin >> n >> k;

		int perm[n];

		for (int j =0; j < n; j++){
			
			if ((j/k) % 2 == 0){
				perm[j+k] = j;

			}
			else if ((j/k) % 2 == 1){

				perm[j-k] = j;
			}

			if ((j-k)/k % 2 == 0 && ((j-k)/k) +1 == (n/k)){
					perm[j-k] = perm[j-2*k];
					perm[j-2*k] = j;
			}

			if ((j/k) == (n/k)){
				startIndex = ((n/k)-1)*k + (j-(n/k) * k - 1);

				for (int i = startIndex + k ; i > startIndex; i--){
					perm[i+1] = perm[i];
				}

				perm[startIndex] = j;
				
			}




		}

		for (int i=0; i < n; i++){
			cout << perm[i]+1 << " ";
		}
	}

	return 0;
}