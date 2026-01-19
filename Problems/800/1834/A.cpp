#include <algorithm>
#include <bits/stdc++.h>
#include <climits>
#include <system_error>
#include <vector>
using namespace std;

#ifdef LOCAL
#include <chrono>
#include <sys/resource.h>
#endif

void problem(){
    int n;
    cin >> n;
    pmr::vector<int> a(n);
    int negative = 0, positive = 0,sum=0;
    for(int i=0;i<n;i++){
        cin >> a[i];
        if(a[i] < 0)
            negative++;
        else
         positive++;
        sum += a[i];
    }
    int tries = 0;
    while((sum < 0) || (negative % 2 != 0)){
        if(negative % 2 != 0){
            tries += 1;
            negative -= 1;
            sum += 2;
        }
        else{
            sum += 2;
            negative -= 1;
            tries += 1;
        }
    }
    cout << tries << "\n";
}
int main() {
    #ifdef LOCAL
    auto start = chrono::high_resolution_clock::now();
    #endif

    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    // --- Contest logic starts here ---
    ios::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    cin >> t;
    while (t--)
        problem();
    // --- Contest logic ends here ---
    //---
    // to run
    // g++ -std=c++17 -O2 -DLOCAL main.cpp -o main
    // ./main < input.txt
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    //
    #ifdef LOCAL
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> diff = end - start;

    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);

    cerr << fixed << setprecision(6);
    cerr << "Execution Time: " << diff.count() << " seconds\n";
    cerr << "Memory Used: " << usage.ru_maxrss / 1024.0 << " MB\n";
    #endif

    return 0;
}
