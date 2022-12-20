package main

import (
	_ "embed"
	"fmt"
	"strings"
)

//go:embed input.txt
var input string

var shapes = []string{
	`####`,

	`.#.
###
.#.`,

	`..#
..#
###`,

	`#
#
#
#`,

	`##
##`,
}

func main() {
	input = strings.TrimSpace(input)
	fmt.Println("p1", solve(2022))
	fmt.Println("p2", solve(1000000000000))
}

func solve(iters int) int64 {
	stones := make(map[xy]bool)
	var maxx int = 0
	var jetnumber int = 0

	DY := map[byte]int{'<': -1, '>': 1}

	topN := func(n int) string {
		var sb strings.Builder
		for x := maxx; x > maxx-n; x-- {
			for y := 0; y < 7; y++ {
				if stones[xy{x, y}] {
					sb.WriteRune('#')
				} else {
					sb.WriteRune('.')
				}
			}
		}
		return sb.String()
	}

	type seenstate struct {
		iteration int
		height    int
	}

	seen := make(map[string]seenstate)

	dropRock := func(r int) int64 {
		rock := shapes[r%len(shapes)]
		rockLayers := strings.Split(rock, "\n")

		if r == 0 {
			maxx = -1
		}

		var pos xy = [2]int{maxx + 3 + len(rockLayers), 2}

		canBlow := func() bool {
			ch := input[jetnumber%len(input)]
			jetnumber++

			dy := DY[ch]

			// check collides
			for x, row := range rockLayers {
				for y, ch := range row {
					if ch == '#' {
						pp := xy{pos[0] - x, y + pos[1] + dy}
						if stones[pp] {
							return false
						}
					}
				}
			}

			// check out of bounds
			if dy > 0 && pos[1]+len(rockLayers[0]) < 7 {
				return true
			}
			if dy < 0 && pos[1] > 0 {
				return true
			}

			return false
		}

		blow := func() {
			ch := input[(jetnumber-1)%len(input)]
			dy := DY[ch]
			pos[1] += dy
		}

		isOverlap := func() bool {
			for x, row := range rockLayers {
				for y, ch := range row {
					if ch == '#' {
						if stones[xy{pos[0] - x, y + pos[1]}] {
							return true
						}
					}
				}
			}
			return false
		}

		canFall := func() bool {
			if pos[0] == 0 {
				return false
			}
			if len(rockLayers)-pos[0]-1 == 0 {
				return false
			}
			pos[0]--
			overlap := isOverlap()
			pos[0]++
			return !overlap
		}

		fall := func() {
			pos[0]--
		}

		for {
			if canBlow() {
				blow()
			}
			if canFall() {
				fall()
			} else {
				break
			}
		}

		for x, row := range rockLayers {
			for y, ch := range row {
				if ch == '#' {
					pp := xy{pos[0] - x, y + pos[1]}
					stones[pp] = true
					maxx = max(maxx, pp[0])
				}
			}
		}

		if r > 3000 {
			// if has seen state before?
			key := topN(200)
			if prev, ok := seen[key]; ok {
				diffIters := r - prev.iteration
				remIters := iters - r
				if remIters%diffIters == 0 {
					height := int64(maxx + 1)
					diffHeight := height - int64(prev.height)
					remLoops := (remIters / diffIters) + 1
					return int64(prev.height) + int64(remLoops)*diffHeight - 1
				}
			}
			seen[key] = seenstate{
				iteration: r,
				height:    maxx + 1,
			}
		}

		return -1
	}

	for r := 0; r < iters; r++ {
		if x := dropRock(r); x > 0 {
			return x
		}
	}

	return int64(maxx + 1)
}

type xy [2]int

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
