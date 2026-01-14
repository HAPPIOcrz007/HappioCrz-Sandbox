        #include <bits/stdc++.h>
        #include <cmath>
        using namespace std;

        #ifdef LOCAL
        #include <chrono>
        #include <sys/resource.h>
        #endif

        const long long MOD = 1000000007;

        long long modPow(long long base, long long exp, long long mod) {
            long long result = 1;
            base %= mod;
            while (exp > 0) {
                if (exp & 1) {
                    result = (result * base) % mod;
                }
                base = (base * base) % mod;
                exp >>= 1;
            }
            return result;
        }

        int countGoodNumbers(long long n) {
            long long evenCount = (n + 1) / 2;  // ceil(n/2)
            long long oddCount = n / 2;         // floor(n/2)

            long long evenWays = modPow(5, evenCount, MOD);
            long long oddWays = modPow(4, oddCount, MOD);

            return (int)((evenWays * oddWays) % MOD);
        }

        int main() {
            #ifdef LOCAL
            auto start = chrono::high_resolution_clock::now();
            #endif

            // --- Contest logic starts here ---
            ios::sync_with_stdio(false);
            cin.tie(NULL);
            int n;
            cin >> n;
            cout << countGoodNumbers(n) <<"\n";
            // --- Contest logic ends here ---
            //---
            // to run
            // g++ -std=c++17 -O2 -DLOCAL main.cpp -o main
            // ./main < input.txt
            //
            #ifdef LOCAL
            cerr << fixed << setprecision(6);
            auto start = chrono::steady_clock::now();
            for (int i = 0; i < 1000000; i++) {
                volatile auto res = power(5, 25, 1000000007);
            }
            auto end = chrono::steady_clock::now();
            cerr << chrono::duration<double>(end - start).count() << " seconds\n";
            cerr << "Memory Used: " << usage.ru_maxrss / 1024.0 << " MB\n";
            #endif

            return 0;
        }
