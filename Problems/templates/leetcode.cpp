#include <bits/stdc++.h>
using namespace std;

#ifdef LOCAL
#include <chrono>
#include <sys/resource.h>
#endif

// Fast modular exponentiation

int main() {
    ios::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    cin >> t;
    while(t--){
        int a;
        vector<int> b;
        cin >> a;
        string line; // Read an entire line from input
        getline(cin, line); // Use stringstream to parse integers from the line std::
        stringstream ss(line);
        int x;
        while (ss >> x){
            b.push_back(x);
        }
        cout << "\n";
    }

    #ifdef LOCAL
    cerr << fixed << setprecision(6);

    // Benchmark modular exponentiation
    auto start = chrono::steady_clock::now();
    for (int i = 0; i < 1000000; i++) {
        volatile auto res = power(5, 25, 1000000007);
    }
    auto end = chrono::steady_clock::now();
    cerr << chrono::duration<double>(end - start).count() << " seconds\n";

    // Memory usage
    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);
    cerr << "Memory Used: " << usage.ru_maxrss / 1024.0 << " MB\n";
    #endif

    return 0;
}
