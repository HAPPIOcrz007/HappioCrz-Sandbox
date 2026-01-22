#include <algorithm>
#include <bits/stdc++.h>
#include <climits>
#include <iostream>
#include <set>
#include <system_error>
#include <vector>
using namespace std;

#ifdef LOCAL
#include <chrono>
#include <sys/resource.h>
#endif

int mex(int a, int b) {
    if (a != 0 && b != 0) return 0;
    if (a != 1 && b != 1) return 1;
    return 2;
}

void problem() {
    int n;
    cin >> n;
    vector<int> a(n);
    int zeroes = 0;
    for(int i =0 ;i < n;i++){
        cin >> a[i];
        if(a[i] == 0)
            zeroes++;
    }
    sort(a.begin(),a.end());
    int globalMex = globalMex = mex(a[0], a[1]);
    for(int i =0 ;i < n-1;i++){
        globalMex = max(globalMex,mex(a[i], a[i+1]));
    }
    if(globalMex == 0){
        cout << "NO" << "\n";
        return;
    }
    if((globalMex == 1) && (zeroes >= 2)){
        cout << "NO" << "\n";
        return;
    }
    cout << "YES" << "\n";
    return;

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
