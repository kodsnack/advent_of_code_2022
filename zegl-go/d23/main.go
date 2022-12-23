package main

import (
	_ "embed"
	"fmt"
	"strings"
)

//go:embed input.txt
var input string

func main() {
	input = strings.TrimSpace(input)

	world := make(map[xy]bool)

	for x, row := range strings.Split(input, "\n") {
		for y, c := range row {
			if c == '#' {
				world[xy{x, y}] = true
			}
		}
	}

	for i := 0; i < 1000000; i++ {
		nextworld := make(map[xy]xy) // prev, next

		for p := range world {
			var N, S, W, E int

			for dx := -1; dx <= 1; dx++ {
				for dy := -1; dy <= 1; dy++ {
					if dx == 0 && dy == 0 {
						continue
					}
					if world[xy{p[0] + dx, p[1] + dy}] {
						if dx == -1 {
							N++
						}
						if dx == 1 {
							S++
						}
						if dy == -1 {
							W++
						}
						if dy == 1 {
							E++
						}
					}
				}
			}

			if N+S+W+E == 0 {
				continue
			}

			countspos := []struct {
				count int
				pos   xy
			}{
				{N, xy{p[0] - 1, p[1]}},
				{S, xy{p[0] + 1, p[1]}},
				{W, xy{p[0], p[1] - 1}},
				{E, xy{p[0], p[1] + 1}},
			}

			for ii := 0; ii < 4; ii++ {
				cp := countspos[(i+ii)%4]
				if cp.count == 0 {
					nextworld[p] = cp.pos
					break
				}
			}

		}

		targets := make(map[xy]int)
		for _, next := range nextworld {
			targets[next]++
		}

		w2 := make(map[xy]bool)
		for p, next := range nextworld {
			if targets[next] == 1 {
				w2[next] = true
				world[p] = false
			}
		}

		if len(w2) == 0 {
			fmt.Println("part2", i+1)
			return
		}

		// move leftovers
		for p, v := range world {
			if v {
				w2[p] = true
			}
		}

		world = w2

		if i == 9 {
			var minx, miny, maxx, maxy int = 999999, 999999, -999999, -999999
			for p := range world {
				minx = min(minx, p[0])
				miny = min(miny, p[1])
				maxx = max(maxx, p[0])
				maxy = max(maxy, p[1])
			}
			var count int
			for x := minx; x <= maxx; x++ {
				for y := miny; y <= maxy; y++ {
					if !world[xy{x, y}] {
						count++
					}
				}
			}
			fmt.Println("part1", count)
		}
	}
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
