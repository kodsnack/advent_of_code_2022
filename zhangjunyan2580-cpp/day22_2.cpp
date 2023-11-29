// Wrap the cube by yourself.

#include <stdio.h>
#include <string.h>

#define BL 50
#define N(x) ((x) / BL)
#define I(x) ((x) % BL)
#define L(x) (I(x) == 0)
#define R(x) (I(x) == BL - 1)
#define U(x) (I(x) == 0)
#define D(x) (I(x) == BL - 1)
#define UE(x, y, i) (nx = (x) * BL, ny = (y) * BL + i)
#define DE(x, y, i) (nx = (x) * BL + BL - 1, ny = (y) * BL + i)
#define LE(x, y, i) (nx = (x) * BL + i, ny = (y) * BL)
#define RE(x, y, i) (nx = (x) * BL + i, ny = (y) * BL + BL - 1)
#define UM(x, y) (nx = (x) - 1, ny = (y), ndir = dir)
#define DM(x, y) (nx = (x) + 1, ny = (y), ndir = dir)
#define LM(x, y) (nx = (x), ny = (y) - 1, ndir = dir)
#define RM(x, y) (nx = (x), ny = (y) + 1, ndir = dir)
#define NI(r, x) ((r) ? (BL - 1 - (x)) : (x))
#define E(x, y, s, i) ((((s) & 1) ? (((s) & 2) ? RE(x, y, i) : LE(x, y, i)) : (((s) & 2) ? UE(x, y, i) : DE(x, y, i))), ndir = (s) ^ 2)

char mp[303][303], seq[6005];
int n, m, ptr;

int d[5][5][4] = {
    { { 0, 0, 0, 0 }, { 1, 1, 2, 0 }, { 1, 1, 3, 0 } },
    { { 0, 0, 0, 0 }, { 2, 1, 2, 0 } },
    { { 3, 0, 2, 0 }, { 3, 0, 3, 0 } },
    { { 0, 2, 2, 0 } }
}, u[5][5][4] = {
    { { 0, 0, 0, 0 }, { 3, 0, 1, 0 }, { 3, 0, 0, 0 } },
    { { 0, 0, 0, 0 }, { 0, 1, 0, 0 } },
    { { 1, 1, 1, 0 }, { 1, 1, 0, 0 } },
    { { 2, 0, 0, 0 } }
}, l[5][5][4] = {
    { { 0, 0, 0, 0 }, { 2, 0, 1, 1 }, { 0, 1, 3, 0 } },
    { { 0, 0, 0, 0 }, { 2, 0, 2, 0 } },
    { { 0, 1, 1, 1 }, { 2, 0, 3, 0 } },
    { { 0, 1, 2, 0 } }
}, r[5][5][4] = {
    { { 0, 0, 0, 0 }, { 0, 2, 1, 0 }, { 2, 1, 3, 1 } },
    { { 0, 0, 0, 0 }, { 0, 2, 0, 0 } },
    { { 2, 1, 1, 0 }, { 0, 2, 3, 1 } },
    { { 2, 1, 0, 0 } }
};

int main() {
    while (scanf("%[^\n]%*c", mp[n])) {
        int l = strlen(mp[n]);
        if (!l) break;
        if (l > m) m = l;
        ++n;
    }
    scanf("%s", seq);
    int x = 0, y = 50, dir = 3;
    while (seq[ptr]) {
        int c = 0;
        while (seq[ptr] >= '0' && seq[ptr] <= '9') c = c * 10 + seq[ptr] - '0', ++ptr;
        while (c) {
            int nx, ny, ndir, bx = N(x), by = N(y);
            switch (dir) {
                case 0: D(x) ?
                E(d[bx][by][0], d[bx][by][1], d[bx][by][2], NI(d[bx][by][3], I(y)))
                : DM(x, y); break;
                case 1: L(y) ?
                E(l[bx][by][0], l[bx][by][1], l[bx][by][2], NI(l[bx][by][3], I(x)))
                : LM(x, y); break;
                case 2: U(x) ?
                E(u[bx][by][0], u[bx][by][1], u[bx][by][2], NI(u[bx][by][3], I(y)))
                : UM(x, y); break;
                case 3: R(y) ?
                E(r[bx][by][0], r[bx][by][1], r[bx][by][2], NI(r[bx][by][3], I(x)))
                : RM(x, y); break;
            }
            if (mp[nx][ny] == '#') break;
            x = nx; y = ny; dir = ndir; --c;
        }
        if (!seq[ptr]) break;
        if (seq[ptr] == 'L') dir = (dir + 3) % 4;
        if (seq[ptr] == 'R') dir = (dir + 1) % 4;
        ++ptr;
    }
    printf("%d\n", 1000 * (x + 1) + 4 * (y + 1) + (dir + 1) % 4);
    return 0;
}