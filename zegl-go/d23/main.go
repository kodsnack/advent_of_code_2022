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
			north := []xy{{p[0] - 1, p[1] - 1}, {p[0] - 1, p[1]}, {p[0] - 1, p[1] + 1}}
			south := []xy{{p[0] + 1, p[1] - 1}, {p[0] + 1, p[1]}, {p[0] + 1, p[1] + 1}}
			west := []xy{{p[0] - 1, p[1] - 1}, {p[0], p[1] - 1}, {p[0] + 1, p[1] - 1}}
			east := []xy{{p[0] - 1, p[1] + 1}, {p[0], p[1] + 1}, {p[0] + 1, p[1] + 1}}

			var cnort, csouth, cwest, ceast int
			for _, n := range north {
				if world[n] {
					cnort++
				}
			}
			for _, n := range south {
				if world[n] {
					csouth++
				}
			}
			for _, n := range west {
				if world[n] {
					cwest++
				}
			}
			for _, n := range east {
				if world[n] {
					ceast++
				}
			}

			count := cnort + csouth + cwest + ceast

			if count == 0 {
				// nextworld[p] = p
				continue
			}

			countspos := []struct {
				count int
				pos   xy
			}{
				{cnort, xy{p[0] - 1, p[1]}},
				{csouth, xy{p[0] + 1, p[1]}},
				{cwest, xy{p[0], p[1] - 1}},
				{ceast, xy{p[0], p[1] + 1}},
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

		var moves int
		w2 := make(map[xy]bool)
		for p, next := range nextworld {
			if targets[next] == 1 {
				w2[next] = true
				world[p] = false
				delete(world, p)
				moves++
			}
		}

		if moves == 0 {
			fmt.Println("part2", i+1)
			// render(world)
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

			//render(world)
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
