intcode_dir=$( realpath $( dirname "${BASH_SOURCE[0]}" ))

export CPATH=${intcode_dir}
export INTCODE_C=$(realpath ${intcode_dir}/intcode.c)
