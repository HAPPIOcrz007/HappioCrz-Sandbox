---
topic:
  - A
  - Codeforces
  - CP31
  - CPP
  - ProblemSet
  - "1896"
tags:
  - cpSorting
  - cp800
link: https://codeforces.com/problemset/problem/1896/A
my_Answer: "[[1896A.cpp]]"
---
#### Notes
1. #cpPermutaion if of size n then 
#### submissions
1. https://codeforces.com/contest/1896/submission/355892607
```cpp
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
```