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

	// find start
	var miny int = 999999
	for p, ch := range world {
		if p[0] == 0 && ch == '.' {
			miny = min(miny, p[1])
		}
	}
	start := xy{0, miny}

	fmt.Println(solve(world, start, parts[1], wrap1))
	fmt.Println(solve(world, start, parts[1], wrap2))

}

type wrapFn func(world map[xy]rune, pos xy, dir int) (xy, int)

var (
	DX = []int{0, 1, 0, -1}
	DY = []int{1, 0, -1, 0}
)

func solve(world map[xy]rune, start xy, instrs string, fn wrapFn) int {
	var dir = 0
	pos := start

	var pre string
	for idx, ch := range instrs {
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

		if len(instrs) == idx+1 || (instrs[idx+1] == 'L' || instrs[idx+1] == 'R') {
			num, _ := strconv.Atoi(pre)
			pre = ""
			for i := 0; i < num; i++ {
				// pos, dir = wrap1(world, pos, dir)
				pos, dir = fn(world, pos, dir)
			}
		}
	}

	return (pos[0]+1)*1000 + (pos[1]+1)*4 + dir
}

func wrap2(world map[xy]rune, pos xy, dir int) (xy, int) {
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

		// right
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

			for ndir, dx := range DX {
				if dx == ndx && DY[ndir] == ndy {
					dir = ndir
					break
				}
			}
			return next, dir
		}

	} else {
		// if can walk
		if world[next] == '.' {
			return next, dir
		}
	}

	return pos, dir
}

func wrap1(world map[xy]rune, pos xy, dir int) (xy, int) {
	next := pos
	next[0] += DX[dir]
	next[1] += DY[dir]

	// wrap y
	if _, ok := world[next]; !ok && dir == 2 {
		var maxY int
		for pp := range world {
			if pp[0] == next[0] {
				maxY = max(maxY, pp[1])
			}
		}
		next[1] = maxY
	}

	if _, ok := world[next]; !ok && dir == 0 {
		var minY int = 999999999999
		for pp := range world {
			if pp[0] == next[0] {
				minY = min(minY, pp[1])
			}
		}
		next[1] = minY
	}

	// wrap x up to bottom
	if _, ok := world[next]; !ok && dir == 3 {
		var maxX int
		for pp := range world {
			if pp[1] == next[1] {
				maxX = max(maxX, pp[0])
			}
		}
		next[0] = maxX
	}

	if _, ok := world[next]; !ok && dir == 1 {
		var minX int = 999999999999
		for pp := range world {
			if pp[1] == next[1] {
				minX = min(minX, pp[0])
			}
		}
		next[0] = minX
	}

	// if can walk
	if world[next] == '.' {
		return next, dir
	}

	return pos, dir
}

type xy [2]int

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
