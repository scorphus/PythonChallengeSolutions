// This file is part of Python Challenge Solutions
// https://github.com/scorphus/PythonChallengeSolutions

// Licensed under the BSD-3-Clause license:
// https://opensource.org/licenses/BSD-3-Clause
// Copyright (c) 2018, Pablo S. Blum de Aguiar <scorphus@gmail.com>

// http://www.pythonchallenge.com/pc/def/map.html

static ORIGINAL: &str = "\
    g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. \
    bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. \
    sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj.";

fn caesar_decipher_byte(byte: u8, shift: i16) -> u8 {
    let (a, z) = ('a' as i16, 'z' as i16);
    if byte < a as u8 || byte > z as u8 {
        return byte
    }
    let translated = byte as i16 + shift;
    if translated > z {
        return (translated + a - z - 1) as u8
    }
    if translated < a {
        let kct = z - a + translated;
        return (kct) as u8
    }
    translated as u8
}

fn caesar_decipher_string(string: String, shift: i16) -> Result<String, std::string::FromUtf8Error> {
    let mut trans_vec = Vec::with_capacity(string.len());
    for byte in string.bytes() {
        trans_vec.push(caesar_decipher_byte(byte, shift))
    }
    String::from_utf8(trans_vec)
}

fn caesar_identify_shift(string: String, most_freq: char) -> i16 {
    let (a, t, z) = ('a' as u8, most_freq as i16, 'z' as u8);
    let mut count_vec: Vec<i32> = Vec::with_capacity(26);
    for _ in 0..26 {
        count_vec.push(0);
    }
    for byte in string.bytes() {
        if byte < a || byte > z {
            continue;
        }
        let index = (byte - a) as usize;
        count_vec[index] += 1;
    }
    let (mut max_byte, mut max_count) = (t, 0);
    for (byte, count) in count_vec.into_iter().enumerate() {
        if count > max_count {
            max_byte = byte as i16;
            max_count = count;
        }
    }
    t - a as i16 - max_byte
}

fn main() {
    for most_freq in vec!['e', 't', 'a', 'o', 'i', 'n', 's'] {
        let shift = caesar_identify_shift(ORIGINAL.to_string(), most_freq);
        println!("Shift from {} = {}?", most_freq, shift);
        match caesar_decipher_string(ORIGINAL.to_string(), shift) {
            Ok(translated) => {
                println!("Translated: {}", translated);
                let url = caesar_decipher_string("map".to_string(), shift).unwrap();
                println!("URL: {}.html", url);
            },
            Err(err) => println!("{} is a bad shift: {}", shift, err),
        }
        println!();
    }
}
