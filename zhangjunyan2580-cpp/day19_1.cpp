#include <iostream>
#include "pystrlib.hpp"

int aa, ba, ca, cb, da, dc, gb;

int dfs(int k, int ar, int br, int cr, int dr, int a, int b, int c, int d, int cm) {
    if (k == 24) { if (d + dr > gb) gb = d + dr; return d + dr; }
    if (d + (2 * dr + 24 - k) * (25 - k) / 2 <= gb) return 0;
    int v = 0, t;
    int cca = a >= aa;
    int ccb = a >= ba && br < cb;
    int ccc = a >= ca && b >= cb && cr < dc;
    int ccd = a >= da && c >= dc;
    int n_cm = !cca | (!ccb << 1) | (!ccc << 2) | (!ccd << 3);
    if (((cm >> 3) & 1) && ccd) if ((t = dfs(k + 1, ar, br, cr, dr + 1, a + ar - da, b + br, c + cr - dc, d + dr, 15)) > v) v = t;
    if (((cm >> 2) & 1) && ccc) if ((t = dfs(k + 1, ar, br, cr + 1, dr, a + ar - ca, b + br - cb, c + cr, d + dr, 15)) > v) v = t;
    if (((cm >> 1) & 1) && ccb) if ((t = dfs(k + 1, ar, br + 1, cr, dr, a + ar - ba, b + br, c + cr, d + dr, 15)) > v) v = t;
    if (((cm >> 0) & 1) && cca) if ((t = dfs(k + 1, ar + 1, br, cr, dr, a + ar - aa, b + br, c + cr, d + dr, 15)) > v) v = t;
    if ((t = dfs(k + 1, ar, br, cr, dr, a + ar, b + br, c + cr, d + dr, n_cm)) > v) v = t;
    return v;
}

int main() {
    std::string line; int num = 0, ans = 0;
    while (std::getline(std::cin, line)) {
        ++num;
        std::vector<std::string> tokens = lib::split(line, " ");
        aa = std::stoi(tokens[6]); ba = std::stoi(tokens[12]); ca = std::stoi(tokens[18]);
        cb = std::stoi(tokens[21]); da = std::stoi(tokens[27]); dc = std::stoi(tokens[30]);
        gb = 0;
        ans += num * dfs(1, 1, 0, 0, 0, 0, 0, 0, 0, 15);
    }
    std::cout << ans << std::endl;
    return 0;
}