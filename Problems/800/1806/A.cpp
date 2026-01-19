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
    int xi,yi,xf,yf;
    cin >> xi >> yi >> xf >> yf;
    if(yi > yf)
        cout << -1 << "\n";
    else{
        int moves = yf - yi;
        xi = xi + moves;
        if(xf > xi)
            cout << -1 << "\n";
        else{
            moves += xi - xf;
            cout << moves << "\n";
        }
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
