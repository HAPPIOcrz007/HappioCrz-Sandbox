#include <bits/stdc++.h>
#include <climits>
#include <vector>
using namespace std;

#ifdef LOCAL
#include <chrono>
#include <sys/resource.h>
#endif

void problem(){
    long long n;
    cin >> n;
    vector<long long> b(n), a;
    for (int i = 0; i < n; i++)
        cin >> b[i];
    a.push_back(b[0]);
    for (int i = 1; i < n; i++){
                if (b[i] >= b[i - 1])
                    a.push_back(b[i]);
                else{
                    a.push_back(b[i]);
                    a.push_back(b[i]);
                }
    }
    cout << a.size() << endl;
    for (auto it : a)
    cout << it << " ";
    cout << endl;
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
