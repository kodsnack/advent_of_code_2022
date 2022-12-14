use std::{
    collections::{HashSet, VecDeque},
    str::FromStr,
};

use aoc::{Puzzle, Solver};

pub struct Aoc;

impl Solver for Aoc {
    type Item = Rucksack;

    fn puzzle() -> aoc::Puzzle {
        Puzzle::new(2022, 3)
    }

    fn solve_one(inputs: &[Self::Item]) -> String {
        inputs.iter().map(|rs| rs.priority() as usize).sum::<usize>().to_string()
    }

    fn solve_two(inputs: &[Self::Item]) -> String {
        let mut badges: VecDeque<u8> = VecDeque::new();
        let mut group: Vec<Rucksack> = Vec::with_capacity(3);
        for rs in inputs {
            group.push(rs.clone());
            if group.len() == 3 {
                let common: HashSet<u8> = group
                    .iter()
                    .map(|rs| rs.as_set())
                    .reduce(|acc: HashSet<u8>, set: HashSet<u8>| {
                        acc.intersection(&set).copied().collect()
                    })
                    .expect("Should be exactly one set");
                let badge: u8 = *common.iter().next().expect("Should be exactly one element");
                badges.push_front(prio(badge));
                group.clear();
            }
        }

        badges.into_iter().map(|x| x as usize).sum::<usize>().to_string()
    }
}

fn prio(item: u8) -> u8 {
    match item {
        // A..=Z
        65..=90 => item - 38,
        // a..=z
        97..=122 => item - 96,
        _ => panic!("Invalid item {}", item),
    }
}

#[derive(Debug, Clone)]
pub struct Rucksack(Vec<u8>);

impl Rucksack {
    fn priority(&self) -> u8 {
        let i: u8 = self.intersection();
        prio(i)
    }

    fn first(&self) -> &[u8] {
        let div: usize = self.0.len() / 2;
        &self.0[0..div]
    }

    fn second(&self) -> &[u8] {
        let div: usize = self.0.len() / 2;
        &self.0[div..]
    }

    fn intersection(&self) -> u8 {
        let s0: HashSet<u8> = self.first().iter().copied().collect();
        let s1: HashSet<u8> = self.second().iter().copied().collect();
        *s0.intersection(&s1)
            .take(1)
            .copied()
            .collect::<Vec<u8>>()
            .first()
            .unwrap_or_else(|| {
                panic!(
                    "Should be exactly one element in intersection, was zero: {:?}, {:?}",
                    s0, s1
                )
            })
    }

    fn as_set(&self) -> HashSet<u8> {
        self.0.clone().into_iter().collect()
    }
}

impl FromStr for Rucksack {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Rucksack(s.as_bytes().into()))
    }
}

#[cfg(test)]
mod tests {
    use aoc::Solver;

    #[test]
    fn test_part2() {
        let input = r#"
        vJrwpWtwJgWrhcsFMMfFFhFp
        jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
        PmmdzqPrVvPwwTWBwg
        wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
        ttgJtRGJQctTZtZT
        CrZsJsPPZsGzwwsLwLmpwMDw
        "#;

        let output: String = crate::day3::Aoc::solve(input);
        assert_eq!("70", output);
    }
}
