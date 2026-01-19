#include <algorithm>
#include <bits/stdc++.h>
#include <climits>
#include <cstdlib>
#include <iostream>
#include <system_error>
#include <vector>
using namespace std;

#ifdef LOCAL
#include <chrono>
#include <sys/resource.h>
#endif

void problem() {
    long long a,b,xk,yk,xq,yq;
    cin >> a >> b;
    cin >> xk >> yk;
    cin >> xq >> yq;
    long long xDiff,yDiff;
    xDiff = abs(xk - xq);
    yDiff = abs(yk - yq);
    int ans = 0;
    if((a < xDiff) || (a < yDiff) || (b < xDiff) || (b < yDiff)){
        if(xDiff == 0){
            if(((yDiff+1)/2 == a) || ((yDiff+1)/2 == b)){
                cout << 2 << "\n";
                return;
            }
        }
        else if (yDiff == 0) {
            if(((xDiff+1)/2 == a) || ((xDiff+1)/2 == b)){
                cout << 2 << "\n";
                return;
            }
        }
        else if ((xDiff > 0) && (yDiff > 0)) {
            if(xDiff == yDiff){
                if(xDiff % 2 == 1){
                    cout << 2 << "\n";
                    return;
                }
                else {
                    cout << 1 << "\n";
                    return;
                }
            }
            else {
                cout << 0 << "\n";
                return;
            }
        }
    }
    cout << 0 << "\n";
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
