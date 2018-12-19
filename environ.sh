year=2018
function aoc-test {
    problem=`basename \`pwd\``
    num=$1
    if [ "$1" != "" ]; then
       shift;
    fi
    export PYTHONPATH=~/code/advent-of-code-$year/:$PYTHONPATH
    cat ~/data/advent-of-code-$year/${problem}/test$num | ./main.py $*
}
function aoc-run {
    problem=`basename \`pwd\``
    export PYTHONPATH=~/code/advent-of-code-$year/:$PYTHONPATH
    cat ~/data/advent-of-code-$year/${problem}/input.txt | ./main.py $*
}
PS1="AOC-${year} $PS1"
