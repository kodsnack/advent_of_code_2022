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

	part1 := func(part2 bool) int {
		sim := make(map[xy]int)
		for k, v := range world {
			sim[k] = v
		}

		for iters := 0; iters < 1000000; iters++ {
			sand := xy{500, 0}

			moves := 0
			for {
				if moves > maxy {
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

			if moves > maxy || moves == 0 {
				return iters
			}

			sim[sand] = 'S'
		}

		return 0
	}

	part2 := func() int {
		Q := []xy{{500, 0}}
		visited := make(map[xy]struct{})

		for len(Q) > 0 {
			sand := Q[0]
			Q = Q[1:]

			if len(visited) > 50_000 {
				break
			}

			if _, ok := visited[sand]; ok {
				continue
			}
			visited[sand] = struct{}{}

			if sand[1]+1 >= floor {
				continue
			}

			tests := [3]xy{
				{sand[0], sand[1] + 1},
				{sand[0] - 1, sand[1] + 1},
				{sand[0] + 1, sand[1] + 1},
			}

			for _, test := range tests {
				if _, ok := world[test]; !ok {
					Q = append(Q, test)
				}
			}
		}

		return len(visited)

	}

	fmt.Println(part1(false)) // 1072
	fmt.Println(part2())      // 24659
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
