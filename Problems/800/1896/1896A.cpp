#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    cin >> t;
    while(t--){
        int n;
        cin >> n;
        long long a[n];
        for (int i = 0; i < n; i++)cin >> a[i];
        if(a[0] == 1)
            cout << "YES" << "\n";
        else
            cout << "NO" << "\n";
    }
}
