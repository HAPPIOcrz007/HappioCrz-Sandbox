#include <bits/stdc++.h>
using namespace std;

#ifdef LOCAL
#include <chrono>
#include <sys/resource.h>
#endif

const int base = 1337;

// Fast modular exponentiation
int power(int a, int k, int mod) {
    long long res = 1;
    long long x = a % mod;
    while (k > 0) {
        if (k & 1) res = (res * x) % mod;
        x = (x * x) % mod;
        k >>= 1;
    }
    return (int)res;
}

// powMod specialized for base = 1337
int powMod(int a, int k) {
    return power(a, k, base);
}

int superPow(int a, vector<int>& b) {
    if (b.empty()) return 1;
    int last = b.back();
    b.pop_back();
    return (power(superPow(a, b), 10, base) * powMod(a, last)) % base;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        int a;
        cin >> a;
        string line;
        cin.ignore(); // flush newline
        getline(cin, line);
        stringstream ss(line);
        vector<int> b;
        int x;
        while (ss >> x) b.push_back(x);

        cout << superPow(a, b) << "\n";
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
