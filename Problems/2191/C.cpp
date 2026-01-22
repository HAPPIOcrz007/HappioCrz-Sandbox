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
    string s;
    cin >> s;
    int zeroes = 0, ones = 0;
    vector<int> a(n);
    if (is_sorted(s.begin(), s.end())) {
        cout << "Bob\n";
    } else {
        cout << "Alice\n";
        cout << n << "\n";
        for (int i = 1; i <= n; i++) cout << i << " ";
        cout << "\n";
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
