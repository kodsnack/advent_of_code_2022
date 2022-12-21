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

	world := make(map[xy]int)
	var start, target xy

	for x, row := range strings.Split(input, "\n") {
		for y, ch := range row {
			world[xy{x, y}] = int(ch)
			if ch == 'S' {
				start = xy{x, y}
			}
			if ch == 'E' {
				target = xy{x, y}
			}
		}
	}

	fmt.Println(solve(world, start, target))

	var best int = 9999999
	for p, ch := range world {
		if ch == 'a' {
			r := solve(world, p, target)
			if r > 0 {
				best = min(best, r)
			}
		}
	}
	fmt.Println(best)
}

func solve(world map[xy]int, start, target xy) int {
	type qi struct {
		steps int
		pos   xy
	}

	best := map[xy]int{}

	Q := []qi{{0, start}}

	for {
		if len(Q) == 0 {
			break
		}
		q := Q[0]
		Q = Q[1:]

		if q.pos == target {
			return q.steps
		}

		if q.steps > 0 {
			if seen, ok := best[q.pos]; ok && q.steps >= seen {
				continue
			}
			best[q.pos] = q.steps
		}

		for _, n := range neighbour4(q.pos) {
			if _, ok := world[n]; !ok {
				continue
			}

			if world[q.pos] >= 'a' && world[q.pos] <= 'z' && world[n] >= 'a' && world[n] <= 'z' && world[n] > world[q.pos]+1 {
				continue
			}
			Q = append(Q, qi{q.steps + 1, n})
		}
	}
	return 0
}

type xy [2]int

func neighbour4(p xy) []xy {
	DX := []int{1, -1, 0, 0}
	DY := []int{0, 0, 1, -1}
	res := make([]xy, 4)
	for k, dx := range DX {
		res[k] = xy{p[0] + dx, p[1] + DY[k]}
	}
	return res
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
