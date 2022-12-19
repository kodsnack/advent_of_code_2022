package main

import (
	_ "embed"
	"fmt"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"time"
)

//go:embed input.txt
var input string

func main() {
	input = strings.TrimSpace(input)

	var sum int
	var prod int = 1

	for k, row := range strings.Split(input, "\n") {

		if k == 3 {
			break
		}

		nums := intsInString(row)
		fmt.Println(nums)

		type qi struct {
			minute   int
			ore      int
			clay     int
			obsidian int
			geode    int

			oreRobot      int
			clayRobot     int
			obsidianRobot int
			geodeRobot    int
		}

		val := func(q qi) int {
			return q.ore + q.clay*10 + q.obsidian*100 + q.geode*10000
		}

		blueprint := nums[0]
		oreRobotOreCost := nums[1]
		clayRobotOreCost := nums[2]
		obsidianRobotOreCost := nums[3]
		obsidianRobotClayCost := nums[4]
		geodeRobotOreCost := nums[5]
		geodeRobotObsidianCost := nums[6]

		var maxgeodes int
		var maxmin int

		seen := make(map[qi]bool)

		Q := []qi{{oreRobot: 1}}
		t0 := time.Now()
		for len(Q) > 0 {

			if Q[0].minute > maxmin {
				maxmin = Q[0].minute

				// prune
				sort.Slice(Q, func(i, j int) bool {
					return val(Q[i]) > val(Q[j])
				})

				if len(Q) > 5_000_000 {
					Q = Q[0:5_000_000]
					continue
				}
			}

			q := Q[0]
			Q = Q[1:]

			if q.minute == 32 {
				if q.geode > maxgeodes {
					maxgeodes = q.geode
				}
				continue
			}

			if seen[q] {
				continue
			}
			seen[q] = true

			var buys int

			if q.ore >= geodeRobotOreCost && q.obsidian >= geodeRobotObsidianCost {
				Q = append(Q, qi{
					minute:   q.minute + 1,
					ore:      q.ore + q.oreRobot - geodeRobotOreCost,
					clay:     q.clay + q.clayRobot,
					obsidian: q.obsidian + q.obsidianRobot - geodeRobotObsidianCost,
					geode:    q.geode + q.geodeRobot,

					oreRobot:      q.oreRobot,
					clayRobot:     q.clayRobot,
					obsidianRobot: q.obsidianRobot,
					geodeRobot:    q.geodeRobot + 1,
				})
				buys++
			}

			if q.ore >= obsidianRobotOreCost && q.clay >= obsidianRobotClayCost {
				Q = append(Q, qi{
					minute:   q.minute + 1,
					ore:      q.ore + q.oreRobot - obsidianRobotOreCost,
					clay:     q.clay + q.clayRobot - obsidianRobotClayCost,
					obsidian: q.obsidian + q.obsidianRobot,
					geode:    q.geode + q.geodeRobot,

					oreRobot:      q.oreRobot,
					clayRobot:     q.clayRobot,
					obsidianRobot: q.obsidianRobot + 1,
					geodeRobot:    q.geodeRobot,
				})
				buys++
			}

			if q.ore >= clayRobotOreCost {
				Q = append(Q, qi{
					minute:   q.minute + 1,
					ore:      q.ore + q.oreRobot - clayRobotOreCost,
					clay:     q.clay + q.clayRobot,
					obsidian: q.obsidian + q.obsidianRobot,
					geode:    q.geode + q.geodeRobot,

					oreRobot:      q.oreRobot,
					clayRobot:     q.clayRobot + 1,
					obsidianRobot: q.obsidianRobot,
					geodeRobot:    q.geodeRobot,
				})
				buys++
			}

			if q.ore >= oreRobotOreCost {
				Q = append(Q, qi{
					minute:   q.minute + 1,
					ore:      q.ore + q.oreRobot - oreRobotOreCost,
					clay:     q.clay + q.clayRobot,
					obsidian: q.obsidian + q.obsidianRobot,
					geode:    q.geode + q.geodeRobot,

					oreRobot:      q.oreRobot + 1,
					clayRobot:     q.clayRobot,
					obsidianRobot: q.obsidianRobot,
					geodeRobot:    q.geodeRobot,
				})
				buys++
			}

			Q = append(Q, qi{
				minute:        q.minute + 1,
				ore:           q.ore + q.oreRobot,
				clay:          q.clay + q.clayRobot,
				obsidian:      q.obsidian + q.obsidianRobot,
				geode:         q.geode + q.geodeRobot,
				oreRobot:      q.oreRobot,
				clayRobot:     q.clayRobot,
				obsidianRobot: q.obsidianRobot,
				geodeRobot:    q.geodeRobot,
			})
		}

		fmt.Println("blueprint", blueprint, "geodes", maxgeodes, time.Since(t0))

		sum += blueprint * maxgeodes
		prod *= maxgeodes
	}

	fmt.Println(sum)
	fmt.Println(prod)
}

func intsInString(s string) []int {
	re := regexp.MustCompile(`-?\d+`)
	matches := re.FindAllString(s, -1)
	res := make([]int, len(matches))
	for i, m := range matches {
		res[i], _ = strconv.Atoi(m)
	}
	return res
}
