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

	world := make(map[xy]rune)
	_ = world

	rowStorms := make(map[xy]int) // delta y
	colStorms := make(map[xy]int) // delta x

	start := xy{0, 1}

	var maxx int
	var maxy int

	for x, row := range strings.Split(input, "\n") {
		for y, ch := range row {
			if ch == '<' {
				rowStorms[xy{x, y}] = -1
			} else if ch == '>' {
				rowStorms[xy{x, y}] = 1
			}
			if ch == '^' {
				colStorms[xy{x, y}] = -1
			} else if ch == 'v' {
				colStorms[xy{x, y}] = 1
			}
			world[xy{x, y}] = ch
			maxx = max(maxx, x)
			maxy = max(maxy, y)
		}
	}

	DX := []int{1, -1, 0, 0}
	DY := []int{0, 0, 1, -1}

	isStorm := func(pos xy, minute int) bool {
		// if a snowstorm is moving into this square, it will be blocked
		for sp, deltaY := range rowStorms {
			if sp[0] == pos[0] {
				stormY := mod((sp[1]+(deltaY*minute)-1), (maxy-1)) + 1
				if stormY == pos[1] {
					return true
				}
			}
		}

		// if a snowstorm is moving into this square, it will be blocked
		for sp, deltaX := range colStorms {
			if sp[1] == pos[1] {
				stormX := mod((sp[0]+(deltaX*minute)-1), (maxx-1)) + 1
				if stormX == pos[0] {
					return true
				}
			}
		}
		return false
	}

	type qi struct {
		pos      xy
		minutes  int
		endfirst bool
		start    bool
	}

	var maxmin int

	Q := []qi{{start, 0, false, false}}

	seen := make(map[qi]bool)

	var solvedP1 bool

	for {
		q := Q[0]
		Q = Q[1:]

		if q.minutes > maxmin {
			seen = make(map[qi]bool)
			maxmin = q.minutes
		}

		if seen[q] {
			continue
		}
		seen[q] = true

		if isStorm(q.pos, q.minutes) {
			continue
		}

		if q.pos[0] == 0 {
			if q.endfirst {
				q.start = true
			}
		}

		if q.pos[0] == maxx {
			if !q.endfirst {
				q.endfirst = true
			}

			if q.start {
				fmt.Println("part2", q.minutes)
				break
			}

			if !solvedP1 {
				solvedP1 = true
				fmt.Println("part1", q.minutes)
			}
		}

		for k, dx := range DX {
			next := xy{q.pos[0] + dx, q.pos[1] + DY[k]}
			if world[next] == '#' {
				continue
			}
			if _, ok := world[next]; !ok {
				continue
			}
			Q = append(Q, qi{next, q.minutes + 1, q.endfirst, q.start})
		}

		Q = append(Q, qi{q.pos, q.minutes + 1, q.endfirst, q.start})
	}
}

func mod(x, m int) int {
	return (x%m + m) % m
}

type xy [2]int

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
