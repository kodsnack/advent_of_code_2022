#include <iostream>
#include <algorithm>
#include <utility>

std::pair<int, int> a[5005];
int bk[20005], n;
std::pair<int, int> b[5005];

int main() {
    while (std::cin >> a[n].first) ++n;
    for (int i = 0; i < n; ++i) a[i].second = ++bk[a[i].first + 10000], b[i] = a[i];
    for (int i = 0; i < n; ++i) {
        int k = 0;
        for (; b[k] != a[i]; ++k);
        if (a[i].first > 0) {
            int v = a[i].first;
            for (; v; --v) {
                int nk = k == n - 1 ? 0 : k + 1;
                std::swap(b[k], b[nk]);
                k = nk;
            }
        } else {
            int v = -a[i].first;
            for (; v; --v) {
                int nk = k == 0 ? n - 1 : k - 1;
                std::swap(b[k], b[nk]);
                k = nk;
            }
        }
    }
    int v;
    for (int i = 0; i < n; ++i)
        if (b[i].first == 0) {
            v = b[(i + 1000) % n].first + b[(i + 2000) % n].first + b[(i + 3000) % n].first;
            break;
        }
    std::cout << v << std::endl;
    return 0;
}