#include <stdio.h>
#include <string.h>

char mp[303][303], seq[6005];
int n, m, u[303], d[303], l[303], r[303], ptr;

int main() {
    freopen("day22.txt", "r", stdin);
    while (scanf("%[^\n]%*c", mp[n])) {
        int l = strlen(mp[n]);
        if (!l) break;
        if (l > m) m = l;
        ++n;
    }
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j)
            if (!mp[i][j]) mp[i][j] = ' ';
    for (int i = 0; i < n; ++i) {
        int j = 0;
        while (j < m && mp[i][j] == ' ') ++j;
        l[i] = j;
        j = m - 1;
        while (j >= 0 && mp[i][j] == ' ') --j;
        r[i] = j;
    }
    for (int j = 0; j < m; ++j) {
        int i = 0;
        while (i < n && mp[i][j] == ' ') ++i;
        u[j] = i;
        i = n - 1;
        while (i >= 0 && mp[i][j] == ' ') --i;
        d[j] = i;
    }
    scanf("%s", seq);
    int x = 0, y = l[0], dir = 3;
    while (seq[ptr]) {
        int c = 0;
        while (seq[ptr] >= '0' && seq[ptr] <= '9') c = c * 10 + seq[ptr] - '0', ++ptr;
        while (c) {
            int nx, ny;
            switch (dir) {
                case 0: nx = x == d[y] ? u[y] : x + 1; ny = y; break;
                case 2: nx = x == u[y] ? d[y] : x - 1; ny = y; break;
                case 1: ny = y == l[x] ? r[x] : y - 1; nx = x; break;
                case 3: ny = y == r[x] ? l[x] : y + 1; nx = x; break;
            }
            if (mp[nx][ny] == '#') break;
            x = nx; y = ny; --c;
        }
        if (!seq[ptr]) break;
        if (seq[ptr] == 'L') dir = (dir + 3) % 4;
        if (seq[ptr] == 'R') dir = (dir + 1) % 4;
        ++ptr;
    }
    printf("%d\n", 1000 * (x + 1) + 4 * (y + 1) + (dir + 1) % 4);
    return 0;
}