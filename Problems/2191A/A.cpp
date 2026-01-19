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

void problem() {
    int n;
    cin >> n;
    vector<int> a(n);
    set<int> red, blue;
    for(int i = 0; i < n; i++){
        cin >> a[i];
        if(i % 2 == 1)
            red.insert(a[i]);
        if(i % 2 == 0)
            blue.insert(a[i]);
    }
    bool possiblity = true;
    for(int x : red){
        if( red.find(x+1) != red.end()){
            cout << "NO" << "\n";
            return;
        }
    }
    for(int x : blue){
        if( blue.find(x+1) != blue.end()){
            cout << "NO" << "\n";
            return;
        }
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
