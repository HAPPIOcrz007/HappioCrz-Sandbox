#include <algorithm>
#include <bits/stdc++.h>
#include <climits>
#include <iostream>
#include <system_error>
#include <vector>
using namespace std;

#ifdef LOCAL
#include <chrono>
#include <sys/resource.h>
#endif

void problem() {
    int n,m,h;
    cin >> n >> m >> h;
    vector<int> a(n);
    for(int i =0;i<n;i++) cin >> a[i];

    vector<int> b(m), c(m);
    for(int i =0;i<m;i++) cin >> b[i] >> c[i];

    // Track last crash
    int lastCrash = -1;
    vector<int> cur = a;

    for(int i =0;i<m;i++){
        cur[b[i]-1] += c[i];
        if(cur[b[i]-1] > h){
            lastCrash = i;
            cur = a;
        }
    }

    if(lastCrash != -1){
        cur = a;
        for(int i = lastCrash+1; i < m; i++){
            cur[b[i]-1] += c[i];
            if(cur[b[i]-1] > h){
                cur = a;
                lastCrash = i;
            }
        }
    }

    for(int i =0;i<n;i++) cout << cur[i] << " ";
    cout << "\n";
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
