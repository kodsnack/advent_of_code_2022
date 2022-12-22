package main

import (
	_ "embed"
	"fmt"
	"strconv"
	"strings"
)

//go:embed input.txt
var input string

func main() {
	world := make(map[xy]rune)

	parts := strings.Split(input, "\n\n")

	for x, row := range strings.Split(parts[0], "\n") {
		for y, c := range row {
			if c == '.' || c == '#' {
				world[xy{x, y}] = c
			}
		}
	}

	walkedOn := make(map[xy]bool)

	var pos xy
	// left, up, right, down
	DX := []int{0, -1, 0, 1}
	DY := []int{-1, 0, 1, 0}
	var dir = 2

	// find start
	var miny int = 999999
	for p, ch := range world {
		if p[0] == 0 && ch == '.' {
			miny = min(miny, p[1])
		}
	}
	pos[1] = miny

	wrap := func(x, y, dx, dy int) (int, int, int, int) {

		// down
		if dx == 1 {
			if x == 49 { // B to C
				return y - 50, 99, 0, -1
			}
			if x == 149 { // D to F
				return y + 100, 49, 0, -1
			}
			if x == 199 { // F to B
				return 0, y + 100, 1, 0
			}

		}

		// up
		if dx == -1 {
			if x == 0 {
				if y < 100 { // A to F
					return y + 100, 0, 0, 1
				} else { // B to F
					return 199, y - 100, -1, 0

				}
			}
			if x == 100 { // E to C
				return y + 50, 50, 0, 1
			}
		}

		//right
		if dy == 1 {
			if y == 149 { // B to D
				return 149 - x, 99, 0, -1
			}
			if y == 99 {
				if x < 100 { // C to B
					return 49, x + 50, -1, 0
				} else { // D to B
					return 49 - (x - 100), 149, 0, -1
				}
			}
			if y == 49 { // F to D
				return 149, 50 + (x - 150), -1, 0
			}
		}

		// left
		if dy == -1 {
			if y == 50 {
				if x < 50 { // A to E
					return 149 - x, 0, 0, 1
				}
				if x >= 50 { // C to E
					return 100, x - 50, 1, 0
				}
			}
			if y == 0 {
				if x < 150 { // E to A
					return 49 - (x - 100), 50, 0, 1
				} else { // F to A
					return 0, x - 100, 1, 0

				}
			}
		}
		fmt.Println(x, y, dx, dy)
		return -1, -1, -1, -1
	}

	var pre string
	for idx, ch := range parts[1] {
		if ch == 'L' {
			dir = (dir - 1) % 4
			if dir < 0 {
				dir += 4
			}
			continue
		} else if ch == 'R' {
			dir = (dir + 1) % 4
			if dir < 0 {
				dir += 4
			}
			continue
		}

		pre += string(ch)

		if len(parts[1]) == idx+1 || (parts[1][idx+1] == 'L' || parts[1][idx+1] == 'R') {
			num, _ := strconv.Atoi(pre)
			pre = ""
			for i := 0; i < num; i++ {
				next := pos
				next[0] += DX[dir]
				next[1] += DY[dir]

				if _, ok := world[next]; !ok {
					nx, ny, ndx, ndy := wrap(pos[0], pos[1], DX[dir], DY[dir])

					next = xy{nx, ny}
					if _, ok := world[next]; !ok {
						fmt.Println(next)
						panic("outside of map")
					}

					// check if we can reverse and end up on the same spot
					{
						rx, ry, rdx, rdy := wrap(nx, ny, -ndx, -ndy)
						if rx != pos[0] || ry != pos[1] || -rdx != DX[dir] || -rdy != DY[dir] {
							fmt.Println(" in:", pos[0], pos[1], DX[dir], DY[dir])
							fmt.Println("out:", nx, ny, ndx, ndy)
							fmt.Println("inr:", nx, ny, -ndx, -ndy)
							fmt.Println("rev:", rx, ry, rdx, rdy)
							panic("not reversible")
						}
					}

					if world[next] == '.' {
						pos = next
						// set dir
						for ndir, dx := range DX {
							if dx == ndx && DY[ndir] == ndy {
								dir = ndir
								break
							}
						}
					}

				} else {

					// if can walk
					if world[next] == '.' {
						pos = next
					}
					walkedOn[pos] = true
				}
			}
		}
	}

	fmt.Println(pos)

	// left, up, right, down
	var face int // right, down, left, up
	switch dir {
	case 2: // right
		face = 0
	case 3:
		face = 1
	case 0: // left
		face = 2 // left
	case 1:
		face = 3
	}

	// 38598
	// p2 147024 too high
	fmt.Println((pos[0]+1)*1000 + (pos[1]+1)*4 + face)
}

type xy [2]int

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
