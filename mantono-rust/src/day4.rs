use std::{
    collections::HashSet,
    ops::{Range, RangeBounds},
    str::FromStr,
};

use aoc::Solver;

pub struct Aoc;

impl Solver for Aoc {
    type Item = Assignment;

    fn puzzle() -> aoc::Puzzle {
        aoc::Puzzle::new(2022, 4)
    }

    fn solve_one(inputs: &[Self::Item]) -> String {
        inputs.iter().filter(|x| x.fully_contains()).count().to_string()
    }

    fn solve_two(inputs: &[Self::Item]) -> String {
        inputs
            .iter()
            //.filter(|x| x.fully_contains())
            .filter(|x| x.intersection().len() > 0)
            //.reduce(|acc, e| acc.union(&e).copied().collect())
            //.unwrap()
            //.len()
            .count()
            .to_string()
    }
}

#[derive(Debug)]
pub struct Assignment(Range<u8>, Range<u8>);

impl Assignment {
    fn fully_contains(&self) -> bool {
        let s0: HashSet<u8> = self.0.clone().into_iter().collect();
        let s1: HashSet<u8> = self.1.clone().into_iter().collect();
        s0.is_subset(&s1) || s1.is_subset(&s0)
    }

    fn intersection(&self) -> HashSet<u8> {
        let s0: HashSet<u8> = self.0.clone().into_iter().collect();
        let s1: HashSet<u8> = self.1.clone().into_iter().collect();
        s0.intersection(&s1).into_iter().copied().collect()
    }
}

impl FromStr for Assignment {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut parts = s.split(",");
        let first = parts.next().expect("Invalid input");
        let second = parts.next().expect("Invalid input");
        Ok(Assignment(parse_range(first).unwrap(), parse_range(second).unwrap()))
    }
}

fn parse_range(input: &str) -> Result<Range<u8>, String> {
    let mut parts = input.split("-");
    let start: u8 = parse_num(parts.next())?;
    let end: u8 = parse_num(parts.next())?;
    Ok(Range {
        start,
        end: end + 1,
    })
}

fn parse_num(n: Option<&str>) -> Result<u8, String> {
    match n {
        Some(n) => match u8::from_str(n) {
            Ok(n) => Ok(n),
            Err(e) => Err(format!("Unable to convert to byte: {:?}", e)),
        },
        None => Err(String::from("Empty value")),
    }
}

#[cfg(test)]
mod tests {
    use aoc::Solver;

    #[test]
    fn test_solve_part2() {
        let input = r#"
            2-4,6-8
            2-3,4-5
            5-7,7-9
            2-8,3-7
            6-6,4-6
            2-6,4-8
        "#;

        let output: String = crate::day4::Aoc::solve(input);
        assert_eq!(String::from("4"), output)
    }
}
