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
    vector<int> a(n);
    for(int i =0;i<n; i++) cin >> a[i];
    bool sorted = true;
    for(int i =0;i<n-1; i++){
        if(a[i+1] < a[i]){
            sorted = false;
            break;
        }
    }
    if(sorted == false){
        cout << 0 << "\n";
    }
    else{
        int minDiff = INT_MAX;
        for(int i =0;i<n-1; i++){
            if(abs(a[i+1] - a[i]) < minDiff)
                minDiff = abs(a[i+1] - a[i]) + 1;
        }
        if(minDiff % 2 == 0)
            minDiff = minDiff/2;
        else
         minDiff = (minDiff+1)/2;
        cout << minDiff << "\n";
    }
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
