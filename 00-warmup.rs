// This file is part of Python Challenge Solutions
// https://github.com/scorphus/PythonChallengeSolutions

// Licensed under the BSD-3-Clause license:
// https://opensource.org/licenses/BSD-3-Clause
// Copyright (c) 2018, Pablo S. Blum de Aguiar <scorphus@gmail.com>

// http://www.pythonchallenge.com/pc/def/0.html

#![feature(test)]

extern crate test;

use test::Bencher;

fn warmup_bitwise() {
    println!("{}", 1i64 << 38);
}

fn warmup_powi() {
    println!("{}", 1f64.powi(38));
}

fn main() {
    warmup_bitwise();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[bench]
    fn bench_warmup_bitwise(b: &mut Bencher) {
        b.iter(|| warmup_bitwise());
    }

    #[bench]
    fn bench_warmup_powi(b: &mut Bencher) {
        b.iter(|| warmup_powi());
    }
}
