year=2018
function aoc-test {
    problem=`basename \`pwd\``
    cat ~/data/advent-of-code-$year/${problem}/test$1 | ./main.py
}
function aoc-run {
    problem=`basename \`pwd\``
    cat ~/data/advent-of-code-$year/${problem}/input.txt | ./main.py
}
PS1="AOC-${year} $PS1"
