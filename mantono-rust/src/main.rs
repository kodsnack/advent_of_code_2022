mod day1;
mod day2;

fn main() {
    let answer: String = aoc::run::<day2::Aoc>().unwrap();
    println!("Answer: {}", answer);
}
