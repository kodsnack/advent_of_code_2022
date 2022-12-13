package main

import (
	_ "embed"
	"encoding/json"
	"fmt"
	"sort"
	"strings"
)

//go:embed input.txt
var input string

func main() {
	input = strings.TrimSpace(input)

	var sum int
	var all []any

	for idx, pairs := range strings.Split(input, "\n\n") {
		pair := strings.Split(pairs, "\n")
		var first, second any
		json.Unmarshal([]byte(pair[0]), &first)
		json.Unmarshal([]byte(pair[1]), &second)
		all = append(all, first, second)
		if equal(first, second) <= 0 {
			sum += idx + 1
		}
	}

	fmt.Println(sum)

	alignments := []string{"[[2]]", "[[6]]"}
	for _, alignment := range alignments {
		var al any
		json.Unmarshal([]byte(alignment), &al)
		all = append(all, al)
	}

	sort.Slice(all, func(i, j int) bool {
		return equal(all[i], all[j]) < 0
	})

	var r int = 1
	for k, v := range all {
		str, _ := json.Marshal(v)
		if indexIn(alignments, string(str)) >= 0 {
			r *= k + 1
		}
	}

	fmt.Println(r)
}

func indexIn(haystack []string, needle string) int {
	for i, v := range haystack {
		if v == needle {
			return i
		}
	}
	return -1
}

func asAnySlice(a any) []any {
	switch a.(type) {
	case []any, []float64:
		return a.([]any)
	case float64:
		return []any{a}
	default:
		panic("unknown")
	}
}

func equal(first, second any) int {
	if a, ok := first.(float64); ok {
		if b, ok := second.(float64); ok {
			return int(a) - int(b)
		}
	}

	aList := asAnySlice(first)
	bList := asAnySlice(second)

	for i := range aList {
		if len(bList) <= i {
			return 1
		}
		if r := equal(aList[i], bList[i]); r != 0 {
			return r
		}
	}
	if len(aList) == len(bList) {
		return 0
	}
	return -1
}
