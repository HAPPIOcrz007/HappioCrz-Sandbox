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
    long long n, k, x;
    cin >> n >> k >> x;
    if (x != 1){
        cout << "YES" << endl;
        cout << n << endl;
        for (int i = 1; i <= n; i++)
            cout << 1 << " ";
        cout << endl;
    }
    else{
        if (k == 1 || (k == 2 && n % 2 == 1))
            cout << "NO" << endl;
        else{
            cout << "YES" << endl;
            if (n % 2 == 0){
                cout << n / 2 << endl;
                for (int i = 1; i <= n / 2; i++)
                    cout << 2 << " ";
                cout << endl;
            }
            else{
                cout << (n - 3) / 2 + 1 << endl;
                for (int i = 1; i <= (n - 3) / 2; i++)
                    cout << 2 << " ";
                cout << 3 << endl;
            }
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
