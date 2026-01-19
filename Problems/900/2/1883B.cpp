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
    long long n,k;
    cin >> n >> k;
    vector<char> a(n);
    vector<int> f(26,0);
    for(int i = 0; i < n; i++){
        cin >> a[i];
        f[int(a[i] - 'a')]++;
    }
    int odd_settings = 0;
    for(int i = 0; i < 26; i++){
        if(f[i] % 2 != 0)
            odd_settings++;
    }
    // if((k == 0) && (n == 1)){
    //     cout << "YES" << "\n";
    //     return;
    // }
    if(n == 1){
        cout << "YES" << "\n";
        return;
    }
    if((n % 2 == 1) && (n >= 3) && (odd_settings == 1)){
        cout << "YES" << "\n";
        return;
    }
    if(abs(k - odd_settings) == 1){
        cout << "YES" << "\n";
        return;
    }
    if(((k - odd_settings) < 0) && ((n -k) > 1)){
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
