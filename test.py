word = "W-W-W-W-W-L-W-W-W-W-L-W-W-W-W-L-L-L-D-L-W-D-W-D-L-W-D-W-W-D-D-D-D-W-W-W-L-W"
word_list = word.split("-")


if len(word_list) >= 15:
    if "D" in word_list:
        first_Draw = word_list.index("D")
        print(first_Draw)
        scores_before_first_draw = word_list[:first_Draw]
        print(scores_before_first_draw)
        scores_after_first_draw = word_list[first_Draw + 1:]
        print(scores_after_first_draw)
        if len(scores_before_first_draw) >= 15:
            if "D" not in scores_before_first_draw:
                print(f"No draw in first 15 matches")
            else:
                print(f"Draw in first 15 matches")

        elif len(scores_after_first_draw) >= 15:
            if "D" not in scores_after_first_draw:
                print(f"No draw in last 15 matches")
            else:
                print(f"Draw in last 15 matches")
    else:
        print("No Draw found in all matches")
