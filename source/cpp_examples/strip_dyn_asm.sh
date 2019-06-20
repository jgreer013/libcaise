s2="((?<=\t)[a-z]*(?=  ))|(\t\n *\K[a-z]*)"

# For all files in /dynamic/
for f in ./dynamic/*
do
  # Create new filename
  b=$(basename $f)
  f2=${b::${#b}-4}
  f2=$f2"_only.txt"
  echo ./dynamic_only/$f2

  # Use regex on file and pipe results to new file
  grep -Po "$s2" $f > ./dynamic_only/$f2
done
