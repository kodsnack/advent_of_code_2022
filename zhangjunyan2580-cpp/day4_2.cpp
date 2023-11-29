#include <stdio.h>

int ans;

int main() {
    {
        int l1, r1, l2, r2;
        while (~scanf("%d-%d,%d-%d", &l1, &r1, &l2, &r2)) ans += (r1 >= l2) && (r2 >= l1);
    }
    printf("%d\n", ans);
    return 0;
}