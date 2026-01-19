#include <algorithm>
#include <bits/stdc++.h>
#include <climits>
#include <cmath>
#include <iostream>
#include <system_error>
#include <vector>
using namespace std;

#ifdef LOCAL
#include <chrono>
#include <sys/resource.h>
#endif

struct Team { int idx; int score; int diff; };

void problem() {
    int n; cin >> n;
    vector<int> wins(n), draws(n), goals(n), concede(n);
    for (int i = 0; i < n; i++) cin >> wins[i];
    for (int i = 0; i < n; i++) cin >> draws[i];
    for (int i = 0; i < n; i++) cin >> goals[i];
    for (int i = 0; i < n; i++) cin >> concede[i];

    vector<Team> teams(n);
    for (int i = 0; i < n; i++){
        int score = 3 * wins[i] + draws[i];
        int diff = goals[i] - concede[i];
        teams[i] = {i, score, diff};
    }
    sort(teams.begin(), teams.end(), [](const Team &a, const Team &b){
        if (a.score != b.score) return a.score > b.score;
        if (a.diff != b.diff) return a.diff > b.diff;
        return a.idx < b.idx;
    });
    cout << teams[0].idx << " " << teams[1].idx << "\n";
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
