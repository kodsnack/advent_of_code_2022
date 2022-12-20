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
	fmt.Println(play(false))
	fmt.Println(play(true))
}

func play(part2 bool) int {
	input = strings.TrimSpace(input)

	var nums []int
	var origNums []int

	set := make(map[int]bool)

	mapped := make(map[int]int)

	for idx, row := range strings.Split(input, "\n") {
		n, _ := strconv.Atoi(row)

		if part2 {
			n = n * 811589153
		}

		n2 := n*1000 + idx
		if set[n2] {
			panic("dupe")
		}
		set[n2] = true
		mapped[n2] = n

		nums = append(nums, n2)
		origNums = append(origNums, n2)
	}

	times := 1
	if part2 {
		times = 10
	}

	for t := 0; t < times; t++ {
		for _, v := range origNums {
			var idx int

			for i := 0; i < len(nums); i++ {
				if nums[0] == v {
					nums = nums[1:]
					idx = i
					break
				}
				nums = append(nums, nums[0])
				nums = nums[1:]
			}

			steps := mapped[v] % len(nums)
			if steps < 0 {
				steps += len(nums)
			}
			for i := 0; i < steps; i++ {
				nums = append(nums, nums[0])
				nums = nums[1:]
			}

			nums = append(nums, v)

			left := len(nums) - idx - steps - 1
			if left < 0 {
				left += len(nums) - 1
			}

			left = left % len(nums)
			for i := 0; i < left; i++ {
				nums = append(nums, nums[0])
				nums = nums[1:]
			}
		}
	}

	zero := 0
	for k, v := range nums {
		if mapped[v] == 0 {
			zero = k
			break
		}
	}

	a := nums[(zero+1000)%len(nums)]
	b := nums[(zero+2000)%len(nums)]
	c := nums[(zero+3000)%len(nums)]

	a = mapped[a]
	b = mapped[b]
	c = mapped[c]

	return a + b + c
}
