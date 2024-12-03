import argparse
import sys
from random import randint


# this function is mostly GPT-4o generated, but manually reviewed and adjusted
def cli_main():
    """entrypoint for CLI"""
    parser = argparse.ArgumentParser(
        description="Convert text to sarcasm text with specified inversion settings."
    )
    parser.add_argument(
        "text",
        type=str,
        nargs="*",
        help="The text to process as sarcasm.",
    )
    parser.add_argument(
        "--inversion_factor",
        "-f",
        type=float,
        default=60,
        help="Factor from 0 to 100 for case inversion (100 means all inversion at -p 0). "
        "Default=30",
    )
    parser.add_argument(
        "--inversion_penalty",
        "-p",
        type=float,
        default=35,
        help="Penalty rate affecting consecutive inversions, "
        "higher rate means less consecutive inversions. "
        "Default=100 (means no more than two consecutive inversions)",
    )
    parser.add_argument(
        "--allow-same-case",
        "-a",
        action="store_true",
        help="Allow resulting text to be in all upper or lower case.",
    )

    args = parser.parse_args()

    # If text is provided via command line arguments
    if args.text:
        input_text = " ".join(args.text)
    # If text is being piped in
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read().strip()
    else:
        parser.error("No text provided either as argument or through stdin.")

    if args.allow_same_case:
        result = make_sarcasm(
            input_text,
            inversion_factor=args.inversion_factor,
            inversion_penalty=args.inversion_penalty,
        )
    else:
        result = make_sarcasm_prevent_same_case(
            input_text,
            inversion_factor=args.inversion_factor,
            inversion_penalty=args.inversion_penalty,
        )

    print(result)



def make_sarcasm_prevent_same_case(
    text: str, inversion_factor: float, inversion_penalty: float
) -> str:
    """
    makes text to sArcAsM TExt
    :param text: the text to transform
    :param inversion_factor: the factor from 0 to 100 (100 means
    :param inversion_penalty: rate by which the
    :return:
    """

    if inversion_factor == 100 and inversion_penalty == 0:
        raise ValueError(
            f"Can't do {inversion_factor=} and {inversion_penalty=} in 'prevent same case mode'"
        )

    word_list = text.split(" ")
    new_words = []
    while len(word_list) > 0:
        word = word_list[0]
        new_word = make_sarcasm(
            word,
            inversion_factor=inversion_factor,
            inversion_penalty=inversion_penalty,
        )
        if (new_word.islower() or new_word.isupper()) and len(word) > 1:
            continue

        new_words.append(new_word)
        word_list = word_list[1:]

    return " ".join(new_words)


def make_sarcasm(text: str, inversion_factor: float, inversion_penalty: float) -> str:
    """
    makes text to sArcAsM TExt
    :param text: the text to transform
    :param inversion_factor: the factor from 0 to 100 (100 means invert all, if inversion_penalty=0)
    :param inversion_penalty: rate by which the
    :return:
    """
    new_str = ""

    was_last_swapped = False
    swap_prob = inversion_factor
    for c in text:
        draw = randint(0, 100)
        if was_last_swapped:
            swap_prob = swap_prob - inversion_penalty
        else:
            swap_prob = inversion_factor + inversion_penalty

        if swap_prob > draw:
            new_str += c.swapcase()
            was_last_swapped = True
        else:
            new_str += c
            was_last_swapped = False

    return new_str


if __name__ == "__main__":
    cli_main()
