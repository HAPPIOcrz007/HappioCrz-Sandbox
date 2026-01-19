---
topic:
  - Codeforces
  - ProblemSet
  - "1899"
  - A
  - CPP
  - CP31
tags:
  - cpGames
  - cpMath
  - cpNumber_theory
  - cp800
link: https://codeforces.com/problemset/problem/1899/A
my_Answer: "[[1899A.cpp]]"
---
https://codeforces.com/problemset/submission/1900/355849222

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

        string s;
        cin >> s;

        bool patch = false;
        int gap = 0;

        for(int i =0 ; i< n; i++){
            if((i > 0) && (i < n-1)){
                if(s[i] == '.'){
                    if((s[i+1] == '.') && (s[i-1] == '.')){
                        patch = true;
                        break;
                    }
                }
            }
            if(s[i] == '.')
                gap += 1;
        }
        if(patch)
            cout << 2 << "\n";
        else
            cout << gap << "\n";
    }
}
```