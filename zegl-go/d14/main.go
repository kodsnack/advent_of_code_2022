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
	input = strings.TrimSpace(input)

	world := make(map[xy]int)

	var maxx, maxy, minx, miny int = 0, 0, 100000, 100000

	for _, row := range strings.Split(input, "\n") {
		insts := strings.Split(row, " -> ")
		var prevxy xy
		for i, inst := range insts {
			rr := strings.Split(inst, ",")
			x, _ := strconv.Atoi(rr[0])
			y, _ := strconv.Atoi(rr[1])

			maxx = max(maxx, x)
			maxy = max(maxy, y)
			minx = min(minx, x)
			miny = min(miny, y)

			if i > 0 {
				if x == prevxy[0] {
					for y2 := min(y, prevxy[1]); y2 <= max(y, prevxy[1]); y2++ {
						world[xy{x, y2}] = '#'
					}
				} else {
					for x2 := min(x, prevxy[0]); x2 <= max(x, prevxy[0]); x2++ {
						world[xy{x2, y}] = '#'
					}
				}
			}
			prevxy = xy{x, y}
		}
	}

	floor := maxy + 2

	simulate := func(part2 bool) int {
		sim := make(map[xy]int)
		for k, v := range world {
			sim[k] = v
		}

		for lol := 0; lol < 1000000; lol++ {
			sand := xy{500, 0}

			moves := 0
			for {
				if moves > 1000000 {
					break
				}

				tests := []xy{
					{sand[0], sand[1] + 1},
					{sand[0] - 1, sand[1] + 1},
					{sand[0] + 1, sand[1] + 1},
				}

				if part2 && tests[0][1] == floor {
					break
				}

				moved := false
				for _, test := range tests {
					if _, ok := sim[test]; !ok {
						sand = test
						moves++
						moved = true
						break
					}
				}

				if moved {
					continue
				}
				break
			}

			if moves > 1000000 || moves == 0 {
				return lol
			}

			sim[sand] = 'S'
		}

		return 0
	}

	fmt.Println(simulate(false))    // 1072
	fmt.Println(simulate(true) + 1) // 24659

}

type xy [2]int

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
