#include <algorithm>
#include <bits/stdc++.h>
#include <climits>
#include <iostream>
#include <system_error>
#include <vector>
using namespace std;
using i32 = int;
using i64 = long long;

#ifdef LOCAL
#include <chrono>
#include <sys/resource.h>
#endif

void problem() {
    i64 n,k;
    cin >> n >> k;
    vector <i64> a(n);

    for(i64 i = 0; i < n; i++){
        cin >> a[i];
    }
    sort(a.begin(),a.end());
    i64 chain = 1, longest_chain = 1;
    for(i64 i = 1; i < n; i++){
        if((a[i] - a[i-1]) <= k){
            chain++;
        } else {
            chain = 1;
        }
        longest_chain = max(longest_chain, chain);
    }
    cout << n - longest_chain << "\n";
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
