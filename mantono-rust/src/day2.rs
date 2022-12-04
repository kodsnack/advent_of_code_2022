use std::str::FromStr;

use aoc::Solver;

pub struct Aoc;

impl Solver for Aoc {
    type Item = Line;

    fn solve_one(inputs: &[Self::Item]) -> String {
        inputs
            .iter()
            .map(|line| Round::try_from(*line).unwrap())
            .map(|round| (round.1, round.play()))
            .map(|(shape, outome)| score(shape, outome))
            .sum::<usize>()
            .to_string()
    }

    fn solve_two(inputs: &[Self::Item]) -> String {
        inputs
            .iter()
            .map(|line| Strategy::try_from(*line).unwrap())
            .map(|strat| (strat.play(), strat.1))
            .map(|(shape, outome)| score(shape, outome))
            .sum::<usize>()
            .to_string()
    }
}

fn score(shape: Shape, outcome: Outcome) -> usize {
    shape.score() + outcome.score()
}

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
pub struct Line(char, char);

impl FromStr for Line {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut tokens = s.split_ascii_whitespace();
        let left: &str = tokens.next().ok_or_else(|| String::from("Could not find left token"))?;
        let right: &str =
            tokens.next().ok_or_else(|| String::from("Could not find right token"))?;

        let left: char =
            left.parse().map_err(|_| format!("Unable to parse as char: '{}'", left))?;
        let right: char =
            right.parse().map_err(|_| format!("Unable to parse as char: '{}'", right))?;
        Ok(Line(left, right))
    }
}

#[derive(Copy, Clone)]
pub struct Strategy(Shape, Outcome);

impl Strategy {
    fn play(&self) -> Shape {
        match (self.0, self.1) {
            (Shape::Rock, Outcome::Lost) => Shape::Scissors,
            (Shape::Rock, Outcome::Draw) => Shape::Rock,
            (Shape::Rock, Outcome::Won) => Shape::Paper,
            (Shape::Paper, Outcome::Lost) => Shape::Rock,
            (Shape::Paper, Outcome::Draw) => Shape::Paper,
            (Shape::Paper, Outcome::Won) => Shape::Scissors,
            (Shape::Scissors, Outcome::Lost) => Shape::Paper,
            (Shape::Scissors, Outcome::Draw) => Shape::Scissors,
            (Shape::Scissors, Outcome::Won) => Shape::Rock,
        }
    }
}

impl From<Line> for Strategy {
    fn from(line: Line) -> Self {
        let shape: Shape = line.0.try_into().expect("Unable to parse shape");
        let outcome: Outcome = line.1.try_into().expect("Unable to parse outcome");
        Strategy(shape, outcome)
    }
}

pub struct Round(Shape, Shape);

impl Round {
    fn play(&self) -> Outcome {
        match (&self.0, &self.1) {
            (Shape::Rock, Shape::Rock) => Outcome::Draw,
            (Shape::Rock, Shape::Paper) => Outcome::Won,
            (Shape::Rock, Shape::Scissors) => Outcome::Lost,
            (Shape::Paper, Shape::Rock) => Outcome::Lost,
            (Shape::Paper, Shape::Paper) => Outcome::Draw,
            (Shape::Paper, Shape::Scissors) => Outcome::Won,
            (Shape::Scissors, Shape::Rock) => Outcome::Won,
            (Shape::Scissors, Shape::Paper) => Outcome::Lost,
            (Shape::Scissors, Shape::Scissors) => Outcome::Draw,
        }
    }
}

impl From<Line> for Round {
    fn from(line: Line) -> Self {
        let left: Shape = line.0.try_into().expect("Unable to parse left shape");
        let right: Shape = line.1.try_into().expect("Unable to parse right shape");
        Round(left, right)
    }
}

#[derive(Clone, Copy)]
enum Outcome {
    Lost,
    Draw,
    Won,
}

impl Outcome {
    fn score(&self) -> usize {
        match self {
            Outcome::Lost => 0,
            Outcome::Draw => 3,
            Outcome::Won => 6,
        }
    }
}

impl TryFrom<char> for Outcome {
    type Error = String;

    fn try_from(c: char) -> Result<Self, Self::Error> {
        match c {
            'X' => Ok(Outcome::Lost),
            'Y' => Ok(Outcome::Draw),
            'Z' => Ok(Outcome::Won),
            _ => Err(format!("Invalid outcome {}", c)),
        }
    }
}

#[derive(Copy, Clone)]
pub enum Shape {
    Rock,
    Paper,
    Scissors,
}

impl Shape {
    fn score(&self) -> usize {
        match self {
            Shape::Rock => 1,
            Shape::Paper => 2,
            Shape::Scissors => 3,
        }
    }
}

impl TryFrom<char> for Shape {
    type Error = String;

    fn try_from(c: char) -> Result<Self, Self::Error> {
        match c {
            'A' | 'X' => Ok(Shape::Rock),
            'B' | 'Y' => Ok(Shape::Paper),
            'C' | 'Z' => Ok(Shape::Scissors),
            _ => Err(format!("Unrecognized input for shape '{}'", c)),
        }
    }
}

#[cfg(test)]
mod tests {
    use aoc::Solver;

    use crate::day2;

    use super::Line;

    const INPUT: &str = "A Y\nB X\nC Z\n";

    #[test]
    fn test_parsing() {
        let parsed_input: Vec<Line> = vec![Line('A', 'Y'), Line('B', 'X'), Line('C', 'Z')];
        assert_eq!(parsed_input, day2::Aoc::parse_input(INPUT));
    }

    #[test]
    fn test_input_part1() {
        let parsed_input: Vec<Line> = vec![Line('A', 'Y'), Line('B', 'X'), Line('C', 'Z')];
        assert_eq!(String::from("15"), day2::Aoc::solve_one(&parsed_input));
    }
    #[test]
    fn test_input_part2() {
        let parsed_input: Vec<Line> = vec![Line('A', 'Y'), Line('B', 'X'), Line('C', 'Z')];
        assert_eq!(String::from("12"), day2::Aoc::solve_two(&parsed_input));
    }
}
